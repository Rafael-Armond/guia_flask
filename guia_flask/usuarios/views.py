from guia_flask import app, db, login_manager, login_required
from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt

from guia_flask.usuarios.models import User
from guia_flask.usuarios.forms import CadastroForm

# Blueprint
usuarios = Blueprint('usuarios',__name__,template_folder='templates')

@login_manager.user_loader
def load_user(_id):
    return User.query.filter_by(id=_id).first()

# Cadastrar usuário
@usuarios.route('/cadastrar',methods=['GET','POST'])
def cadastrar():
    bcrypt = Bcrypt()

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['senha']).first()

        if user is None:
            name = request.form['nome']
            email = request.form['email']
            password = bcrypt.generate_password_hash(request.form['senha']) 
            urole = request.form['urole']

            new_user = User(name,password,email,urole)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            flash("Usuário cadastrado com sucesso","success")
            return redirect(url_for('principal.index'))
        else:
            flash("E-mail já cadastrado.","warning")
            return redirect(url_for('usuarios.cadastrar'))
    
    return render_template("cadastro.html") 

# Login
@usuarios.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None:
            if user.check_password(request.form['password']):
                login_user(user)
                flash(f"{user.name} logado com sucesso.","success")
                return redirect(url_for('principal.index'))
            else:
                flash("Senha incorreta","warning")
                return redirect(url_for('usuarios.login'))
        else:
            flash("E-mail não cadastrado","warning")
            return redirect(url_for('usuarios.login'))
    return render_template("login.html")  

# Listar usuários
@usuarios.route('/listar')
@login_required()
def listar():
    users = User.query.all()
    return render_template("listar.html",users=users) 

# Deletar usuário
@usuarios.route('/deletar/<_id>')
@login_required(['admin'])
def deletar(_id):
    user = User.query.filter_by(id=_id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('usuarios.listar'))

# Editar usuário
@usuarios.route('/editar/<_id>',methods=['GET','POST'])
@login_required()
def editar(_id):
    bcrypt = Bcrypt()
    user = User.query.filter_by(id=_id).first()

    if user is not None:
        if request.method == 'POST':

            user.name = request.form['name']
            user.email = request.form['email']
            user.urole = request.form['urole']

            db.session.commit()
            flash("Usuário editado com sucesso.","success")
            return redirect(url_for('usuarios.listar'))

    else: 
        flash("Usuário não encontrado.","info")
    
    return render_template("editar.html",user=user) 

# Logout
@usuarios.route("/logout")
@login_required()
def logout():
    logout_user()
    return redirect(url_for('principal.index')) 

