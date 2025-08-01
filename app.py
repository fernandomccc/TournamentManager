from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Campeonato_grupos
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


def criar_usuario_admin():
    db.create_all()
    if not Usuario.query.filter_by(username="admin").first():
        admin = Usuario(username="admin", senha=generate_password_hash("admin"))
        db.session.add(admin)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(username=request.form['username']).first()
        if usuario and check_password_hash(usuario.senha, request.form['senha']):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuário ou senha incorretos", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu com sucesso.", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/grupos_form')
def grupos_form():
    return render_template('grupos_form.html')

@app.route('/criar_campeonato_grupos', methods=['POST'])
def criar_campeonato_grupo():
    try:
        total_equipes = int(request.form['total_equipes'])
        equipes_por_grupo = int(request.form['equipes_por_grupo'])
        classificados_por_grupo = int(request.form['classificados_por_grupo'])

        novo_campeonato = Campeonato_grupos(
            total_equipes=total_equipes,
            equipes_por_grupo=equipes_por_grupo,
            classificados_por_grupo=classificados_por_grupo
        )
        db.session.add(novo_campeonato)
        db.session.commit()

        # Redirecionar para a página de edição de nomes das equipes
        return redirect(url_for('editar_equipe_nomes', campeonato_id=novo_campeonato.id))

    except Exception as e:
        return f"Ocorreu um erro ao criar o campeonato: {e}", 500

@app.route('/eliminatoria_form')
def eliminatoria_form():
    return render_template('eliminatoria_form.html')




if __name__ == '__main__':
    app.run(debug=True)
