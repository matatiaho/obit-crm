# Obituary Scraper

This project includes a simple Flask application that scrapes obituary
information from several websites. Scraped data is stored in a local
SQLite database and displayed on a web page.

## Running

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser. Click **Run Scraper** to
   trigger scraping. The table of obituaries refreshes on each page load.
