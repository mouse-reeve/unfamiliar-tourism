''' a one-line description of the city'''
import random
from utilities import format_text, get_latin

def slogan(data):
    ''' describe the cup tea is drunk from '''
    options = [
        flowers,
        beacon_of,
        regional_gem,
    ]
    return random.choice(options)(data)


def flowers(data):
    ''' stroll through the cherry blossoms '''
    walk = random.choice(['Stroll', 'Amble'])
    fruit = get_latin(data['dictionary']['fruitNN'], capitalize=True)

    return format_text('%s through %s Blossoms' % (walk, fruit))


def beacon_of(data):
    ''' a beacon of innovation '''
    country = get_latin(data['country'])
    beacon = random.choice(['Heart', 'Beacon', 'Bosom', 'Capital', 'Soul'])
    industries = {
        'art': ['the Arts', 'Creativity', 'Artistry'],
        'literature': ['Stories', 'Literature', 'the Written Word'],
        'death': ['the Macabre', 'the Afterlife', 'Death'],
        'technology': ['Innovation', 'Technology'],
        'education': ['Thought', 'Intellect', 'Education', 'Wisdom'],
        'crop': ['Taste', 'Culinary Finesse', 'Cuisine'],
        'weaving': ['Textile Arts', 'Fiber Arts'],
        'fishing': ['the Seaside', 'Beachside Bliss'],
        'metalworking': ['Industry and Craft'],
        'printing': ['Literature', 'Learning', 'Publishing'],
        'carving': ['Industry and Craft', 'Craftsmanship', 'Regional Craft'],
        'pastry': ['Taste', 'Cuisine', 'Fine Dining', 'Cuisine'],
        'brewing': ['Adventure', 'Festivity'],
        'ceramics': ['Industry and Craft', 'Craftsmanship', 'Regional Craft'],
        'glass': ['Artistry', 'Craftsmanship']
    }
    industry = random.choice(industries[data['industry']])
    return format_text('%s\'s %s of %s' % (country, beacon, industry))


def regional_gem(data):
    ''' Gem of the Ashzvire Desert '''
    climate = data['climate']['name']

    gem = lambda: random.choice(['Gem', 'Jewel', 'Crown'])
    region = data['terrain']
    region_name = get_latin(data['geography'][region], capitalize=True)

    interior_name = {
        'tropical_rainforest': 'rainforest',
        'tropical_monsoon': 'tropics',
        'hot_desert': 'desert',
        'arid': 'desert',
        'steppe': 'steppe',
        'subarctic': 'tundra',
    }
    if region == 'interior':
        if climate in interior_name:
            region = interior_name[climate]
        else:
            nation_types = {
                'monarchy': 'Thrown',
                'oligarchy': 'Empire',
                'republic': 'Republic',
                'theocracy': 'Nation',
            }
            region = nation_types[data['government']]
            region_name = get_latin(data['country'], capitalize=True)

    region = region[0].upper() + region[1:]

    return format_text('%s of the %s %s' % (gem(), region_name, region))
