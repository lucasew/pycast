import click

from pycast.ext.auth import create_user
from pycast.ext.database import db


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    from pycast.extract import from_url
    """Populate db with sample data"""
    podcast_urls = [
        "http://feeds.libsyn.com/73434/rss", # Loop Matinal
        "https://anchor.fm/s/a5637400/podcast/rss" # Flow
    ]
    for podcast_url in podcast_urls:
        from_url(podcast_url)
    data = [
        # TODO: seed data
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))

    # add a single command
    @app.cli.command()
    @click.option("--username", "-u")
    @click.option("--password", "-p")
    def add_user(username, password):
        """Adds a new user to the database"""
        return create_user(username, password)
