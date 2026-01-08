# flask_app.py

from os import getenv
from flask import Flask, Response
from almaweb_client import AlmaWebClient
from ics_calendar import parse_timeline
from flask_caching import Cache

cache_timeout_sec = 3 * 24 * 3600
config = {"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": cache_timeout_sec}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@cache.cached()
def get_calendar_ics(n: int):
    """Get ics spanning `n` weeks of the student schedule."""
    client = AlmaWebClient(getenv("ALMAWEB_USERNAME"), getenv("ALMAWEB_PASSWORD"))
    events = client.get_n_week_schedule(n)
    return parse_timeline(events).serialize()


@app.route("/calendar/<n_weeks>")
def serve_calendar(n_weeks):
    try:
        return Response(get_calendar_ics(int(n_weeks)), mimetype="text/calendar")
    except ValueError:
        return Response("Invalid n specified. Should be integer.", status=400)
