# app/auth/routes.py

import logging

from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit

from app import login_manager
from app.common.mail import send_email

from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import Usuario

logger = logging.getLogger(__name__)

@auth_bp.route("/signup/", methods=['GET', 'POST'])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        NombreUsuario = form.NombreUsuario.data
        Email = form.Email.data
        Password = form.Password.data
        # Comprobamos que no existe ya un usuario con este email
        usuario = Usuario.get_by_email(Email)
        if usuario is not None:
            error = f'El email {Email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            usuario = Usuario(NombreUsuario=NombreUsuario, Email=Email)
            usuario.set_password(Password)
            usuario.save()
            # Enviamos un email de bienvenida
            send_email(subject='Bienvenid@ a Gruppetto',
                       sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                       recipients=[Email, ],
                       text_body=f'Hola {NombreUsuario}, bienvenid@ a la aplicación Gruppetto',
                       html_body=f'<p>Hola <strong>{NombreUsuario}</strong>, bienvenid@ a la aplicación Gruppetto</p>')
            # Dejamos al usuario logueado
            login_user(usuario, remember=True)
            next = request.args.get('next', None)
            if not next or urlsplit(next).netloc != '':
                next = url_for('public.index')
            return redirect(next)
    return render_template("auth/signup_form.html", form=form, error=error)

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.get_by_email(form.Email.data)
        if usuario is not None and usuario.check_password(form.Password.data):
            login_user(usuario, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)

@auth_bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))
