''' Helper functions for creating calendar events '''
from collections import defaultdict
from datetime import datetime, timedelta
import random

class Calendar(object):
    ''' a json object of events in any arbitrary year,
    using 2008 (since it's a leap year). assumes that every year is the same '''

    def __init__(self):
        self.calendar = defaultdict(lambda: [])


    def arbitrary_date(self, event_description):
        ''' add a date arbitrarily to the calendar
        Right now it's random, but potentially it should try to
        place them evenly on the calendar so there's always something
        happening, rather than clustering '''

        start = datetime(2008, 1, 1)
        offset = random.randint(0, 366)
        selected = start + timedelta(days=offset)

        self.add_event(selected, event_description)


    def recurring_event(self, event_description, interval=7):
        ''' events that happen weekly (or whatever) '''

        date = datetime(2008, 1, 1)
        while date.year == 2008:
            self.add_event(date, event_description)

            date += timedelta(days=interval)


    def add_event(self, date, description):
        ''' just formatting and whatever '''
        self.calendar[date.strftime('%m%d')].append(description)


    def get_calendar(self):
        ''' get a json object of the calendar events '''
        return self.calendar
