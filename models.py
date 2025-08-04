from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Campeonato_grupos(db.Model):
    __tablename__ = 'campeonato_grupos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), default="grupos")
    total_equipes = db.Column(db.Integer)
    equipes_por_grupo = db.Column(db.Integer)
    classificados_por_grupo = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
