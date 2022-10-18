from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def main():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route('/indexParent')
def parent():
    todo_list = Todo.query.all()
    return render_template('indexParent.html', todo_list=todo_list)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


# -------------------- #
# ------Start-Of-------#
# -------------------- #
# ---Authentication----#
# -------------------- #
# -------------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    #todo_list = Todo.query.all()
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') or request.form['password'] != 'tmp':
            error = 'Invalid Credentials. Please try again.'
        else:
            #session['logged_in'] = True
            #flash('You were logged in.')
            return redirect(url_for('parent'))

   #     if(request.form["username"] == "") or request.form["password"] == "":
   #         return render_template("main", todo_list=todo_list)
   #     if(request.form["username"] == "admin") or request.form["password"] == "tmp":
  #          return render_template("parent", todo_list=todo_list)
  #      else:
 #           error = "Invalid Credentials. Try again!"

    return render_template('login.html', error=error)

# -------------------- #
# ------Start-Of-------#
# -------------------- #
# ----Interactives---- #
# -------------------- #
# -------------------- #


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("parent"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("main"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("parent"))

# -------------------- #
# -------End-Of--------#
# -------------------- #
# ----Interactives---- #
# -------------------- #
# -------------------- #





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="10.0.0.149", port=80)
