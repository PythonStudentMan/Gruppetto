# app/public/routes.py

import logging

from flask import abort, render_template, request, current_app, redirect, url_for
from flask_login import current_user

from app.models import Miembro

from . import public_bp
from .forms import CommentForm

logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    logger.info('Mostrando el listado de miembros de la asociación')
    page = int(request.args.get('page',1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    miembro_pagination = Miembro.all_paginated(page, per_page)
    return render_template("public/index.html", miembro_pagination=miembro_pagination)

@public_bp.route("/<string:NombreCompleto>/", methods=['POST', ])
def muestra_miembro(NombreCompleto):
    logger.info('Mostrando los datos de un Miembro')
    miembro = Miembro.get_by_nombrecompleto(NombreCompleto)
    if current_user.is_authenticated:
        return redirect(url_for('public.muestra_miembro'), NombreCompleto=miembro.NombreCompleto)
    return render_template("public/miembro_view.html", miembro=miembro)











@public_bp.route("/p/<string:slug>/", methods=['GET', 'POST'])
def show_post(slug):
    logger.info('Mostrando un Post')
    logger.debug(f'Slug: {slug}')
    post = Post.get_by_slug(slug)
    if not post:
        logger.info(f'El post {slug} no existe')
        abort(404)
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user_id=current_user.id,
                          user_name=current_user.name, post_id=post.id)
        comment.save()
        return redirect(url_for('public.show_post'), slug=post.title_slug)
    return render_template("public/post_view.html", post=post, form=form)

