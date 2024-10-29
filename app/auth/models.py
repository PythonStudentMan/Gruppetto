from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Usuario(db.Model, UserMixin):

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    NombreUsuario = db.Column(db.String(80), nullable=False, unique=True)
    Password = db.Column(db.String(128), nullable=False)
    Email = db.Column(db.String(256), unique=True, nullable=False)
    EsAministrador = db.Column(db.Boolean, default=False)
    EsSupervisor = db.Column(db.Boolean, default=False)

    def __init__(self, NombreUsuario, Email):
        self.NombreUsuario = NombreUsuario
        self.Email = Email
        
    def __repr__(self):
        return f'<Usuario {self.NombreUsuario}>'
    
    def set_password(self, Password):
        self.Password = generate_password_hash(Password)

    def check_password(self, Password):
        return check_password_hash(self.Password, Password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Usuario.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)
    
    @staticmethod
    def get_by_email(Email):
        return Usuario.query.filter_by(Email=Email).first()
