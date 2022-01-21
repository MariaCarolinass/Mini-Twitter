from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, \
    Length
from app.models import User, Post

class LoginForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(),
        Length(min=1, max=110)], render_kw={"placeholder": "Digite o seu \
endereço de e-mail"})
    password = PasswordField('Senha:', validators=[DataRequired(),
        Length(min=1, max=120)], render_kw={"placeholder": "Digite a sua senha"})
    remember_me = BooleanField('Lembre de mim')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome:', validators=[DataRequired(),
        Length(min=1, max=75)], render_kw={"placeholder": "Digite o seu nome"})
    nickname = StringField('Apelido:', validators=[DataRequired(),
        Length(min=1, max=65)], render_kw={"placeholder": "Digite o seu apelido"})
    email = StringField('E-mail:', validators=[DataRequired(), Email(),
        Length(min=1, max=110)], render_kw={"placeholder": "Digite o seu \
endereço de e-mail"})
    password = PasswordField('Senha:', validators=[DataRequired(),
        Length(min=1, max=120)], render_kw={"placeholder": "Digite a sua senha"})
    password2 = PasswordField('Repetir senha:', validators=[DataRequired(),
        EqualTo('password'), Length(min=1, max=120)],
        render_kw={"placeholder": "Digite novamente a sua senha"})
    submit = SubmitField('Cadastrar')

    def validate_nickname(self, nickname):
        user = User.query.filter_by(nickname=nickname.data).first()
        if user is not None:
            raise ValidationError('Por favor use um apelido diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor use um endereço de e-mail diferente.')

class RegisterPost(FlaskForm):
    message = TextAreaField('Digite uma postagem:', validators=[DataRequired(),
        Length(min=1, max=150)], render_kw={"placeholder": "O que está havendo?"})
    submit = SubmitField('Enviar')
