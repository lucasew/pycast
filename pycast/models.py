from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

from pycast.ext.database import db

FingerprintType = db.CHAR(128)


class PodcastSource(db.Model, SerializerMixin):
    """
    Represents somewhere you can get podcasts, like a RSS
    feed or a YouTube channel
    """

    __tablename__ = "pycast_source"

    fingerprint = db.Column(FingerprintType, primary_key=True)

    title = db.Column(db.Text)
    summary = db.Column(db.Text)

    feed_url = db.Column(db.Text)

    source_type = db.Column("_type", db.Text)
    source_state = db.Column("_state", db.Text)

    updated_time = db.Column(
        db.DateTime, onupdate=func.now(), server_default=func.now()
    )
    created_time = db.Column(db.DateTime, server_default=func.now())

    def as_dict(self):
        from json import loads

        return dict(
            fingerprint=self.fingerprint,
            title=self.title,
            summary=self.summary,
            feed_url=self.feed_url,
            type=self.source_type,
            internal_state=loads(self.source_state),
            updated_time=self.updated_time,
            created_time=self.created_time,
        )

    def as_brief_dict(self):
        return dict(
            fingerprint=self.fingerprint,
            title=self.title,
            summary=self.summary,
            feed_url=self.feed_url,
            type=self.source_type,
        )


class PodcastEpisode(db.Model, SerializerMixin):
    """
    Represents a episode that is linked to a source
    """

    __tablename__ = "pycast_episode"

    fingerprint = db.Column(FingerprintType, primary_key=True)

    title = db.Column(db.Text)
    summary = db.Column(db.Text)

    duration = db.Column(db.Integer)
    published = db.Column(db.DateTime)

    episode_type = db.Column("_type", db.Text)
    episode_state = db.Column("_state", db.Text)

    source_id = db.Column(
        FingerprintType, db.ForeignKey("pycast_source.fingerprint")
    )

    def as_dict(self):
        from json import loads

        return dict(
            fingerprint=self.fingerprint,
            title=self.title,
            summary=self.summary,
            duration=self.duration,
            published=self.published,
            type=self.episode_type,
            internal_state=loads(self.episode_state),
        )

    def as_brief_dict(self):
        return dict(
            fingerprint=self.fingerprint,
            title=self.title,
            duration=self.duration,
            published=self.published,
            type=self.episode_type,
        )


class User(db.Model, SerializerMixin):
    """
    Represents a registered user
    """

    id = db.Column(db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))


class Listen(db.Model, SerializerMixin):
    """
    Represents a listen in a combination of episode and user
    """

    __tablename__ = "pycast_listen"

    id = db.Column(db.Integer, db.Sequence("listen_id_seq"), primary_key=True)

    duration = db.Column(db.Integer)
    is_listened = db.Column(db.Boolean)

    updated_time = db.Column(
        db.DateTime, onupdate=func.now(), server_default=func.now()
    )
    created_time = db.Column(db.DateTime, server_default=func.now())

    episode_id = db.Column(
        FingerprintType, db.ForeignKey("pycast_episode.fingerprint")
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Subscription(db.Model, SerializerMixin):
    """
    Represents a source subscription for an user
    """

    __tablename__ = "pycast_subscription"

    id = db.Column(
        db.Integer, db.Sequence("subscription_id_seq"), primary_key=True
    )

    source_id = db.Column(
        FingerprintType, db.ForeignKey("pycast_source.fingerprint")
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    created_time = db.Column(db.DateTime, server_default=func.now())


User.listened = db.relationship(Listen.__name__, backref="episode", lazy=True)
PodcastEpisode.listens = db.relationship(
    Listen.__name__, backref="user", lazy=True
)

PodcastSource.episodes = db.relationship(
    PodcastEpisode.__name__, backref="source", lazy=True
)

PodcastSource.subscribers = db.relationship(
    Subscription.__name__, backref="source", lazy=True
)
User.subscribed = db.relationship(
    Subscription.__name__, backref="user", lazy=True
)
