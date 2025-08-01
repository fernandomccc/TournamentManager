from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Campeonato_grupos(db.Model):  # Nome da classe corrigido para coincidir com a convenção usada
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), default='grupos')  # Valor padrão pode ser útil
    total_equipes = db.Column(db.Integer, nullable=False)
    equipes_por_grupo = db.Column(db.Integer, nullable=False)
    classificados_por_grupo = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
