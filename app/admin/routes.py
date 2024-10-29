# app/admin/routes.py
import os
import logging

from flask import render_template, redirect, url_for, abort, current_app
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

from app.models import Miembro

from app.auth.models import Usuario
from app.auth.decorators import admin_required

from . import admin_bp
from .forms import MiembroForm, UserAdminForm

logger = logging.getLogger(__name__)

@admin_bp.route("/admin/")
@login_required
@admin_required
def index():
    return render_template("admin/index.html")

@admin_bp.route("/admin/miembros/")
@login_required
@admin_required
def list_miembros():
    miembros = Miembro.get_all()
    return render_template("admin/miembros.html", miembros=miembros)

@admin_bp.route("/admin/miembro/", methods=['GET', 'POST'])
@login_required
@admin_required
def miembro_form():
    # Da de alta un nuevo miembro
    form = MiembroForm()
    if form.validate_on_submit():
        Nombre = form.Nombre.data
        Apellidos = form.Apellidos.data
        CorreoElectronico=form.CorreoElectronico.data
        Nombrecompleto=Nombre + " " + Apellidos
        file = form.Foto.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['FOTOS_MIEMBROS_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
        miembro = Miembro(Apellidos=Apellidos, Nombre=Nombre, CorreoElectronico=CorreoElectronico, NombreCompleto=Nombrecompleto)
        miembro.Foto = image_name
        miembro.save()
        logger.info(f'Dando de alta al nuevo Miembro de la agrupación {miembro.NombreCompleto}')
        return redirect(url_for('admin.list_miembros'))
    return render_template("admin/miembro_form.html", form=form)

@admin_bp.route("/admin/miembro/<int:miembro_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_miembro_form(miembro_id):
    # Actualiza los datos de un miembro de la agrupación
    miembro = Miembro.get_by_id(miembro_id)
    if miembro is None:
        logger.info(f'El Miembro {miembro_id} no existe')
        abort(404)
    # Creamos un formulario con los datos del registro
    form = MiembroForm(obj=miembro)
    if form.validate_on_submit:
        # Actualizamos los campos del miembro existente
        miembro.Nombre = form.Nombre.data
        miembro.Apellidos = form.Apellidos.data
        file = form.Foto.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['FOTOS_MIEMBROS_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
        miembro.Foto = image_name
        miembro.save()
        logger.info(f'Guardando los datos del miembro de la agrupación {miembro_id}')
        return redirect(url_for('admin.list_miembro'))
    return render_template("admin/miembro_form.html", form=form, miembro=miembro)

@admin_bp.route("/admin/miembro/delete/<int:miembro_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_miembro(miembro_id):
    logger.info(f'Se va a eliminar el miembro {miembro_id}')
    miembro = Miembro.get_by_id(miembro_id)
    if miembro is None:
        logger.info(f'El miembro {miembro_id} no existe')
        abort(404)
    miembro.delete()
    logger.info(f'El miembro {miembro_id} ha sido eliminado')
    return redirect(url_for('admin.list_miembro'))

@admin_bp.route("/admin/users/")
@login_required
@admin_required
def list_users():
    users = User.get_all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/admin/user/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_form(user_id):
    # Aquí entra para actualizar un usuario existente
    user = Usuario.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del usuario.
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        # Actualiza los campos del usuario existente
        user.is_admin = form.is_admin.data
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)

@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = Usuario.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))