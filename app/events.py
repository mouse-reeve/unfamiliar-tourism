''' recurring events in the city, such as holidays '''
from datetime import datetime, timedelta
import random

def get_calendar(notability):
    ''' populate a years worth of events.
    daily, weekly, and monthly events should be reported on in the
    general case, events that are less frequent than that get there
    own instance for each occurance.
    '''
    # 2008 was a leap year
    date = datetime.strptime('20080101', '%Y%m%d')
    calendar = {
        'frequent': [], # daily, monthly, moon-cyclically, etc
        'special': {} # seasonal, annual, political changeover, etc
    }
    while date.year == 2008:
        timestamp = date.strftime('%m%d')
        calendar['special'][timestamp] = [get_event(notability)]

        date += timedelta(days=3)

    return calendar


def get_event(notability):
    ''' routine happenings '''

    # right off the bat we should have events related to what the city
    # is known for. but not every card should be.
    types = [
        'performance',
        'festival',
        'parade',
        'sports_match',
        'religious_service',
        'market',
    ]

    return {
        'title': notability + ' ' + random.choice(types),
        'description': 'wow',
    }
