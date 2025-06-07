# Obituary Scraper

This project includes a simple Flask application that scrapes obituary
information from several websites. Scraped data is stored in a local
SQLite database and displayed on a web page using a small web interface
served by Flask.

## Prerequisites

- Python 3.8 or later
- Google Chrome (required for Selenium)
- (Optional) `venv` or another virtual environment tool

## Setup

1. *(Optional)* Create and activate a virtual environment so the installed
   packages stay isolated from the rest of your system:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # on Windows use "venv\Scripts\activate"
   ```
2. Install the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Running

1. Start the application:
   ```bash
   python app.py
   ```

2. Open `http://localhost:5000` in your browser. Click **Run Scraper** to
   trigger scraping. Use the search box or table headers to filter and sort
   results by name, date of death, or source. The table refreshes on each
   page load.

> **Note:** View the site through the address above. Opening
> `index.html` directly (for example with the Live Server extension) serves
> the page as static HTML and the `/run` route will not function.
