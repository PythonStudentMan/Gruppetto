from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, DecimalField, SelectField, IntegerField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from wtforms.validators import DataRequired, Length, Email

from app.models import Instrumento

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    post_image = FileField('Imagen de Cabecera', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes')])
    submit = SubmitField('Guardar')

class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')

class MiembroForm(FlaskForm):
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    Apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=100)])
    Foto = FileField('Fotografía', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes')])
    AsisteBandaEscuela = BooleanField('Asiste a Banda Escuela')
    AsisteBandaTitular = BooleanField('Asiste a Banda Titular')
    AsisteLenguajeMusical = BooleanField('Recibe clases de Lenguaje Musical')
    EsAlumnoEscuela = BooleanField('Recibe clases de Instrumento')
    EsMayorEdad = BooleanField('Es Mayor de Edad')
    EsSocio = BooleanField('Es Socio')
    EstaFederado = BooleanField('Está Federado')
    EsMusicoProfesional = BooleanField('Es Músico Profesional')
    EstudiaConservatorio = BooleanField('Recibe estudios musicales fuera de la agrupación')
    CorreoElectronico = StringField('Email', validarots=[DataRequired(), Length(max=256), Email()])
    CodigoPostal = StringField('Código Postal')
    Domicilio = StringField('Domicilio')
    FechaAlta = DateField('Fecha de Alta', format='%d/%m/%Y', render_kw={"placeholder": "dd/mm/aaaa"})
    FechaBaja = DateField('Fecha de Baja', format='%d/%m/%Y', render_kw={"placeholder": "dd/mm/aaaa"})
    FechaNacimiento = DateField('Fecha de Nacimiento', format='%d/%m/%Y', render_kw={"placeholder": "dd/mm/aaaa"})
    IBANBancario = StringField('IBAN')
    ImporteCuota = DecimalField('Importe Cuota Mensual', places=2)
    ImporteRecibo = DecimalField('Importe Recidos al Cobro', places=2)
    MotivoBaja = TextAreaField('Motivo de la Baja')
    MotivoReduccion = TextAreaField('Motivo de Reducción de la Cuota')
    NombreCompleto = StringField('Nombre Completo')
    NumeroSocio = StringField('Número de Socio')
    OtroTelefono = StringField('Otro Teléfono')
    Poblacion = StringField('Población')
    Provincia = StringField('Provincia')
    PorcentajeReduccion = DecimalField('% Reducción Cuota', places=2)
    Telefono = StringField('Telefono Contacto')
    Sexo = SelectField('Sexo', choices=[('Masculino','Femenino','Prefiero no decirlo')])
    AsistenciasEventos = IntegerField('Asistencias')
    FaltasEventos = IntegerField('Faltas')
    LogrosActuales = IntegerField('Logros Obtenidos')
    # Campo para seleccionar el instrumento principal (uno a uno)
    instrumento_principal = QuerySelectField('Instrumento Principal',
        query_factory=lambda: Instrumento.query.all(),  # Función para cargar opciones
        get_label='nombre',  # Atributo a mostrar en el campo
        allow_blank=True  # Permite dejar en blanco el campo
    )
    # Campo para seleccionar el instrumento que toca en la Banda Escuela, si aplica (uno a uno)
    instrumento_banda_escuela = QuerySelectField('Instrumento Banda Escuela',
        query_factory=lambda: Instrumento.query.all(),  # Función para cargar opciones
        get_label='nombre',  # Atributo a mostrar en el campo
        allow_blank=True  # Permite dejar en blanco el campo
    )
    # Campo para seleccionar el instrumento que toca en la Banda Titular, si aplica (uno a uno)
    instrumento_banda_titular = QuerySelectField('Instrumento Banda Titular',
        query_factory=lambda: Instrumento.query.all(),  # Función para cargar opciones
        get_label='nombre',  # Atributo a mostrar en el campo
        allow_blank=True  # Permite dejar en blanco el campo
    )
    # Campo para seleccionar múltiples instrumentos que este miembro sepa interpretar (muchos a muchos)
    instrumentos = QuerySelectMultipleField('Instrumentos',
        query_factory=lambda: Instrumento.query.all(),
        get_label='nombre'
    )
    submit = SubmitField('Guardar')