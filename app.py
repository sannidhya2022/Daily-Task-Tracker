from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
from datetime import datetime
import io
from time import strptime

app = Flask(__name__)

TASKS_FILE = "tasks.csv"

def load_tasks():
    try:
        with open(TASKS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

def save_task(task):
    with open(TASKS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=task.keys())
        if file.tell() == 0:  
            writer.writeheader()
        writer.writerow(task)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        task = request.form['task']
        solution = request.form['solution']
        urgency = request.form['urgency']

        task_data = {
            'date': date,
            'task': task,
            'solution': solution,
            'urgency': urgency
        }
        save_task(task_data)
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/view', methods=['GET'])
def view_tasks():
    tasks = load_tasks()
    grouped_tasks = {}
    for task in tasks:
        month = datetime.strptime(task['date'], '%Y-%m-%d').strftime('%B %Y')
        if month not in grouped_tasks:
            grouped_tasks[month] = []
        grouped_tasks[month].append(task)
    return render_template('view_tasks.html', grouped_tasks=grouped_tasks)

@app.route('/export', methods=['GET'])
def export_tasks():
    tasks = load_tasks()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['date', 'task', 'solution', 'urgency'])
    writer.writeheader()
    writer.writerows(tasks)

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='tasks.csv'
    )

if __name__ == '__main__':
    app.run(debug=False, port=5000)