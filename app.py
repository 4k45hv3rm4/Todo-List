from flask import Flask, url_for, render_template ,request , redirect, session
from flask_sqlalchemy import  SQLAlchemy

from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db  =SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), unique=True,  nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>'% self.id


@app.route('/',methods=['GET','POST'])
def index():

    if request.method == "POST":
        t_content = request.form["content"]
        new_t = TODO(content = t_content)
        try:
            db.session.add(new_t)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding task"
    else:
        tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template("index.html",tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    t_delete = TODO.query.get_or_404(id)
    try:
        db.session.delete(t_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting task."

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = TODO.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating task."
    return render_template('update.html',task=task)
if __name__ == "__main__":
    app.run()
