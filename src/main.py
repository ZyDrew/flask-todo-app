from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from data import read_users_file, write_users_file
import os

# Définit le chemin absolu vers le dossier parent (où se trouvent templates/, static/, etc.)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = 'une_clé_secrète_pour_les_flashes'  # nécessaire

@app.route("/")
def home():
    users = read_users_file()
    logstate, username, tasks = get_users_state(users)

    return render_template("index.html", tasks=tasks, logstate=logstate, username=username)

@app.route("/user_register", methods=["POST"])
def user_register():
    username = request.form.get("register-username")
    password = request.form.get("register-password")

    users = read_users_file()
    for user in users:
        if username == user["username"]:
            flash("Nom d'utilisateur déjà existant", "error")
            return render_template("index.html", register_username=username)

    new_user = {
        "username" : username,
        "password" : password,
        "tasks" : []
    }

    users.append(new_user)
    write_users_file(users)

    session["logged_in"] = True
    session["username"] = username
    
    return redirect(url_for("home"))

@app.route("/user_login", methods=["POST"])
def user_login():
    username = request.form.get("login-username")
    password = request.form.get("login-password")

    users = read_users_file()
    user = check_user_loggin(users, username, password)

    if user is None:
        flash("Nom d'utilisateur ou mot de passe incorrect", "error")
        return render_template("index.html", login_username=username, login_password=password)
    
    session["logged_in"] = True
    session["username"] = username
    
    return redirect(url_for("home"))

@app.route("/user_logout", methods=["POST"])
def user_logout():
    session["logged_in"] = None
    session["username"] = None

    return redirect(url_for("home"))

@app.route("/add", methods=["POST"])
def add_task():
    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    urgent = False if request.form.get("urgent") == None else True

    new_task = {
        "text" : request.form.get("newTask"),
        "date" : dt,
        "done" : False,
        "urgent" : urgent,
        "category" : request.form.get("category")
    }

    if new_task["text"] != "":
        users = read_users_file()
        username = session.get("username")
        for user in users:
            if user["username"] == username:
                user["tasks"].append(new_task)
                continue

        write_users_file(users)

    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    users = read_users_file() 
    username = session.get("username")
    for user in users:
        if user["username"] == username:
            if 0 <= task_id < len(user["tasks"]):
                user["tasks"].pop(task_id)
                continue
    
    write_users_file(users)
    return redirect(url_for("home"))

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_done(task_id):
    users = read_users_file() 
    username = session.get("username")
    for user in users:
        if user["username"] == username:
            if 0 <= task_id < len(user["tasks"]):
                user["tasks"][task_id]["done"] = not user["tasks"][task_id]["done"]
                continue
    
    write_users_file(users)
    return "", 204

@app.route("/filter", methods=["POST"])
def filter_tasks():
    filter_main = request.form.get("filter-main")
    filter_order = request.form.get("filter-order")

    users = read_users_file()
    username = session.get("username")
    for user in users:
        if user["username"] == username:
            tasks = user["tasks"]
            continue

    if filter_order == "asc":
        filter_state = True
    elif filter_order == "desc":
        filter_state = False
    else:
        filter_state = False

    match filter_main:
        case "urgent":
            sorted_tasks = sorted(tasks, key=lambda task: task["urgent"], reverse=filter_state)
        case "category":
            sorted_tasks = sorted(tasks, key=lambda task: task["category"], reverse=filter_state)
        case "done":
            sorted_tasks = sorted(tasks, key=lambda task: task["done"], reverse=filter_state)
        case _:
            sorted_tasks = sorted(tasks, key=lambda task: task["text"], reverse=filter_state)

    for user in users:
        if user["username"] == username:
            user["tasks"] = sorted_tasks
            continue

    write_users_file(users)
    return render_template("task_list.html", tasks=sorted_tasks)

def get_tasks():
    users = read_users_file()
    username = session.get("username")
    for user in users:
        if user["username"] == username:
            return user["tasks"]

def get_users_state(users):
    logstate = ""
    username = ""
    tasks = []

    if session.get("logged_in"):
        logstate = "hidden"
        username = session.get("username")
        for user in users:
            if user["username"] == username:
                tasks = user["tasks"]
                continue

    return logstate, username, tasks

def check_user_loggin(users, username, password):
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                return user
    return None

if __name__ == "__main__":
    app.run(debug=True)
