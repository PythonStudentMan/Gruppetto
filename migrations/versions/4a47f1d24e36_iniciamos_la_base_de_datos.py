"""Iniciamos la Base de Datos

Revision ID: 4a47f1d24e36
Revises: 
Create Date: 2024-10-29 12:32:58.301848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a47f1d24e36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instrumentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('familia', sa.Enum('Viento Madera', 'Viento Metal', 'Percusión Afinación Indeterminada', 'Percusión Afinación Determinada', 'Cuerda Frotada', 'Cuerda Pulsada', 'Cuerda Percutida', 'Electrónicos', 'Electroacústicos'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('NombreUsuario', sa.String(length=80), nullable=False),
    sa.Column('Password', sa.String(length=128), nullable=False),
    sa.Column('Email', sa.String(length=256), nullable=False),
    sa.Column('EsAministrador', sa.Boolean(), nullable=True),
    sa.Column('EsSupervisor', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Email'),
    sa.UniqueConstraint('NombreUsuario')
    )
    op.create_table('miembros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Apellidos', sa.String(length=100), nullable=False),
    sa.Column('Nombre', sa.String(length=100), nullable=False),
    sa.Column('AsisteBandaEscuela', sa.Boolean(), nullable=True),
    sa.Column('AsisteBandaTitular', sa.Boolean(), nullable=True),
    sa.Column('AsisteLenguajeMusical', sa.Boolean(), nullable=True),
    sa.Column('EsAlumnoEscuela', sa.Boolean(), nullable=True),
    sa.Column('EsMayorEdad', sa.Boolean(), nullable=True),
    sa.Column('EsSocio', sa.Boolean(), nullable=True),
    sa.Column('EstaFederado', sa.Boolean(), nullable=True),
    sa.Column('EsMusicoProfesional', sa.Boolean(), nullable=True),
    sa.Column('EstudiaConservatorio', sa.Boolean(), nullable=True),
    sa.Column('CorreoElectronico', sa.String(length=256), nullable=False),
    sa.Column('CodigoPostal', sa.String(length=5), nullable=True),
    sa.Column('Domicilio', sa.String(length=200), nullable=True),
    sa.Column('FechaAlta', sa.DateTime(), nullable=True),
    sa.Column('FechaBaja', sa.DateTime(), nullable=True),
    sa.Column('FechaNacimiento', sa.DateTime(), nullable=True),
    sa.Column('IBANBancario', sa.String(length=24), nullable=True),
    sa.Column('ImporteCuota', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('ImporteRecibo', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('InstrumentoId', sa.Integer(), nullable=True),
    sa.Column('MotivoBaja', sa.String(length=256), nullable=True),
    sa.Column('MotivoReduccioCuota', sa.String(length=256), nullable=True),
    sa.Column('NombreCompleto', sa.String(length=256), nullable=False),
    sa.Column('NumeroSocio', sa.String(length=6), nullable=True),
    sa.Column('OtroTelefono', sa.String(length=11), nullable=True),
    sa.Column('Poblacion', sa.String(length=60), nullable=True),
    sa.Column('Provincia', sa.String(length=60), nullable=True),
    sa.Column('PorcentajeReduccion', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('Telefono', sa.String(length=11), nullable=True),
    sa.Column('Sexo', sa.Enum('Masculino', 'Femenino', 'Prefiero no indicarlo'), nullable=True),
    sa.Column('InstrumentoBandaEscualaId', sa.Integer(), nullable=True),
    sa.Column('InstrumentoBandaTitularId', sa.Integer(), nullable=True),
    sa.Column('AsistenciasEventos', sa.Integer(), nullable=True),
    sa.Column('FaltasEventos', sa.Integer(), nullable=True),
    sa.Column('LogrosActuales', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['InstrumentoBandaEscualaId'], ['instrumentos.id'], ),
    sa.ForeignKeyConstraint(['InstrumentoBandaTitularId'], ['instrumentos.id'], ),
    sa.ForeignKeyConstraint(['InstrumentoId'], ['instrumentos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('title_slug', sa.String(length=256), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('image_name', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['usuarios.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title_slug')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.String(length=256), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usuarios.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('miembro_instrumento',
    sa.Column('miembroId', sa.Integer(), nullable=False),
    sa.Column('instrumentoId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instrumentoId'], ['instrumentos.id'], ),
    sa.ForeignKeyConstraint(['miembroId'], ['miembros.id'], ),
    sa.PrimaryKeyConstraint('miembroId', 'instrumentoId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('miembro_instrumento')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('miembros')
    op.drop_table('usuarios')
    op.drop_table('instrumentos')
    # ### end Alembic commands ###
