from flask import Flask, render_template,  request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# set up the database file path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create the database object
db = SQLAlchemy(app)

# define the table structure (model)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(100), nullable=False)


@app.route('/')
def home():

    # get all users from the database
    users = User.query.all() 


    return render_template(
        'index.html',
        title='Welcome to Flask App',
        name='Aneeqa Mehboob',
        rollno='12345',
        
         heading='Database Connection Successful',

         users = users       # send users list to HTML template


    )

@app.route('/dbstatus')
def dbstatus():
    try:
        count = User.query.count()
        message = f"Database connected successfully! Total users: {count}"
        print(message)  # 👈 this will show in the terminal
        return message  # 👈 this will show in the browser
    except Exception as e:
        error_message = f"Database connection failed: {e}"
        print(error_message)  # 👈 print in terminal
        return error_message  # 👈 show in browser
    

@app.route('/addusers')
def addusers():
    try:
        # create sample user data
        user1 = User(name='Ali Khan', email='ali@example.com', city='Lahore')
        user2 = User(name='Sara Ahmed', email='sara@example.com', city='Karachi')
        user3 = User(name='Usman Iqbal', email='usman@example.com', city='Islamabad')
        user4 = User(name='Fatima Noor', email='fatima@example.com', city='Peshawar')

        # add all users to the database
        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        print("✅ 4 users added successfully!")
        return "4 users added successfully!"
    except Exception as e:
        return f"Error: {e}"
    
@app.route('/update/<int:user_id>', methods=['POST'])
def update(user_id):
    user = User.query.get_or_404(user_id)
    user.name = request.form['name']
    user.email = request.form['email']
    user.city = request.form['city']
    db.session.commit()
    print(f"✅ User {user.id} updated successfully!")
    return redirect(url_for('home'))

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    print(f"🗑️ User {user.id} deleted successfully!")
    return redirect(url_for('home'))

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    city = request.form['city']

    new_user = User(name=name, email=email, city=city)
    db.session.add(new_user)
    db.session.commit()

    print(f"✅ New user '{name}' added successfully!")
    return redirect(url_for('home'))


# run the app
if __name__ == '__main__':

    # this will create the database file automatically if it doesn't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)

