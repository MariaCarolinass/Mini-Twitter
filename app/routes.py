from app import app, db
from flask import render_template, flash, url_for, request, redirect, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, RegisterPost

#API
@app.route('/api', methods=['GET'])
def Api_Info():
    """Informações da API"""
    api_info = {'version': 'v1'}
    return jsonify(api_info)

@app.route('/api/token')
@login_required
def get_auth_token():
    """Solicita token de autenticação"""
    token = current_user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@app.route('/api/register_users', methods=['GET'])
def register_users():
    """Carrega os dados dos usuários"""
    users = User.query.all()
    request_users = [r.as_dict() for r in users]
    return jsonify(request_users)

@app.route('/api/register_posts', methods=['GET'])
def register_posts():
    """Carrega os dados das postagens"""
    posts = Post.query.all()
    request_posts = [r.as_dict() for r in posts]
    return jsonify(request_posts)

#Página principal
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Cadastra e exibe uma nova postagem"""
    form = RegisterPost()
    if form.validate_on_submit():
        post = Post(message=form.message.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Parabéns, sua postagem foi cadastrada!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    # Exibi todas as postagens que o usuário cadastra e dos usuários seguidos
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Início', form=form,
        posts=posts.items, next_url=next_url, prev_url=prev_url)

#Encontrar mais postagens
@app.route('/explore')
@login_required
def explore():
    """Mostra todas as postagens de usuários"""
    page = request.args.get('page', 1, type=int)
    # Exibi todas as postagens, menos as postagens do usuário logado
    posts = Post.query.filter(Post.user_id != current_user.id).order_by(
        Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('explore.html', title='Encontrar postagens',
        posts=posts.items, next_url=next_url, prev_url=prev_url)

#Funcionalidades de login e cadastro do usuário
@app.route('/logout')
def logout():
    """Saí do login do usuário"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Faz a autenticação do usuário"""
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
    """Cadastra um novo usuário"""
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

#Funcionalidades de seguir e parar de seguir usuário
@app.route('/follow/<username>', methods=['GET', 'POST'])
def follow(username):
    """Segue um usuário"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário {} não encontrado.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Você não pode seguir a si mesmo!')
        return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash('Você está seguindo {}!'.format(username))
    return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['GET', 'POST'])
def unfollow(username):
    """Para de seguir um usuário"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário {} não encontrado.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Você não pode deixar de seguir a si mesmo!')
        return redirect(url_for('index'))
    current_user.unfollow(user)
    db.session.commit()
    flash('Você deixou de seguir {}.'.format(username))
    return redirect(url_for('index'))
