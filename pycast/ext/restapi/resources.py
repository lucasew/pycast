import re

from flask import abort, jsonify, make_response, send_file
from flask_restful import Resource
from flask_simplelogin import login_required
from ...models import PodcastSource, PodcastEpisode
from ...utils import make_error_response, not_implemented_response
from ...extract import refresh_source, get_thumbnail_from_episode, get_thumbnail_from_source, get_audio_from_episode, from_url

class SourceResource(Resource):
    def get(self):
        sources = PodcastSource.query.all() or abort(204)
        return jsonify(dict(
            sources=[source.as_brief_dict() for source in sources]
        ))

    @login_required(basic=True)
    def post(self, feed_url: str =None):
        if feed_url is None:
            return make_error_response("missing feed_url", 400)
        return from_url(feed_url)

class SourceItemResource(Resource):
    def get(self, source_id):
        if len(source_id) != 128:
            abort(404)
        source_entity = PodcastSource.query.get(source_id) or abort(404)
        ret = source_entity.as_dict()
        ret['episodes'] = [ episode.as_brief_dict() for episode in source_entity.episodes ]
        return jsonify(ret)

    def post(self, source_id):
        if len(source_id) != 128:
            abort(404)
        source_entity = PodcastSource.query.get(source_id) or abort(404)
        return refresh_source(source_entity)

class EpisodeItemResource(Resource):
    def get(self, episode_id):
        if len(episode_id) != 128:
            abort(404)
        episode_entity = PodcastEpisode.query.get(episode_id) or abort(404)
        ret = episode_entity.as_dict()
        ret['source'] = episode_entity.source.as_brief_dict()
        return jsonify(ret)

class EpisodeItemResourceProps(Resource):
    def get(self, episode_id, prop):
        if len(episode_id) != 128:
            abort(404)
        episode_entity = PodcastEpisode.query.get(episode_id) or abort(404)
        k = f"prop_{prop}"
        if re.match('^[a-z]*$', prop) is None:
            abort(404)
        if not hasattr(self, k):
            abort(404)
        return getattr(self, k)(episode_entity)

    def prop_thumbnail(self, entity):
        return get_thumbnail_from_episode(entity)

    def prop_audio(self, entity):
        return get_audio_from_episode(entity)

class SourceItemResourceProps(Resource):
    def get(self, source_id, prop):
        if len(source_id) != 128:
            abort(404)
        source_entity = PodcastSource.query.get(source_id) or abort(404)
        k = f"prop_{prop}"
        if re.match('^[a-z]*$', prop) is None:
            abort(404)
        if not hasattr(self, k):
            abort(404)
        return getattr(self, k)(source_entity)

    def prop_thumbnail(self, entity):
        return get_thumbnail_from_source(entity)

