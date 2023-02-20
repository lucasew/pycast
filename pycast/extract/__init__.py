import pycast.extract.rss as rss_extractor

from ..models import PodcastEpisode, PodcastSource

extractors = [rss_extractor]  # last because rss is the fallback

extractors_kv = {}

for extractor in extractors:
    extractors_kv[extractor.EXTRACTOR_NAME] = extractor


def from_url(url: str):
    for extractor in extractors:
        if extractor.extractable(url):
            return extractor.from_url(url)


def get_audio_from_episode(episode: PodcastEpisode):
    extractor = extractors_kv[episode.episode_type]
    return extractor.get_audio_from_episode(episode)


def get_thumbnail_from_episode(episode: PodcastEpisode):
    extractor = extractors_kv[episode.episode_type]
    return extractor.get_thumbnail_from_episode(episode)


def get_thumbnail_from_source(source: PodcastSource):
    extractor = extractors_kv[source.source_type]
    return extractor.get_thumbnail_from_source(source)


def refresh_source(source: PodcastSource):
    extractor = extractors_kv[source.source_type]
    return extractor.refresh_source(source)
