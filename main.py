from flask import Flask, redirect, make_response, render_template, request, session, url_for, flash
from flask_bootstrap import Bootstrap
from forms.login import UserLogin

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = ['SECRETKEY']


users = ['user1', 'user2', 'user3']


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def root():
    username = session.get('username')
    context = {
        'username': username
    }

    if username:
        flash('This is my first message')
        return render_template('content.html', **context)

    return render_template('content.html')


@app.route('/users')
def get_users():
    context = {
        'users': users
    }
    return render_template('users.html', **context)


@app.route('/users/<user_id>')
def get_user(user_id):
    context = {
        'user_id': user_id,
        'users': users
    }
    return render_template('base.html', **context)


@app.route('/users/<user_id>/ip')
def show_ip(user_id):
    user_ip = session.get('user_ip')
    context = {
        'user_id': user_id,
        'user_ip': user_ip
    }
    return render_template('show_ip.html', context=context)


@app.route('/users/<user_id>/get-ip')
def get_ip(user_id):
    user_ip = request.remote_addr
    response = make_response(redirect('/users/{}/ip'.format(user_id)))
    session['user_ip'] = user_ip
    return response

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    login_form = UserLogin()
    username = session.get('username')
    
    context = {
        'login': login_form,
        'username': username
        }

    #Adding validations for users
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        return redirect(url_for('root'))

    return render_template('login.html', **context)



