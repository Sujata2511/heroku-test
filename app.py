from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# This is the class creating the all the attribute of the DataBase
class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)            # This is used for Primary Key
    title = db.Column(db.String(200),nullable=False)        # It used as a input 
    desc = db.Column(db.String(500),nullable=False)         # It used as a input
    date_created = db.Column(db.DateTime,default=datetime.utcnow()) # It used to pick the date time

    def __repr__(self) -> str:                   #  is a special method used to represent a class's objects as a string.
        return f"{self.sno} - {self.title}"
    
    # Page 1


#NOTE Here we work with the GET and POST so we need to pass the list of the methods
@app.route('/', methods=['GET','POST'])         # http://127.0.0.1:8000 When we write this URL then this function will run
def hello_world():
    if request.method=='POST':
        title = request.form['title']           # NOTE: Geting the value from the html in the title field
        desc = request.form['desc']
                                                 # NOTE: Here we see http://127.0.0.1:8000 this page the 'index.html' 
        todo = Todo(title=title, desc= desc)     # NOTE: Puting the value of the database which are getting from the Database
        db.session.add(todo)        # NOTE:Adding the object in the databas
        db.session.commit()         # NOTE: For successfuly commited in the database
    
    allTodo = Todo.query.all()  # NOTE: Geting all the list from the Data Base
    print(allTodo)              # Printing the Database Vallue in the terminal
        # By passing this parameter we get this database to the index.html file and we can get this data through the jinjer2 
        #NOTE: For this template we can display the value in the HTML table in the webpage 
    return render_template('index.html', allTodo=allTodo)    # render_template() use with the return statement
   

# NOTE: In this way we can make multiple page in the website
    # Page 2 
    # @app.route('/show')      # http://127.0.0.1:8000/Product When we type this URL then this function will executed
    # def product():
    #     allTodo = Todo.query.all()  # Getting all the list from the database
    #     print(allTodo)              # print all the list from the database
    #     return 'This is the Product page'

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title'] 
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first() 
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()    
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')     # Taking integer for serial number
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()    # applies a limit of one within the generated SQL, so that only one primary entity row is generated on the server side
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')            # After Deleting the data from the table we need to redirect to the same page '/' this is use to redirect the same page


if __name__ == '__main__':
    # debug=True Gives us an error document page 
    # NOTE: Only use on the develupment time otherwise it should be Faluse
    app.run(debug=True)     # Externaly set the port number 8000
