from flask import Flask, render_template_string, redirect, url_for

from obit_scraper import ObituaryScraper, ObituaryDatabase

app = Flask(__name__)

INDEX_TEMPLATE = """
<!doctype html>
<title>Obituary Scraper</title>
<h1>Obituary Records</h1>
<a href="{{ url_for('run_scraper') }}">Run Scraper</a>
<table border="1" cellpadding="5">
    <tr><th>First Name</th><th>Last Name</th><th>Date of Death</th><th>URL</th></tr>
    {% for row in rows %}
    <tr>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
        <td><a href="{{ row[4] }}" target="_blank">link</a></td>
    </tr>
    {% endfor %}
</table>
"""

@app.route('/')
def index():
    db = ObituaryDatabase()
    cur = db.conn.cursor()
    cur.execute('SELECT * FROM obituaries ORDER BY id DESC')
    rows = cur.fetchall()
    db.close()
    return render_template_string(INDEX_TEMPLATE, rows=rows)

@app.route('/run')
def run_scraper():
    scraper = ObituaryScraper()
    try:
        scraper.run()
    finally:
        scraper.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
