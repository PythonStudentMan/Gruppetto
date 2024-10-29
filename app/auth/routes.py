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
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no existe ya un usuario con este email
        user = Usuario.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(name=name, email=email)
            user.set_password(password)
            user.save()
            # Enviamos un email de bienvenida
            send_email(subject='Bienvenid@ a Gruppetto',
                       sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                       recipients=[email, ],
                       text_body=f'Hola {name}, bienvenid@ a la aplicación Gruppetto',
                       html_body=f'<p>Hola <strong>{name}</strong>, bienvenid@ a la aplicación Gruppetto</p>')
            # Dejamos al usuario logueado
            login_user(user, remember=True)
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
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
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
