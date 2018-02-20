''' buildings and built environment '''
from datetime import datetime
import random
import tracery
from utilities import format_text, get_latin

def building(primary_material, secondary_material):
    ''' a generic building '''

    rules = {
        'start': 'a %s building with %s' % \
            (primary_material, secondary_material)
    }
    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)


def eatery(name, category, data):
    ''' a charming stone hut where they serve tea '''
    rules = {
        # structures
        'start': [
            '''With a gourmet, #cuisine# menu and #vibe#, #name# is a
               #platitude#. It will have you craving perennial favorites
               like #dish#. The setting in #space# is stunning, a perfect
               #city# experience''',
            '''Owner #chef# has given #cuisine# a modern edge while
               still staying true to the regional style. The venue is stunning,
               #space# with #vibe#. Be sure to try the #dish#.''',
            '''In this #vibe# #type#, you can settle down in #space#. The menu
               features staples of #city# #cuisine#, and is best known for
               traditional-style #dish#.''',
            '''#name# is a #cuisine# restaurant in #neighborhood# that's been
               going strong since #founding#. With #vibe# and attentive service,
               it serves #cuisine# in #space#.''',
            '''#name# is a #vibe# #type#, and always welcoming. It offers
               excellent #cuisine#. The #dish is hard to beat.''',
            '''This #space# #type# in #neighborhood# gets rave reviews for
               top notch and affordable #cuisine# and ambiance. The #vibe# makes
               it a #platitude#''',
            '''#name# is one of #city#'s best #cuisine# restaurants. It's
               #platitude# where you can enjoy #space#. There's a greate range
               of dishes on offer, including #dish#.''',
            '''This #platitude# opened in #founding# and has set the tone for
               #city# cuisine ever since. Many regular order #dish# and sit back
               and enjoy the #vibe#.''',
        ],

        # info
        'name': name,
        'type': category,
        'city': get_latin(data['city_name'], capitalize=True),
        'neighborhood': 'the %s district' % get_latin(
            random.choice(data['geography']['neighborhoods']), capitalize=True),
        'founding': str(random.randint(data['founded'] + 5,
                                       datetime.now().year - 4)),
        'chef': data['get_person']('chef')['name'],

        # descriptive componenets
        'cuisine': 'local cuisine',
        'dish': 'local dish',
        'platitude': [
            'enduring favorite'
            'first-rate establishment',
            'local go-to',
            'local favorite',
            'popular place',
            'much loved #type#',
            'prestigious',
            'foodie oasis',
        ],
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
        'space': ['space'],

        # wordlists
        'atmosphere': ['atmosphere', 'charm'],
    }
    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)
