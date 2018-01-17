''' a one-line description of the city'''
import tracery
from utilities import format_text

def slogan(city_age, industry, population, city_name):
    ''' describe the cup tea is drunk from '''

    industry_part = {
        'weaving': [
            'innovative looms and weaving', 'tapestries',
            'fabrics and textiles', 'textiles and fabrics'],
        'fishing': ['scenic fishing boats', 'seaside charm',
                    'delicious daily catch'],
        'metalworking': ['intricate metalworking',
                         'majestic forges and smiths'],
        'printing': ['supplying the nation with fine books',
                     'its printers and bookbinding'],
        'carving': ['sculpture and statuary', 'delicate carved goods'],
        'pastry': ['speciality pastry', 'its hearty breads'],
        'brewing': ['the distinctive liquor it produces',
                    'its unique local liquor'],
        'ceramics': ['handcrafted ceramics', 'artisan ceramics'],
        'glass': ['hand blown glass'],
        'art': ['culture and fine arts', 'the arts'],
        'literature': ['its lively literary community'],
        'death': ['fascination with death', 'macabre fixations',
                  'morbid fascinations'
                  'elaborate funerary practices'],
        'technology': ['technological innovation'],
        'education': ['learning and philosophy', 'fostering deep thinkers'],
        'crop': ['a rare flowering plant said to have spiritual properties'],
    }

    age_part = 'ancient city'
    if city_age == 50:
        age_part = 'exciting, fast-paced young city'
    elif city_age == 500:
        age_part = 'modern metropolis'

    age_part = {
        1000: ['ancient #city#', 'historical #city#', '#city# of antiquity',
               'old world #city#'],
        500: ['modern #city#', 'gleaming #city#', 'progressive #city#',
              'modern #city# with a rich history'],
        50: ['young #city#', 'fast-paced young #city#', 'boomtown #city#',
             'scrapy #city#', 'hyper-modern #city#', 'exciting new #city#']
    }

    city_words = ['urban gem', 'urban jewel'] + ['city'] * 5
    if population < 5000:
        city_words += ['town', 'village', 'township', 'retreat']
    if population > 1000000:
        city_words += ['metropolis', 'capitol', 'powerhouse', 'megapolis']

    rules = {
        'start': 'a #age_part# &mdash; #fame_part#',
        'age_part': age_part[city_age],
        'fame_part': 'a #fame# #industry_part#',
        'fame': ['beacon of', 'center of', 'hotbed of',
                 'destination for', 'must-see for',],
        'city': city_words,
        'industry_part': industry_part[industry],
        'unique': ['uniquely', 'distinctively', 'quintessentially'],
    }
    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)

