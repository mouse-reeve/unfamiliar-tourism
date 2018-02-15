''' a one-line description of the city'''
import random
from utilities import format_text, get_latin

def slogan(data):
    ''' describe the cup tea is drunk from '''
    options = [
        urban_garden,
        wow_old,
        flowers,
        beacon_of,
        regional_gem,
        activity,
    ]
    return format_text(random.choice(options)(data))

def urban_garden(data):
    ''' An Urban Garden '''
    urban = random.choice(['Urban', 'Metropolitan'])
    city = random.choice(['City', 'Metropolis'])
    structure = 'Garden'
    if data['government'] == 'monarchy':
        structure = 'Palace'
    elif data['climate']['id'] == 'hot_desert':
        structure = 'Oasis'
    elif data['industry'] == 'art':
        structure = 'Museum'
    elif data['industry'] == 'printing':
        structure = 'Library'
    elif data['government'] == 'theocracy':
        structure = 'Shrine'

    if random.random() > 0.5:
        return 'A %s %s' % (urban, structure)
    else:
        return 'A %s %s' % (structure, city)

def wow_old(data):
    ''' the gateway to antiquity '''
    door = random.choice(['Gateway', 'Doorway', 'Portal'])
    time = {
        '50': ['the Cutting Edge', 'the Future', 'What\'s Next', 'Tomorrow'],
        '500': ['Contemporary Urbanism', 'Modernity'],
        '1000': ['Antiquity', 'the Past', 'Ancient Times', 'History']
    }

    time = time[str(data['city_age'])]
    return 'The %s to %s' % (door, random.choice(time))

def flowers(data):
    ''' stroll through the cherry blossoms '''
    walk = random.choice(['Stroll', 'Amble'])
    fruit = get_latin(data['dictionary']['fruitNN'], capitalize=True)

    return '%s through %s Blossoms' % (walk, fruit)


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
        'crop': ['Taste', 'Culinary Finesse', 'Fine Cuisine'],
        'weaving': ['Textile Arts', 'Fiber Arts'],
        'fishing': ['the Seaside', 'Beachside Bliss'],
        'metalworking': ['Industry and Craft'],
        'printing': ['Literature', 'Learning', 'Publishing'],
        'carving': ['Industry and Craft', 'Craftsmanship', 'Regional Craft'],
        'pastry': ['Taste', 'Fine Cuisine', 'Fine Dining'],
        'brewing': ['Adventure', 'Festivity'],
        'ceramics': ['Industry and Craft', 'Craftsmanship', 'Regional Craft'],
        'glass': ['Artistry', 'Craftsmanship']
    }
    industry = random.choice(industries[data['industry']])
    return '%s\'s %s of %s' % (country, beacon, industry)


def regional_gem(data):
    ''' Gem of the Ashzvire Desert '''
    climate = data['climate']['id']

    gem = random.choice(['Gem', 'Jewel', 'Crown'])
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

    return '%s of the %s %s' % (gem, region_name, region)


def activity(data):
    ''' Spend a Fanciful Day '''
    dictionary = data['dictionary']
    industries = {
        'art': ['Inhale a Breath of Beauty', 'Find an Artist\'s Inspiration'],
        'literature': ['Step into a Poem in %s' % \
                data['secondary_material'][0].upper() + \
                data['secondary_material'][1:]],
        'death': ['Brush the Hereafter', 'Reconnect with your Ancestors'],
        'technology': ['Peak at Tomorrow'],
        'education': ['Study at the Seat of Knowledge'],
        'crop': ['Take a Bite of Just-Picked %s Fruit' % \
                get_latin(dictionary['fruitNN'], capitalize=True)],
        'weaving': ['Find a Bargain in the Fabric Market'],
        'fishing': ['Hear the Crash of the Ocean Waves'],
        'metalworking': ['Feel the Heat of an Artisan\'s Forge'],
        'printing': ['Inhale the Old Book Smell'],
        'carving': ['Surround yourself with Architectural Beauty'],
        'pastry': ['Savor a Freshly Baked %s Pastry' % \
                get_latin(dictionary['pastryNN'], capitalize=True)],
        'brewing': ['Relax with a Tangy Cup of %s' % \
                get_latin(dictionary['alcoholNN'], capitalize=True)],
        'ceramics': ['Spin a %s-ian Potters Wheel' % \
                get_latin(data['city_name'], capitalize=True)],
        'glass': ['Find Yourself Awash in Refracted Light'],
    }
    return random.choice(industries[data['industry']])


