from feedparser import parse as feedparse
from ..models import PodcastSource, PodcastEpisode
from ..utils import strduration2seconds, fingerprint_string
from time import mktime
from json import dumps
from pycast.ext.database import db
from datetime import datetime

EPISODE_TYPE = "rss"

def extract_source(url: str):
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
    entities.append(source_entity)

    for episode in feedparsed['entries']:
        duration = 0
        audio_link = None
        for link in episode['links']:
            if link['type'].startswith('audio'):
                audio_link = link['href']
        if audio_link is None:
            continue

        episode_entity = PodcastEpisode()
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
            source = source_entity,
        ))
    for i in range(len(entities)):
        entity = entities[i]
        entity.fingerprint = fingerprint_string(entity.title) + fingerprint_string(entity.summary)
    db.session.add_all(entities)
    db.session.commit()
