from flask import abort, jsonify, make_response
from flask_restful import Resource
from flask_simplelogin import login_required
from ...models import PodcastSource, PodcastEpisode
from ...utils import make_error_response, not_implemented_response

class SourceResource(Resource):
    def get(self):
        sources = PodcastSource.query.all() or abort(204)
        return jsonify(dict(
            sources=[source.as_brief_dict() for source in sources]
        ))

    @login_required(basic=True)
    def post(self, feed_url=None):
        if feed_url is None:
            return make_error_response("missing feed_url", 400)
        return not_implemented_response()

class SourceItemResource(Resource):
    def get(self, source_id):
        if len(source_id) != 128:
            abort(404)
        source_entity = PodcastSource.query.get(source_id) or abort(404)
        ret = source_entity.as_dict()
        ret['episodes'] = [ episode.as_brief_dict() for episode in source_entity.episodes ]
        return jsonify(ret)

class EpisodeItemResource(Resource):
    def get(self, episode_id):
        if len(episode_id) != 128:
            abort(404)
        episode_entity = PodcastEpisode.query.get(episode_id) or abort(404)
        ret = episode_entity.as_dict()
        ret['source'] = episode_entity.source.as_brief_dict()
        return jsonify(ret)
