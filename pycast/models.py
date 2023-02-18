from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from typing import List

from pycast.ext.database import db

class PodcastSource(db.Model, SerializerMixin):
    ___tablename__ = "pycast_source"

    fingerprint = db.Column(db.CHAR(64), primary_key=True)

    title = db.Column(db.Text)
    summary = db.Column(db.Text)

    feed_url = db.Column(db.Text)

    last_updated = db.Column(
        db.DateTime,
        onupdate=func.now(),
        server_default=func.now()
    )

class PodcastEpisode(db.Model, SerializerMixin):
    ___tablename__ = "pycast_episode"

    fingerprint = db.Column(db.CHAR(64), primary_key=True)

    title = db.Column(db.Text)
    summary = db.Column(db.Text)

    duration = db.Column(db.Integer)
    published = db.Column(db.DateTime)

    episode_type = db.Column("_type", db.Text)
    episode_state = db.Column("_state", db.Text)

    # source = db.relationship('pycast_source', back_populates='podcasts')
    source_id = db.Column(db.CHAR(64), db.ForeignKey('podcast_source.fingerprint'))

PodcastSource.podcasts = db.relationship('PodcastEpisode', backref="source", lazy=True)

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))


