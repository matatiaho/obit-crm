import json
import re
import sqlite3
import time
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def split_name(full_name: str):
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


@dataclass
class Obituary:
    first_name: str
    last_name: str
    date_of_death: str
    url: str


class ObituaryDatabase:
    def __init__(self, db_path: str = "obituaries.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS obituaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                date_of_death TEXT,
                url TEXT UNIQUE
            )"""
        )
        self.conn.commit()

    def insert_if_new(self, obit: Obituary) -> bool:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT 1 FROM obituaries WHERE first_name=? AND last_name=? AND date_of_death=?",
            (obit.first_name, obit.last_name, obit.date_of_death),
        )
        if cur.fetchone():
            # duplicate
            return False
        cur.execute(
            "INSERT OR IGNORE INTO obituaries (first_name, last_name, date_of_death, url) VALUES (?, ?, ?, ?)",
            (obit.first_name, obit.last_name, obit.date_of_death, obit.url),
        )
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()


class ObituaryScraper:
    def __init__(self, db_path: str = "obituaries.db"):
        self.db = ObituaryDatabase(db_path)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def close(self):
        self.driver.quit()
        self.db.close()

    def _save_obituary(self, first: str, last: str, dod: str, url: str):
        obit = Obituary(first, last, dod, url)
        if self.db.insert_if_new(obit):
            print(f"Saved: {first} {last} {dod} -> {url}")
        else:
            print(f"Duplicate: {first} {last} {dod}")

    def scrape_mount_sinai(self):
        url = "https://mountsinaiparks.keeper.memorial/"
        self.driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            print("No data found on Mount Sinai page")
            return
        data = json.loads(script.string)
        queries = data.get("props", {}).get("pageProps", {}).get("dehydratedState", {}).get("queries", [])
        for q in queries:
            if q.get("queryKey", [])[0] == "MICROSITE_PROFILES":
                profiles = q.get("state", {}).get("data", {}).get("data", {}).get("profiles", [])
                for p in profiles:
                    first = p.get("firstName", "")
                    last = p.get("lastName", "")
                    dod = p.get("dateOfDeathDisplay", "")
                    slug = p.get("usernameForUrl", "")
                    profile_url = urljoin(url, slug)
                    self._save_obituary(first, last, dod, profile_url)
                break

    def scrape_echovita(self):
        base = "https://www.echovita.com"
        url = f"{base}/us/obituaries/ca/los-angeles"
        self.driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for card in soup.select("div.obit-list-wrapper"):
            name_a = card.select_one("a.text-name-obit-in-list")
            date_span = card.select_one("p.text-info-obit-in-list span")
            if not name_a or not date_span:
                continue
            name = name_a.get_text(strip=True)
            first, last = split_name(name)
            dod = date_span.get_text(strip=True)
            link = urljoin(base, name_a["href"])
            self._save_obituary(first, last, dod, link)

    def scrape_legacy(self):
        url = "https://www.legacy.com/us/obituaries/latimes/browse"
        self.driver.get(url)
        time.sleep(5)  # allow Cloudflare challenge to complete
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for row in soup.select("div.card__content"):
            link = row.select_one("a.card__title-link")
            date_span = row.select_one("span.date")
            if not link or not date_span:
                continue
            name = link.get_text(strip=True)
            first, last = split_name(name)
            dod = date_span.get_text(strip=True)
            self._save_obituary(first, last, dod, link["href"])

    def run(self):
        self.scrape_mount_sinai()
        self.scrape_legacy()
        self.scrape_echovita()


if __name__ == "__main__":
    scraper = ObituaryScraper()
    try:
        scraper.run()
    finally:
        scraper.close()
