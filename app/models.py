# app/models.py

from flask import url_for

from slugify import slugify
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timezone
from app import db

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    image_name = db.Column(db.String(256))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all,delete-orphan', order_by='asc(Comment.created)')

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all():
        return Post.query.all()
    
    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Post.query.order_by(Post.created.asc()).\
            paginate(page=page, per_page=per_page, error_out=False)

class Comment(db.Model):
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    user_name = db.Column(db.String(256))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    def __init__(self, content, user_id=None, user_name=user_name, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()




# Tabla de asociación intermedia para músicos que toquen varios instrumentos
miembro_instrumento = db.Table('miembro_instrumento',
    db.Column('miembroId', db.Integer, db.ForeignKey('miembros.id'), primary_key=True),
    db.Column('instrumentoId', db.Integer, db.ForeignKey('instrumentos.id'), primary_key=True)
)

class Instrumento(db.Model):

    __tablename__ = 'instrumentos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    familia = db.Column(db.Enum('Viento Madera', 'Viento Metal', 'Percusión Afinación Indeterminada', 'Percusión Afinación Determinada', 'Cuerda Frotada', 'Cuerda Pulsada', 
                            'Cuerda Percutida', 'Electrónicos', 'Electroacústicos'))

    # Relación inversa para acceder a los miembros que interpretan cada instrumento
    #miembros = db.relationship('Miembro', secondary=miembro_instrumento, back_populates='instrumentos',foreign_keys=[miembro_instrumento.c.miembroId, miembro_instrumento.c.instrumentoId])

    miembros = db.relationship('Miembro', secondary=miembro_instrumento, back_populates='instrumentos')

    def __init__(self, nombre, familia):
        self.nombre = nombre
        self.familia = familia

    def __repr__(self):
        return f'<Instrumento {self.nombre}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Instrumento.query.all()

    @staticmethod
    def get_by_nombre(nombre):
        return Instrumento.query.filter_by(nombre=nombre).first()
    


class Miembro(db.Model):

    __tablename__ = 'miembros'

    id = db.Column(db.Integer, primary_key=True)
    Foto = db.Column(db.String(256))
    Apellidos = db.Column(db.String(100), nullable=False)
    Nombre = db.Column(db.String(100), nullable=False)
    AsisteBandaEscuela = db.Column(db.Boolean)
    AsisteBandaTitular = db.Column(db.Boolean)
    AsisteLenguajeMusical = db.Column(db.Boolean)
    EsAlumnoEscuela = db.Column(db.Boolean)
    EsMayorEdad = db.Column(db.Boolean)
    EsSocio = db.Column(db.Boolean)
    EstaFederado = db.Column(db.Boolean)
    EsMusicoProfesional = db.Column(db.Boolean)
    EstudiaConservatorio = db.Column(db.Boolean)
    CorreoElectronico = db.Column(db.String(256), nullable=False)
    CodigoPostal = db.Column(db.String(5))
    Domicilio = db.Column(db.String(200))
    FechaAlta = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    FechaBaja = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    FechaNacimiento = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    IBANBancario = db.Column(db.String(24))
    ImporteCuota = db.Column(db.Numeric(4, 2))
    ImporteRecibo = db.Column(db.Numeric(4, 2))
    MotivoBaja = db.Column(db.String(256))
    MotivoReduccion = db.Column(db.String(256))
    NombreCompleto = db.Column(db.String(256), nullable=False)
    NumeroSocio = db.Column(db.String(6))
    OtroTelefono = db.Column(db.String(11))
    # Relación para accedor a la lista de instrumentos que interpreta el miembro
    instrumentos = db.relationship('Instrumento', secondary=miembro_instrumento, back_populates='miembros')
    
    # Instrumento principal (el que toca)
    instrumento_principal_id = db.Column(db.Integer, db.ForeignKey('instrumentos.id'))
    instrumento_principal = db.relationship('Instrumento', foreign_keys=[instrumento_principal_id], backref='principal_de_miembros')

    # Instrumento que toca en la banda escuela
    instrumento_banda_escuela_id = db.Column(db.Integer, db.ForeignKey('instrumentos.id'))
    instrumento_banda_escuela = db.relationship('Instrumento', foreign_keys=[instrumento_banda_escuela_id], backref='banda_escuela_de_miembros')

    # Instrumento que toca en la banda titular
    instrumento_banda_titular_id = db.Column(db.Integer, db.ForeignKey('instrumentos.id'))
    instrumento_banda_titular = db.relationship('Instrumento', foreign_keys=[instrumento_banda_titular_id], backref='banda_titular_de_miembros')

    Poblacion = db.Column(db.String(60))
    Provincia = db.Column(db.String(60))
    PorcentajeReduccion = db.Column(db.Numeric(3,2))
    Telefono = db.Column(db.String(11))
    Sexo = db.Column(db.Enum('Masculino', 'Femenino', 'Prefiero no indicarlo'))
    AsistenciasEventos = db.Column(db.Integer)
    FaltasEventos = db.Column(db.Integer)
    LogrosActuales = db.Column(db.Integer)

    def __repr__(self):
        return f'<Miembro {self.NombreCompleto}>'

    def save(self):
        if not self.id:
            db.session.add(self)
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Miembro.query.get(id)

    @staticmethod
    def get_by_nombrecompleto(nombrecompleto):
        return Miembro.query.filer_by(nombrecompleto).first()
    
    @staticmethod
    def get_by_instrumento(instrumento):
        return Miembro.query.filter_by(instrumento)
    
    @staticmethod
    def get_by_apellidos(apellidos):
        return Miembro.query.filter_by(apellidos)

    @staticmethod
    def get_all():
        return Miembro.query.all()
    
    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Miembro.query.order_by(Miembro.Apellidos.asc()).\
            paginate(page=page, per_page=per_page, error_out=False)