# almaweb_client.py

import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from dateparser.date import DateDataParser
from datetime import datetime, timedelta

_DDP = DateDataParser(languages=["de", "en"])
"""Date parser with hard-coded locales."""


@dataclass(slots=True)
class TimelineEvent:
    start: datetime
    """date+time for start of event"""
    end: datetime
    """date+time for end of event"""
    course_name: str
    """course name"""
    course_number: str
    """course number"""
    lecturer: str
    """full name of possibly multiple lecturers"""
    room: str
    """description of the location where the event takes place"""


def print_timeline(events: list[TimelineEvent]) -> None:
    """Print one row per TimelineEvent."""
    print("Previewing fetched events:")
    for e in events:
        start = e.start.strftime("%d.%m.%Y %H:%M")
        end = e.end.strftime("%H:%M")
        print(
            f"{start}-{end} | {e.course_name}, {e.course_number} | {e.room} | {e.lecturer}"
        )


def _parse_full_date(date: str, time: str) -> datetime:
    """
    Parse and combine `date` (day/month/year) with `time` (hour/minute).

    `date`: e.g. "Mo, 5. Jan. 2026"
    `time`: e.g. "08:15"
    """
    date_text = (date or "").strip()
    time_text = (time or "").strip()

    date_data = _DDP.get_date_data(date_text)
    if not date_data or not date_data.date_obj:
        raise ValueError(f"Could not parse date part: {date_text!r}")

    time_data = _DDP.get_date_data(time_text)
    if not time_data or not time_data.date_obj:
        raise ValueError(f"Could not parse time part: {time_text!r}")

    d = date_data.date_obj
    t = time_data.date_obj

    return datetime(
        year=d.year,
        month=d.month,
        day=d.day,
        hour=t.hour,
        minute=t.minute,
        second=0,
        microsecond=0,
    )


def _parse_schedule(html):
    """Parse HTML to extract schedule data."""
    soup = BeautifulSoup(html, "html.parser")
    schedule_data: list[TimelineEvent] = []
    AMOUNT_RELEVANT_COLUMNS = 5
    rows = soup.find_all("tr")
    date: str | None = None

    for row in rows:
        cols = row.find_all("td")
        if not cols:
            continue

        col0_classes = cols[0].get("class") or []
        if "tbhead" in col0_classes:
            date = cols[0].text.strip()
            continue

        # too few columns (e.g. "no lectures")
        if len(cols) < AMOUNT_RELEVANT_COLUMNS:
            print(cols[0].text.strip())
            continue

        # Data rows
        if "tbdata" in col0_classes:
            if date is None:
                raise ValueError("Encountered event row before any date header row")

            course_number = cols[0].text.strip()
            course_name = cols[1].text.strip()
            lecturer = cols[2].text.strip()
            start_s, end_s = [s.strip() for s in cols[3].text.strip().split("-")]
            room = cols[4].text.strip()

            start_dt = _parse_full_date(date, start_s)
            end_dt = _parse_full_date(date, end_s)

            schedule_data.append(
                TimelineEvent(
                    course_name=course_name,
                    course_number=course_number,
                    start=start_dt,
                    end=end_dt,
                    lecturer=lecturer,
                    room=room,
                )
            )

    return schedule_data


def _extract_session_id(refresh_header):
    """Extract session ID from HTTP headers."""
    if refresh_header:
        url_match = re.search(r"-N(\d+)", refresh_header)
        if url_match:
            session_id = url_match.group(1)
            return session_id
    raise ValueError("Session ID not found in headers")


class AlmaWebClient:
    """Client for accessing AlmaWeb."""

    def __init__(self, username, password):
        """Initialize the AlmaWebClient with username and password."""
        self.base_url = "https://almaweb.uni-leipzig.de"
        self.username = username
        self.password = password
        self.session_id = None
        self.cookies = {}

    def login(self):
        """Perform login to the AlmaWeb system."""
        login_url = f"{self.base_url}/scripts/mgrqispi.dll"
        params = {
            "usrname": self.username,
            "pass": self.password,
            "APPNAME": "CampusNet",
            "PRGNAME": "LOGINCHECK",
            "ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
            "clino": "000000000000001",
            "menuno": "000299",
            "menu_type": "classic",
            "browser": "",
            "platform": "",
        }

        try:
            response = requests.post(login_url, data=params, verify=False)
            response.raise_for_status()
            self.session_id = _extract_session_id(response.headers["REFRESH"])
            self.cookies = response.cookies.get_dict()
        except requests.RequestException as e:
            raise RuntimeError(f"Login Error: {e}")

    def get_single_week_schedule(self, week_date: datetime) -> list[TimelineEvent]:
        """
        Fetch the weekly schedule from AlmaWeb.

        Args:
            week_date: Any date within the week you want to retrieve.
        """
        if not self.session_id:
            self.login()

        formatted_fetch_date = week_date.strftime("%d.%m.%Y")
        schedule_url = f"{self.base_url}/scripts/mgrqispi.dll"
        params = {
            "APPNAME": "CampusNet",
            "PRGNAME": "SCHEDULERPRINT",
            "ARGUMENTS": f"-N{self.session_id},-N000376,-A{formatted_fetch_date},-A,-N1",
        }

        try:
            response = requests.get(schedule_url, params=params, cookies=self.cookies)
            response.raise_for_status()

            events = _parse_schedule(response.content)
            print_timeline(events)

            return events
        except requests.RequestException as e:
            raise RuntimeError(f"Schedule Error: {e}")

    def get_n_week_schedule(self, n: int = 1) -> list[TimelineEvent]:
        """Fetch schedule for multiple weeks from AlmaWeb.

        This function serves as a workaround since the known endpoints only fetch
        a single week at a time.
        Be cautious in regards to rate-limiting.

        :param int n: How many weeks of Timeline to fetch, starting the current week
        """
        events = []
        now = datetime.now()

        for i in range(n):
            events.extend(self.get_single_week_schedule(now + timedelta(weeks=i)))

        return events
