from flask import Flask, redirect, request, render_template, url_for, flash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
TASKS = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Adds a task to the TASKS list and flash a corresponding message
        if "ADD" in request.form:
            note = request.form["NOTE"].strip()
            if not note:
                flash("Please add a task to do", "error")
            else:
                TASKS.append({"note": note, "done": False})
                flash("Task was added to your Todo list", "success")
            return redirect(url_for("index"))

        # Marks a task as complete
        elif "COMPLETE" in request.form:
            id = int(request.form["COMPLETE"])
            TASKS[id]["done"] = True
            flash("Task hsa been completed!", "success")
            return redirect(url_for("index"))

        # Deletes the task
        elif "DELETE" in request.form:
            id = int(request.form["DELETE"])
            TASKS.pop(id)
            flash("Task has been deleted!", "success")
            return redirect(url_for("index"))

    pending = [t for t in TASKS if not t["done"]]
    done = [t for t in TASKS if t["done"]]
    return render_template("index.html", tasks=TASKS, pending= pending , done=done)

if __name__ == '__main__':
    app.run(debug=True)