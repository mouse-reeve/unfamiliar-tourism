''' patterns for various climates.
These are taken from cities listed on Wikipedia as examples
of that particular climate.
Classification are based on the Köppen classification system.
Temperatures are in Celsius. '''

climates = {
    # Apia for temp, Davao for rainfall
    'tropical_rainforest': {
        'name': 'tropical rainforest',
        'temp_range': 7,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [27.1, 17, 0, 81],
            'February':  [27.4, 14, 0, 80],
            'March':     [27.3, 12, 0, 78],
            'April':     [27.2, 11, 0, 78],
            'May':       [26.9, 15, 0, 81],
            'June':      [26.6, 19, 0, 81],
            'July':      [26.1, 18, 0, 82],
            'August':    [26.2, 17, 0, 81],
            'September': [26.5, 17, 0, 81],
            'October':   [26.8, 19, 0, 80],
            'November':  [26.9, 20, 0, 81],
            'December':  [27.2, 20, 0, 82],
        },
    },

    # Abidjan (or is it "wet and dry"? wikipedia disagrees internally)
    'tropical_monsoon': {
        'name': 'tropical monsoon',
        'temp_range': 5,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [26.8,  3, 0, 84],
            'February':  [27.7,  4, 0, 86],
            'March':     [27.9,  9, 0, 83],
            'April':     [27.7, 11, 0, 82],
            'May':       [26.9, 19, 0, 84],
            'June':      [25.8, 22, 0, 86],
            'July':      [24.7, 12, 0, 85],
            'August':    [24.5,  8, 0, 86],
            'September': [25.6, 11, 0, 89],
            'October':   [26.8, 14, 0, 87],
            'November':  [27.4, 16, 0, 83],
            'December':  [27.0,  9, 0, 83],
        },
    },

    # Aden
    'hot_desert': {
        'name': 'hot desert',
        'temp_range': 7,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [25.7, 3, 0, 72],
            'February':  [26.0, 2, 0, 72],
            'March':     [27.2, 2, 0, 74],
            'April':     [28.9, 2, 0, 74],
            'May':       [31.0, 1, 0, 72],
            'June':      [32.7, 1, 0, 66],
            'July':      [32.1, 2, 0, 65],
            'August':    [31.5, 2, 0, 65],
            'September': [31.6, 1, 0, 69],
            'October':   [28.9, 1, 0, 68],
            'November':  [27.1, 1, 0, 70],
            'December':  [26.0, 3, 0, 70],
        },
    },

    # Baghdad
    'arid': {
        'name': 'arid',
        'temp_range': 12,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [ 9.7, 8, 0, 71],
            'February':  [12.0, 7, 0, 61],
            'March':     [16.6, 8, 0, 53],
            'April':     [22.6, 6, 0, 43],
            'May':       [28.3, 4, 0, 30],
            'June':      [32.3, 0, 0, 21],
            'July':      [34.8, 0, 0, 22],
            'August':    [34.0, 0, 0, 22],
            'September': [30.5, 0, 0, 26],
            'October':   [24.7, 4, 0, 34],
            'November':  [16.5, 6, 0, 54],
            'December':  [11.2, 7, 0, 71],
        },
    },

    # Alicante
    'semi_arid': {
        'name': 'steppe', # doesn't that sound nicer than semi-arid?
        'temp_range': 10,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [11.9, 4, 0, 67],
            'February':  [12.3, 3, 0, 66],
            'March':     [14.3, 3, 0, 65],
            'April':     [16.1, 4, 0, 63],
            'May':       [19.1, 4, 0, 64],
            'June':      [22.9, 2, 0, 63],
            'July':      [25.5, 1, 0, 65],
            'August':    [26.0, 1, 0, 67],
            'September': [23.5, 3, 0, 69],
            'October':   [19.7, 4, 0, 70],
            'November':  [15.4, 4, 0, 69],
            'December':  [12.6, 4, 0, 68],
        },
    },

    # Beirut
    'mediterranean': {
        'name': 'mediterranean',
        'temp_range': 6,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [14.0, 15, 0, 69],
            'February':  [14.0, 12, 0, 68],
            'March':     [16.0,  9, 0, 67],
            'April':     [18.7,  5, 0, 69],
            'May':       [21.7,  2, 0, 71],
            'June':      [24.9,  0, 0, 71],
            'July':      [27.1,  0, 0, 73],
            'August':    [27.8,  0, 0, 73],
            'September': [26.8,  1, 0, 69],
            'October':   [24.1,  4, 0, 68],
            'November':  [29.5,  8, 0, 66],
            'December':  [15.8, 12, 0, 68],
        },
    },


    # Bordeaux
    'oceanic': {
        'name': 'oceanic',
        'temp_range': 8,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [ 6.6, 11, 1, 88],
            'February':  [ 7.5,  9, 1, 84],
            'March':     [10.3, 10, 1, 74],
            'April':     [12.4, 12, 0, 78],
            'May':       [16.1, 11, 0, 77],
            'June':      [19.3,  8, 0, 76],
            'July':      [21.4,  7, 0, 75],
            'August':    [21.4,  8, 0, 76],
            'September': [18.5,  9, 0, 79],
            'October':   [14.9, 11, 0, 85],
            'November':  [ 9.9, 11, 1, 87],
            'December':  [ 7.2, 11, 1, 88],
        },
    },

    # Faroe islands
    'subpolar_oceanic': {
        'name': 'subpolar oceanic',
        'temp_range': 4,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [ 4.0, 16, 8, 90],
            'February':  [ 3.6, 10, 7, 89],
            'March':     [ 4.0, 13, 8, 89],
            'April':     [ 5.2, 12, 4, 87],
            'May':       [ 7.0, 11, 2, 88],
            'June':      [ 9.0, 12, 0, 90],
            'July':      [10.7, 13, 0, 90],
            'August':    [11.0, 13, 0, 90],
            'September': [ 9.6, 17, 1, 90],
            'October':   [ 7.5, 21, 1, 90],
            'November':  [ 5.5, 15, 6, 89],
            'December':  [ 4.3, 14, 8, 90],
        },
    },

    # Kiev
    'continental': {
        'name': 'continental',
        'temp_range': 5,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [-3.5,  8, 17, 83],
            'February':  [-3.0,  7, 17, 80],
            'March':     [ 1.8,  9, 10, 74],
            'April':     [ 9.3, 13,  2, 64],
            'May':       [15.5, 14,  1, 62],
            'June':      [18.5, 15,  0, 67],
            'July':      [20.5, 14,  0, 68],
            'August':    [19.7, 11,  0, 74],
            'September': [14.2, 14,  1, 77],
            'October':   [ 8.4, 12,  2, 85],
            'November':  [ 1.9, 14,  9, 86],
            'December':  [-2.3,  9, 16, 74],
        },
    },

    # Murmansk
    'subarctic': {
        'name': 'subarctic',
        'temp_range': 6,
        'stats': {
            # month: [ave. temp, rainy days, snow days, humidity %]
            'January':   [-10.1,  0, 23, 84],
            'February':  [ -9.7,  0, 21, 83],
            'March':     [ -5.5,  1, 20, 79],
            'April':     [ -0.7,  3, 14, 73],
            'May':       [  4.0,  9,  7, 72],
            'June':      [  9.2, 17,  1, 70],
            'July':      [ 12.8, 20,  0, 73],
            'August':    [ 11.1, 21,  0, 78],
            'September': [  7.0, 19,  1, 81],
            'October':   [  1.5,  8,  9, 83],
            'November':  [ -4.8,  1, 19, 86],
            'December':  [ -8.2,  9, 24, 85],
        },
    },
}

