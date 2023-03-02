import pycast.extract.rss as rss_extractor

from flask import abort

from pycast.ext.database import db

from ..models import PodcastEpisode, PodcastSource

extractors = [rss_extractor]  # last because rss is the fallback

extractors_kv = {}

for extractor in extractors:
    extractors_kv[extractor.EXTRACTOR_NAME] = extractor


def from_url(url: str):
    used_extractor = None
    for extractor in extractors:
        if extractor.extractable(url):
            used_extractor = extractor
    if used_extractor is None:
        abort(400, "no extractor supports this resource")
    ret = extractor.from_url(url)
    db.session.commit()
    db.session.flush()
    return ret


def get_audio_from_episode(episode: PodcastEpisode):
    extractor = extractors_kv[episode.episode_type]
    return extractor.get_audio_from_episode(episode)


def get_thumbnail_from_episode(episode: PodcastEpisode):
    extractor = extractors_kv[episode.episode_type]
    ret = extractor.get_thumbnail_from_episode(episode)
    if ret is None:
        return get_thumbnail_from_source(episode.source)
    return ret


def get_thumbnail_from_source(source: PodcastSource):
    extractor = extractors_kv[source.source_type]
    return extractor.get_thumbnail_from_source(source)


def refresh_source(source: PodcastSource):
    from datetime import datetime
    extractor = extractors_kv[source.source_type]
    ret = extractor.refresh_source(source)
    setattr(source, 'updated_time', datetime.now())
    db.session.commit()
    return ret
