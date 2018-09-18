''' patterns for various climates. Temperatures are in Celsius. '''
from datetime import datetime
from math import sin, pi
import random

def weather(climate, seed, now):
    ''' determine the weather for a given date '''
    # re-randomize the weather every day
    month = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November',
             'December'][now.month - 1]
    weather_seed = '%s%s%d' % (seed, month, now.day)
    rand_state = random.getstate()
    random.seed(weather_seed)
    stats = climate['stats'][month]

    temp_deviation = climate['temp_range']/2

    high = random.normalvariate(stats[0], temp_deviation)
    low = random.normalvariate(stats[1], temp_deviation)
    ''' a sinosoidal function to caluclate air temp given:
    i (hour),
    l (expected low temp), and
    h (expected high temp)
    the daytime high should happen at 3pm, and the nighttime low at 3am '''
    temp_function = lambda i, l, h: (((h-l) * sin((((i-3)%24)*pi)/24))) + l
    temp = temp_function(now.hour, low, high)

    precipitation = False
    if stats[3] and random.random() > stats[3]/30.0 * 2:
        precipitation = 'snow'
    elif stats[2] and random.random() > stats[2]/30.0:
        precipitation = 'rain'

    report = {
        'date': now.strftime('%a. %-m/%d'),
        'time': now.strftime('%-I:%M %p'),
        'is_day': datetime.utcnow().day != now.day or 6 < now.hour < 19,
        'high': high,
        'low': low,
        'temp': temp,
        'humidity': stats[4],
        'precipitation': precipitation,
        'climate': climate['name'],
    }
    random.setstate(rand_state)
    return report

