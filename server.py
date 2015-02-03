from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
import sqlite3

app = Flask(__name__)

conn = None

def get_conn():
	global conn
	if conn is None:
		conn = sqlite3.connect('database.sql')
		# Dictionary results
		conn.row_factory = sqlite3.Row
	return conn

def close_connection():
	global conn
	if conn is not None:
		conn.close()

def query_db(query, args=(), one=False):
	cur = get_conn().cursor()
	cur.execute(query, args)
	r = cur.fetchall()
	cur.close()
	return (r[0] if r else None) if one else r

def add_task(category, priority, description):
	query_db('INSERT INTO tasks values(?, ?, ?)', (category, priority, description), one=True)
	get_conn().commit()

@app.route('/', methods=['GET', 'POST'])
def tasks():
	if request.method == "POST":
		category = request.form['category']
		priority = request.form['priority']
		description = request.form['description']
		add_task(category, priority, description)
		return redirect(url_for('tasks'))
	else:
		tasks = query_db('SELECT * FROM tasks ORDER BY priority DESC')
		return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
	app.debug = True
	app.run()
