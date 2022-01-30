from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "apple"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    

#landing page
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

#user page
@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        course_list = Course.query.all()
        return render_template("user.html", course_list=course_list)
    else:
        return redirect(url_for("login"))

#add new course
@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        new_course = Course(title=title, complete=False)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("user"))

@app.route("/update/<int:course_id>")
def update(course_id):
    course = Course.query.filter_by(id=course_id).first()
    Course.complete = not Course.complete
    db.session.commit()
    return redirect(url_for("user"))


@app.route("/delete/<int:course_id>")
def delete(course_id):
    course = Course.query.filter_by(id=course_id).first()
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("user"))




if __name__ == "__main__":
    db.create_all()
    
    app.run(debug=True)
