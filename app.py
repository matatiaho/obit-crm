from flask import Flask, render_template, redirect, url_for

from obit_scraper import ObituaryScraper, ObituaryDatabase

app = Flask(__name__)

@app.route('/')
def index():
    db = ObituaryDatabase()
    cur = db.conn.cursor()
    cur.execute('SELECT * FROM obituaries ORDER BY id DESC')
    rows = cur.fetchall()
    db.close()
    return render_template('index.html', rows=rows)

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
