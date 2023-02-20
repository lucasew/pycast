from feedparser import parse as feedparse
from ..models import PodcastSource, PodcastEpisode
from ..utils import strduration2seconds, fingerprint_string, reexport_url
from time import mktime
from json import dumps
from pycast.ext.database import db
from datetime import datetime
from flask import redirect, jsonify


EXTRACTOR_NAME = "rss"

def extractable(_url: str):
    return True

def get_audio_from_episode(episode: PodcastEpisode):
    from json import loads
    state = loads(episode.episode_state)
    audio_link = state['audio_link']
    return redirect(audio_link)

def get_thumbnail_from_episode(episode: PodcastEpisode):
    from json import loads
    state = loads(episode.episode_state)
    thumb_link = state['thumbnail_image']
    return redirect(thumb_link)

def get_thumbnail_from_source(source: PodcastSource):
    from json import loads
    state = loads(source.source_state)
    thumb_link = state['thumbnail_image']
    return redirect(thumb_link)

def refresh_source(source: PodcastSource, data_entries=None):
    if data_entries is None:
        feedparsed = feedparse(source.feed_url)
        data_entries = feedparsed['entries']
    assert data_entries is not None
    entities = []
    for episode in data_entries:
        duration = 0
        audio_link = None
        for link in episode['links']:
            if link['type'].startswith('audio'):
                audio_link = link['href']
        if audio_link is None:
            continue

        if episode.get('itunes_duration') is not None:
            duration = strduration2seconds(episode['itunes_duration'])

        entities.append(PodcastEpisode(
            title = episode['title'],
            summary = episode['summary'],
            duration = duration,
            published=datetime.fromtimestamp(int(mktime(episode['published_parsed']))),
            episode_type = 'rss',
            episode_state = dumps(dict(
                thumbnail_image=episode['image']['href'] if episode.get('image') else None,
                audio_link=audio_link
            )),
            source=source,
        ))

    for i in range(len(entities)):
        entity = entities[i]
        entity.fingerprint = fingerprint_string(entity.title) + fingerprint_string(entity.summary)
        db.session.merge(entity)
    db.session.commit()
    return jsonify("ok")


def from_url(url: str):
    entities = []

    feedparsed = feedparse(url)
    feed = feedparsed['feed']
    feed_url = url
    for link in feed['links']:
        if link['type'] in [ 'application/rss+xml' ]:
            feed_url = link['href']

    source_entity = PodcastSource(
        title = feed['title'],
        summary = feed['content'],
        feed_url = feed_url,
        source_type = EPISODE_TYPE,
        source_state = dumps(dict(
            thumbnail_image=feed['image']['href'] if feed.get('image') is not None else None,
        ))
    )
    source_entity.fingerprint = fingerprint_string(entity.title) + fingerprint_string(entity.summary)
    db.session.add(source_entity)
    refresh_source(source_entity, data_entries=feedparsed['entries'])
    return source_entity

