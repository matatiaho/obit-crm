from flask import Flask, render_template, redirect, url_for, request

from obit_scraper import ObituaryScraper, ObituaryDatabase
import pkg_resources
import sys

app = Flask(__name__)

@app.route('/')
def index():
    search = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'id')

    sort_map = {
        'name': 'last_name ASC, first_name ASC',
        'date': 'date_of_death ASC',
        'source': 'source ASC',
        'id': 'id DESC'
    }
    order_by = sort_map.get(sort, 'id DESC')

    db = ObituaryDatabase()
    cur = db.conn.cursor()
    query = 'SELECT * FROM obituaries'
    params = []
    if search:
        query += ' WHERE first_name LIKE ? OR last_name LIKE ?'
        like = f'%{search}%'
        params = [like, like]
    query += f' ORDER BY {order_by}'
    cur.execute(query, params)
    rows = cur.fetchall()
    db.close()
    return render_template('index.html', rows=rows, search=search, sort=sort)

@app.route('/run')
def run_scraper():
    scraper = ObituaryScraper()
    try:
        scraper.run()
    finally:
        scraper.close()
    return redirect(url_for('index'))


def _check_requirements(req_file: str = 'requirements.txt'):
    results = []
    try:
        with open(req_file) as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        return results
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        pkg = line.split('==')[0]
        try:
            dist = pkg_resources.get_distribution(pkg)
            version = dist.version
        except Exception:
            version = None
        results.append({'name': line, 'version': version})
    return results


@app.route('/requirements')
def requirements():
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    reqs = _check_requirements()
    return render_template('requirements.html', requirements=reqs, python_version=python_version)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
