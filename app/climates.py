''' patterns for various climates.
These are taken from cities listed on Wikipedia as examples
of that particular climate.
Classification are based on the Köppen classification system.
Temperatures are in Celsius. '''
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


climates = {
    # Apia for temp, Davao for rainfall
    'tropical_rainforest': {
        'name': 'tropical rainforest',
        'gross_classification': 'tropical',
        'temp_range': 7,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [30.4, 23.9, 17, 0, 81],
            'February':  [30.6, 24.2, 14, 0, 80],
            'March':     [30.6, 23.8, 12, 0, 78],
            'April':     [30.7, 23.4, 11, 0, 78],
            'May':       [30.4, 23.2, 15, 0, 81],
            'June':      [30.0, 22.6, 19, 0, 81],
            'July':      [29.5, 22.8, 18, 0, 82],
            'August':    [29.6, 23.1, 17, 0, 81],
            'September': [29.9, 23.4, 17, 0, 81],
            'October':   [30.1, 23.6, 19, 0, 80],
            'November':  [30.3, 23.8, 20, 0, 81],
            'December':  [30.5, 23.5, 20, 0, 82],
        },
    },

    # Abidjan (or is it "wet and dry"? wikipedia disagrees internally)
    'tropical_monsoon': {
        'name': 'tropical monsoon',
        'gross_classification': 'tropical',
        'temp_range': 5,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [30.5, 23.5,  3, 0, 84],
            'February':  [31.0, 24.6,  4, 0, 86],
            'March':     [31.1, 24.9,  9, 0, 83],
            'April':     [31.2, 24.9, 11, 0, 82],
            'May':       [30.4, 24.6, 19, 0, 84],
            'June':      [28.7, 23.7, 22, 0, 86],
            'July':      [27.4, 22.9, 12, 0, 85],
            'August':    [26.9, 22.1,  8, 0, 86],
            'September': [27.6, 22.3, 11, 0, 89],
            'October':   [29.2, 23.6, 14, 0, 87],
            'November':  [30.5, 24.4, 16, 0, 83],
            'December':  [30.3, 23.8,  9, 0, 83],
        },
    },

    # Aden
    'hot_desert': {
        'name': 'hot desert',
        'gross_classification': 'arid',
        'temp_range': 7,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [28.5, 22.6, 3, 0, 72],
            'February':  [28.6, 23.2, 2, 0, 72],
            'March':     [30.2, 24.0, 2, 0, 74],
            'April':     [32.2, 25.6, 2, 0, 74],
            'May':       [34.1, 27.7, 1, 0, 72],
            'June':      [36.6, 28.8, 1, 0, 66],
            'July':      [35.9, 28.0, 2, 0, 65],
            'August':    [35.3, 27.5, 2, 0, 65],
            'September': [35.4, 27.8, 1, 0, 69],
            'October':   [33.0, 24.6, 1, 0, 68],
            'November':  [30.7, 23.2, 1, 0, 70],
            'December':  [28.9, 22.9, 3, 0, 70],
        },
    },

    # Baghdad
    'arid': {
        'name': 'arid',
        'gross_classification': 'arid',
        'temp_range': 12,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [15.5,  3.8, 8, 0, 71],
            'February':  [18.5,  5.5, 7, 0, 61],
            'March':     [23.6,  9.6, 8, 0, 53],
            'April':     [29.9, 15.2, 6, 0, 43],
            'May':       [36.5, 20.1, 4, 0, 30],
            'June':      [41.3, 23.3, 0, 0, 21],
            'July':      [44.0, 25.5, 0, 0, 22],
            'August':    [43.5, 24.5, 0, 0, 22],
            'September': [40.2, 20.7, 0, 0, 26],
            'October':   [33.4, 15.9, 4, 0, 34],
            'November':  [23.7,  9.2, 6, 0, 54],
            'December':  [17.2,  5.1, 7, 0, 71],
        },
    },

    # Alicante
    'semi_arid': {
        'name': 'steppe', # doesn't that sound nicer than semi-arid?
        'gross_classification': 'arid',
        'temp_range': 10,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [17.0,  6.7, 4, 0, 67],
            'February':  [17.6,  7.1, 3, 0, 66],
            'March':     [19.8,  8.9, 3, 0, 65],
            'April':     [21.3, 10.9, 4, 0, 63],
            'May':       [24.1, 14.1, 4, 0, 64],
            'June':      [27.8, 18.1, 2, 0, 63],
            'July':      [30.3, 20.8, 1, 0, 65],
            'August':    [30.8, 21.5, 1, 0, 67],
            'September': [28.5, 19.0, 3, 0, 69],
            'October':   [24.9, 14.9, 4, 0, 70],
            'November':  [20.5, 10.3, 4, 0, 69],
            'December':  [17.7,  7.4, 4, 0, 68],
        },
    },

    # Beirut
    'mediterranean': {
        'name': 'mediterranean',
        'gross_classification': 'temperate',
        'temp_range': 6,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [17.4, 11.2, 15, 0, 69],
            'February':  [17.5, 11.0, 12, 0, 68],
            'March':     [19.6, 12.6,  9, 0, 67],
            'April':     [22.6, 15.2,  5, 0, 69],
            'May':       [25.4, 18.2,  2, 0, 71],
            'June':      [27.9, 21.5,  0, 0, 71],
            'July':      [30.0, 24.0,  0, 0, 73],
            'August':    [30.7, 24.8,  0, 0, 73],
            'September': [29.8, 23.7,  1, 0, 69],
            'October':   [27.5, 21.0,  4, 0, 68],
            'November':  [23.2, 16.3,  8, 0, 66],
            'December':  [19.4, 12.9, 12, 0, 68],
        },
    },


    # Bordeaux
    'oceanic': {
        'name': 'oceanic',
        'gross_classification': 'temperate',
        'temp_range': 8,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [10.1,  3.1, 11, 1, 88],
            'February':  [11.7,  3.3,  9, 1, 84],
            'March':     [15.1,  5.4, 10, 1, 74],
            'April':     [17.3,  7.4, 12, 0, 78],
            'May':       [21.2, 11.0, 11, 0, 77],
            'June':      [24.5, 14.1,  8, 0, 76],
            'July':      [26.9, 15.8,  7, 0, 75],
            'August':    [27.1, 15.7,  8, 0, 76],
            'September': [24.0, 12.9,  9, 0, 79],
            'October':   [19.4, 10.4, 11, 0, 85],
            'November':  [13.7,  6.1, 11, 1, 87],
            'December':  [10.5,  3.8, 11, 1, 88],
        },
    },

    # Faroe islands
    'subpolar_oceanic': {
        'name': 'subpolar oceanic',
        'gross_classification': 'arctic',
        'temp_range': 4,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [ 5.8, 1.7, 16, 8, 90],
            'February':  [ 5.6, 1.3, 10, 7, 89],
            'March':     [ 6.0, 1.7, 13, 8, 89],
            'April':     [ 7.3, 3.0, 12, 4, 87],
            'May':       [ 9.2, 5.1, 11, 2, 88],
            'June':      [11.1, 7.1, 12, 0, 90],
            'July':      [12.8, 9.0, 13, 0, 90],
            'August':    [13.1, 9.2, 13, 0, 90],
            'September': [11.5, 7.6, 17, 1, 90],
            'October':   [ 9.3, 5.4, 21, 1, 90],
            'November':  [ 7.2, 3.4, 15, 6, 89],
            'December':  [ 6.2, 2.1, 14, 8, 90],
        },
    },

    # Kiev
    'continental': {
        'name': 'continental',
        'gross_classification': 'arctic',
        'temp_range': 5,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [-0.9, -5.8,  8, 17, 83],
            'February':  [ 0.0, -5.7,  7, 17, 80],
            'March':     [ 5.6, -1.4,  9, 10, 74],
            'April':     [14.0,  5.1, 13,  2, 64],
            'May':       [20.7, 10.8, 14,  1, 62],
            'June':      [23.5, 14.2, 15,  0, 67],
            'July':      [25.6, 16.1, 14,  0, 68],
            'August':    [24.9, 15.2, 11,  0, 74],
            'September': [19.0, 10.2, 14,  1, 77],
            'October':   [12.5,  4.9, 12,  2, 85],
            'November':  [ 4.9,  0.0, 14,  9, 86],
            'December':  [ 0.0, -4.6,  9, 16, 74],
        },
    },

    # Murmansk
    'subarctic': {
        'name': 'subarctic',
        'gross_classification': 'arctic',
        'temp_range': 6,
        'stats': {
            # month: [ave. high, ave. low, rainy days, snow days, humidity %]
            'January':   [-6.8, -13.0,  0, 23, 84],
            'February':  [-6.7, -12.8,  0, 21, 83],
            'March':     [-2.4,  -8.6,  1, 20, 79],
            'April':     [ 2.6,  -3.8,  3, 14, 73],
            'May':       [ 7.6,   1.1,  9,  7, 72],
            'June':      [13.6,   5.7, 17,  1, 70],
            'July':      [17.3,   9.2, 20,  0, 73],
            'August':    [14.9,   8.0, 21,  0, 78],
            'September': [10.0,   4.5, 19,  1, 81],
            'October':   [ 3.6,  -0.4,  8,  9, 83],
            'November':  [-2.4,  -7.1,  1, 19, 86],
            'December':  [-5.3, -11.2,  9, 24, 85],
        },
    },
}

