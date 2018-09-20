''' buildings and built environment '''
from datetime import datetime
import random
import tracery
from utilities import format_text, get_latin

def eatery(name, dish, category, data):
    ''' a charming stone hut where they serve tea '''
    earliest = data['founded'] if data['founded'] > 1700 else 1700
    founding = random.randint(earliest - 4, datetime.now().year - 4)

    rules = {
        # structures
        'start': [
            '''With a gourmet, #cuisine# menu and #vibe_part#, #name# is a
               #platitude#. It will have you craving perennial favorites
               like #dish#. The setting, in #space#, is stunning, a perfect
               #city# experience.''',
            '''Owner #chef# has given #cuisine# cuisine a modern edge while
               still staying true to the regional style. The venue is stunning,
               #space# with #vibe_part#. Be sure to try the #dish#.''',
            '''In this #vibe# #type#, you can settle down in #space#. The menu
               features staples of #cuisine# cuisine, and is best known for
               traditional-style #dish#.''',
            '''#name# is a #cuisine# restaurant in #city# that's been
               going strong since #founding#. With a #vibe_part# and attentive
               service, it offers #cuisine# cuisine in #space#.''',
            '''#name# is a #vibe# #type# in a welcoming environment. It offers
               excellent #cuisine# food. The #dish# is hard to beat.''',
            '''This #space# gets rave reviews for
               #positive# and affordable #cuisine# food and ambiance. The
               #vibe_part# makes it a #platitude#.''',
            '''#name# is one of #city#'s best #cuisine# restaurants. It's a
               #platitude# where you can enjoy this #space#. There's a great
               range of dishes on offer, including #dish#.''',
            '''This #platitude# opened in #founding# and has set the tone for
               #city# cuisine ever since. Regulars like to order #dish#, sit
               back, and enjoy the #vibe_part#.''',
            '''Something of a social hub in #city#, this #vibe# #type#
               doesn't exactly advertise itself, but the #dish# is #positive#.
               Overall a #platitude#.''',
            '''A popular #vibe# cafe in the heart of #city# serving
               #dish# and drinks.''',
            '''Founded in early #founding#, #name# serves arguably the best
               know #dish# in town and it does a #positive# job. It has a
               #secondary_material#-decked interior and a #vibe_part#.''',
            '''This simple place, popular with the city workers, covers the
               bases for a #positive# lunch of #dish#.''',
            '''#name# is a rather dark and seedy place to say the least, but
               within its #material# walls you'll get a #positive# range of
               local dishes.''',
            '''This simple seven-table place offers #positive# breakfasts and
               gets packed by lunchtime -- and rightly so. The #dish# is a
               killer (not literally!).''',
        ],

        # info
        'name': '<em>%s</em>' % name,
        'type': category,
        'city': '<em>%s</em>' % get_latin(data['city_name'], capitalize=True),
        'neighborhood': 'the <em>%s</em> district' % get_latin(
            random.choice(data['geography']['neighborhoods']), capitalize=True),
        'founding': str(founding),
        'chef': data['get_person']('chef')['name'],

        # descriptive componenets
        'cuisine': '<em>%s</em>ian-style' % get_latin(
            data['country'],
            capitalize=True),
        'dish': '"<em>%s</em>" (a %s)' % (get_latin(dish['name']),
                                          dish['description']),
        'platitude': [
            'enduring favorite',
            'first-rate establishment',
            'local go-to',
            'local favorite',
            'popular place',
            'much loved #type#',
            'prestigious',
            'foodie oasis',
        ],
        'vibe_part': '#vibe# #atmosphere#',

        'space': [
            '#stories# with #color#-painted #material# walls and #accent#',
            'stylish #material# and #secondary_material# #stories#',
        ],
        'stories': '#%s#' % data['stories'],
        'single': ['building', '#type#'],
        'multi': 'spacious #building#',
        'many': '%s-floor #building#' % random.choice(
            ['first', 'second', 'third', 'fourth', 'fifth', 'top']),
        'accent': '#secondary_material# #accent_object#',
        'accent_object': ['wall-hangings', 'doorways', 'lamps'],
        'material': data['primary_material'],
        'secondary_material': data['secondary_material'],
        'building': ['suite', 'hall', 'room', '#type#'],

        # wordlists
        'atmosphere': ['atmosphere', 'charm'],
        'positive': ['top notch', 'good', 'great', 'fantastic', 'beloved',
            'excellent', 'high caliber', 'wonderful', 'popular',],
        'vibe': [
            'bustling',
            'busy',
            'relaxing',
            'sophisticated',
            'quaint',
            'cozy',
            'elegant',
            'world-renowned',
            'laid-back',
        ],
        'color': ['red', 'orange', 'yellow', 'green',
                  'purple', 'white', 'pink'],
    }
    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)

