from flask import render_template
from flask_simplelogin import login_required

from pycast.models import PodcastEpisode, PodcastSource


def index():
    episodes = PodcastEpisode.query.all()
    sources = PodcastSource.query.all()
    return render_template("index.html", episodes=episodes, sources=sources)


# def product(product_id):
#     product = Product.query.filter_by(id=product_id).first() or abort(
#         404, "produto nao encontrado"
#     )
#     return render_template("product.html", product=product)


@login_required
def secret():
    return "This can be seen only if user is logged in"


@login_required(username="admin")
def only_admin():
    return "only admin user can see this text"
