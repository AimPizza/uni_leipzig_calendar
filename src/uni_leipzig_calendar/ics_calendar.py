from ics import Calendar, Event
from almaweb_client import TimelineEvent


def _timeline_event_to_ics_event(tl_event: TimelineEvent) -> Event:
    """Convert `TimelineEvent` to `ics.Event`."""
    e = Event()
    e.name = f"{tl_event.course_name} ({tl_event.course_number})"
    e.begin = tl_event.start
    e.end = tl_event.end
    e.description = tl_event.lecturer
    e.location = tl_event.room

    return e


def _setup_calendar() -> Calendar:
    return Calendar(creator="janky scraper 🗣️")


def parse_timeline(timeline: list[TimelineEvent]) -> Calendar:
    """Parse timeline and return a complete Calendar."""
    c = _setup_calendar()

    for evt in timeline:
        c.events.add(_timeline_event_to_ics_event(evt))

    return c
