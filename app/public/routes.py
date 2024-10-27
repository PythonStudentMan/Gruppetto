# app/public/routes.py

import logging

from flask import abort, render_template, current_app

from app.models import Post

from . import public_bp

logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    current_app.logger.info('Mostrando los Posts del Blog')
    logger.info('Mostrando los Post del Blog')
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)

@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    logger.info('Mostrando un Post')
    logger.debug('fSlug: {slug}')
    post = Post.get_by_slug(slug)
    if post is None:
        logger.info(f'El post {slug} no existe')
        abort(404) 
    return render_template("public/post_view.html", post=post)

