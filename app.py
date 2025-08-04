from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Campeonato_grupos, Usuario
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Cria as tabelas e o usuário admin ao iniciar o app
with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(username="admin").first():
        admin = Usuario(username="admin", senha=generate_password_hash("admin"))
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso.")

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

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

        return redirect(url_for('editar_equipe_nomes', campeonato_id=novo_campeonato.id))
    except Exception as e:
        return f"Ocorreu um erro ao criar o campeonato: {e}", 500

@app.route('/eliminatoria_form')
def eliminatoria_form():
    return render_template('eliminatoria_form.html')

@app.route('/campeonato_grupos', methods=['GET', 'POST'])
def campeonato_grupos():
    if request.method == 'POST':
        total_equipes = int(request.form['total_equipes'])
        equipes_por_grupo = int(request.form['equipes_por_grupo'])
        classificacoes_por_grupo = int(request.form['classificacoes_por_grupo'])
        session['config_grupos'] = {
            'total_equipes': total_equipes,
            'equipes_por_grupo': equipes_por_grupo,
            'classificacoes_por_grupo': classificacoes_por_grupo
        }
        return redirect(url_for('editar_equipes'))
    return render_template('campeonato_grupos.html')

@app.route('/editar_equipes', methods=['GET', 'POST'])
def editar_equipes():
    config = session.get('config_grupos')
    if not config:
        return redirect(url_for('campeonato_grupos'))
    total = config['total_equipes']

    if request.method == 'POST':
        nomes_equipes = [request.form.get(f'equipe_{i}') for i in range(total)]
        session['nomes_equipes'] = nomes_equipes
        return redirect(url_for('mostrar_grupos'))

    return render_template('editar_equipes.html', total=total)

@app.route('/mostrar_grupos')
def mostrar_grupos():
    config = session.get('config_grupos')
    nomes = session.get('nomes_equipes')
    if not config or not nomes:
        return redirect(url_for('campeonato_grupos'))

    equipes_por_grupo = config['equipes_por_grupo']
    grupos = [nomes[i:i+equipes_por_grupo] for i in range(0, len(nomes), equipes_por_grupo)]

    return render_template('mostrar_grupos.html', grupos=grupos)

if __name__ == '__main__':
    app.run(debug=True)
