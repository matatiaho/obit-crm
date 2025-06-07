# Obituary Scraper

This project includes a simple Flask application that scrapes obituary
information from several websites. Scraped data is stored in a local
SQLite database and displayed on a web page using a small web interface
served by Flask.

## Prerequisites

- Python 3.8–3.11
- Google Chrome (required for Selenium)
- (Optional) `venv` or another virtual environment tool

> **Note:** Python 3.12 is currently unsupported because several
> dependencies still import `distutils`. Use Python 3.8–3.11 or install a
> version of `setuptools` that provides the `distutils` module:
>
> ```bash
> python3.11 -m venv venv     # or python3.12 if needed
> source venv/bin/activate
> pip install 'setuptools>=69'
> ```

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

3. Start the app and visit `/requirements` to verify your Python version and
   installed packages match the list above.

## Running

1. Start the application:
   ```bash
   python app.py
   ```

2. Open `http://localhost:5000` in your browser. Use the **Run Scraper**
   button to trigger scraping or click **Check Environment** to view your
   Python version and installed packages. The search box and table headers
   let you filter and sort results by name, date of death, or source. The
   table refreshes on each page load.

> **Note:** View the site through the address above. Opening
> `index.html` directly (for example with the Live Server extension) serves
> the page as static HTML and the `/run` route will not function.
