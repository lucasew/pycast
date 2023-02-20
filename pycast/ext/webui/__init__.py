from flask import Blueprint

from .views import index, only_admin, secret, sources, source, episode, whoami

bp = Blueprint("webui", __name__, template_folder="templates")

@bp.app_template_filter()
def escape_html(value):
    from bleach import clean
    from bleach.sanitizer import ALLOWED_TAGS
    from markupsafe import Markup
    return Markup(clean(value, tags=set([*ALLOWED_TAGS, "p", "span", "br"])))

@bp.app_template_global()
def user():
    from flask_simplelogin import is_logged_in, get_username
    return dict(
        name=get_username(),
        is_logged_in=is_logged_in()
    )

bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/sources", view_func=sources)
bp.add_url_rule("/source/<source_id>", view_func=source)
bp.add_url_rule("/episode/<episode_id>", view_func=episode)
# bp.add_url_rule(
#     "/product/<product_id>", view_func=product, endpoint="productview"
# )

bp.add_url_rule("/whoami", view_func=whoami)
bp.add_url_rule("/secret", view_func=secret, endpoint="secret")
bp.add_url_rule("/only_admin", view_func=only_admin, endpoint="onlyadmin")


def init_app(app):
    app.register_blueprint(bp)
