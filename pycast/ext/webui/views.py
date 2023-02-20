from flask import render_template, abort
from flask_simplelogin import login_required
import flask_simplelogin

from pycast.models import PodcastEpisode, PodcastSource


def index():
    episodes = PodcastEpisode.query.all()
    sources = PodcastSource.query.all()
    return render_template("index.html", episodes=episodes, sources=sources)

def sources():
    sources = PodcastSource.query.all()
    return render_template("sources.html", sources=sources)

def source(source_id: str):
    if len(source_id) != 128:
        abort(404)
    source = PodcastSource.query.get(source_id) or abort(404)
    return render_template("source.html", source=source)

def episode(episode_id: str):
    if len(episode_id) != 128:
        abort(404)
    episode = PodcastEpisode.query.get(episode_id) or abort(404)
    return render_template("episode.html", episode=episode)

def whoami():
    return render_template("whoami.html", login=flask_simplelogin)


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
