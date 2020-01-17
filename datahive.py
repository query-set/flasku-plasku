from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Zaloguj się lub zarejestruj")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(
                User(email=request.form['email'],
                     username=request.form['username'],
                     password=request.form['password']
                )
            )

            db.session.commit()
            return redirect(url_for('login'), message="Teraz możesz się zalogować.")
        except:
            return render_template('index.html', message="Taki użytkownik już istnieje!")
    else:
        print(request.method)
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        e = request.form['email']
        p = request.form['password']
        data = User.query.filter_by(email=e, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Niepoprawne dane!")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.secret_key = "datahiv"
    db.create_all()
    app.run()
