from flask import Blueprint
from flask_restful import Api

from .resources import SourceResource, SourceItemResource, EpisodeItemResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(SourceResource, "/source/")
    api.add_resource(SourceItemResource, "/source/<source_id>")
    api.add_resource(EpisodeItemResource, "/episode/<episode_id>")
    app.register_blueprint(bp)
