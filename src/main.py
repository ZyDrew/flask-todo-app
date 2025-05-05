from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from data import read_tasks_file, write_tasks_file
import os

# Définit le chemin absolu vers le dossier parent (où se trouvent templates/, static/, etc.)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

tasks = read_tasks_file()

@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    new_task = {"id" : len(tasks), "text" : request.form.get("newTask"), "date" : dt, "done" : False}
    if new_task:
        tasks.append(new_task)
        write_tasks_file(tasks)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        write_tasks_file(tasks)
    return redirect(url_for("home"))

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_done(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
    write_tasks_file(tasks)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
