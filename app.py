from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"mydatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(50),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    category = db.Column(db.String(50),nullable=False)

@app.route('/create_tables')
def create_tables():
    db.create_all()
    return 'Tables created'


@app.route('/')
def add():
    return render_template('add.html')

@app.route('/add_expense',methods=['POST'])
def addExpense():
    date = request.form['date']
    name = request.form['expenseName']
    amount = request.form['amount']
    category = request.form['category']

    expense = Expense(date=date,name=name,amount=amount,category=category)

    db.session.add(expense)
    db.session.commit()

    return redirect('/expenses')

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    total=0
    t_business = 0
    t_other = 0
    t_food = 0
    t_entertainment = 0
    for exp in expenses:
        total += exp.amount
        if exp.category == 'business':
            t_business += exp.amount
        elif exp.category == 'other':
            t_other += exp.amount
        elif exp.category == 'food':
            t_food += exp.amount
        elif exp.category == 'entertainment':
            t_entertainment += exp.amount
        
    return render_template('expenses.html',expenses=expenses,total=total,t_business=t_business,t_entertainment=t_entertainment,t_food=t_food,t_other=t_other)

@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/update/<int:id>')
def update(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('update.html',expense=expense)

@app.route('/edit',methods=['POST'])
def edit():
    id = request.form['id']
    date = request.form['date']
    expenseName = request.form['expenseName']
    amount = request.form['amount']
    category = request.form['category']

    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.name = expenseName
    expense.amount = amount
    expense.category = category
    db.session.commit()
    return redirect('/expenses')



if __name__ == '__main__':
    app.run(debug=True, port=8080)