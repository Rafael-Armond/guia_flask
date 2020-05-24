from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField, PasswordField, SelectField)
from wtforms.validators import DataRequired, Length, EqualTo, Email

from guia_flask.usuarios.models import User

# Formulário de cadastro
class CadastroForm(FlaskForm):
    name = StringField("Nome completo", validators=[DataRequired(message="Campo obrigatório")])
    password = PasswordField("Senha",validators=[DataRequired(message="Campo obrigatório"),Length(min=3, max=50,message="Mínimo de 3 caracteres e máximo de 50")])
    email = StringField("Email", validators=[DataRequired(message="Campo Obrigatório!"), Email(message="Campo Obrigatório"), Length(min=3, max=120, message="Mínimo de 3 caracteres e máximo de 120.")])
    conf_senha = PasswordField("Confirme sua senha", validators=[DataRequired(message="Campo Obrigatório!"), Length(min=0, max=50, message="Mínimo de 3 caracteres e máximo de 50")])
    urole = SelectField("Tipo de usuário", choices=[('user','Usuário'),('admin','Administrador')], validators=[DataRequired(message="Campo obrigatório!")])
    submit = SubmitField("Cadastrar")
