from app import app, db
from flask import render_template, flash, url_for, request, redirect
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, RegisterPost

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = RegisterPost()
    if form.validate_on_submit():
        post = Post(message=form.message.data)
        db.session.add(post)
        db.session.commit()
        flash('Parabéns, sua postagem foi cadastrada!')
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template('index.html', title='Início', form=form, posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('E-mail ou senha inválido')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Entrar', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, nickname=form.nickname.data,
            email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, seu usuário foi cadastrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastre-se', form=form)
