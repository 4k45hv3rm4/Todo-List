# Todo-List

A Basic CRUD web app that allows to Add task, Update , View and Delete Them according to user Conventions  Using Flask-SQLalchemy .
Models include id, content , Date_created. id uniquely identifies the 
```
![Preview](https://photos.google.com/photo/AF1QipOxiCF5YmOSfaRyVIS1oZatHbpsRtlCc-7iZVzV)

## Getting Started

Fork this project on your Local Machine and install Python3.5 or above and Flask  or above in your system. ```cd``` into your orject directory . 

### Directory Structure

```
todo_ist/
        static/
              css/main.css
        template/
              base.html
              index.html
              update.html
        app.py
        test.db
        
```
#### Install Virtual Enviornment

Virtual environments are independent groups of Python libraries, one for each project. Packages installed for one project will not affect other projects or the operating system’s packages.
on your command line under project directory type

```>pip install virtualenv```

Create a virtual env named env 
using following line on windows command line
```>py -3 -m venv venv```

To Activate Virtual Enviornment type

```>venv\Scripts\activate```

You would've have seen 
Something like this on your cmd
``` 
(venv) C:\Users\lenovo\Desktop\todo_ist>```
```
##### Install Flask 

Within the activated environment, use the following command to install Flask:

```
$ pip install Flask
```

Now your system is ready to run this project 
on your system cmd
type
```
$ export FLASK_APP=hello.py
$ flask run
* Running on http://127.0.0.1:5000/  
```

Following are the code for individual File 
```
#app.py



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
    app.run(debug=True)
    
```

```
#base.html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width", intial-scale=1.0>
    <meta http-equiva="X_UA-compatible" content="ie=edge">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/main.css') }}">
    <!-- <title>Document</title> -->
    {% block head %}{% endblock %}
</head>
<body>
    {% block body %}{% endblock %}
</body>
</html>

```


```
#index.html

{% extends 'base.html' %}
{% block head %}
<title>Todoist</title>
{% endblock %}
{% block body %}
<h1>Task List</h1>
<div class="card-header">
    <div class="container-sm">

        {% if tasks|length <1 %}
            <div class="alert alert-success" role="alert">
      <h4 class="alert-heading">Welcome !</h4>
      <p class="mb-0">Your ToDo List seems empty .Click to Add Task</p>
    </div>

        {% else %}
    <div class="container-sm">

      <p class="mb-0">You have {{ tasks|length }} tasks.</p>
    </div>
            <table class="table-hover">
                <thead>
                <tr>
                    <th>Task</th>
                    <th>Added</th>
                    <th>Actions</th>
                </tr>
                </thead>
                <tbody>
                {% for task in tasks %}
                    <tr>
                        <td> {{ task.content }}</td>
                        <td> {{ task.date_created.date() }}</td>
                        <td>
                            <a href="delete/{{ task.id }}" class="btn btn-danger" role="button" aria-pressed="true">DELETE</a>
                            <br><br>
                            <a href="update/{{ task.id }}" class="btn btn-primary" role="button" aria-pressed="true">Update</a>
                        </td>
                    </tr>

                {% endfor %}
                </tbody>
            </table>
        {% endif %}
        <form action="/" method="POST">
            <input class="form-control shadow p-3 mb-5 bg-white rounded " aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" type="text" name="content" id="content" placeholder="Enter your task here">
            <input  type="submit" name="submit" value="Create new Task" class="btn btn-primary">
        </form>

    </div>
</div>

{% endblock %}

```


```
#update.html
{% extends 'base.html' %}
{% block head %}
<title>Todoist</title>
{% endblock %}

{% block body %}
<div class="content">
    <h1>Task List</h1>
    <div class="form">
        <form action="/update/{{ task.id }}" method="POST">
            <input class="form-control shadow p-1 mb-3 bg-white rounded " type="text" name="content" id="content" value="{{ task.content }}" style="width: 40%;text-align:center;margin-left: 30%">
            <input type="submit" value="Update">
        </form>
    </div>
</div>
{% endblock %}
```
## Authors

* **Akash Verma** - *Initial work* - [4k45hv3rm4](https://github.com/4k45hv3rm4)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for detail
