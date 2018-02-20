''' Nature! '''
import tracery
from utilities import format_text

def animal(climate, terrain):
    ''' urban wildlife '''
    rules = {
        'start': '#type#. #human_interaction#.',
        'type': [
            '#bird#', '#rodent#', '#raccoon#', '#coyote#'
        ],
        'insect': 'insects that #behavior#',
        'bird': '#size#, #color# #bird_type# with #bird_accent# ' \
                'that #bird_behavior#',
        'rodent': '#size# #warm_color# rodents that #behavior#',
        'raccoon': '#size#, raccoon-like animals that #behavior#',
        'coyote': '#size# wild dogs with #warm_color# and #color# coats. '\
                  'It is said that they #behavior#',

        # birds
        'bird_type': ['raptors'] + 10 * ['songbirds', 'birds'],
        'bird_accent': [
            'dark #color# wings',
            '#warm_color# throats',
            '#cold_color# bellies',
            '#cold_color# tails',
            '#color# heads',
            'striking #warm_color# beaks',
            'sharp talons',
            'long, flowing tails',
            'crooked beaks'
        ],

        'size': ['large', 'small', 'tiny'],
        'color': ['white', 'brown'],
        'warm_color': ['red', 'pink', 'orange', 'yellow'],
        'cold_color': ['green', 'blue', 'teal', 'purple'],

        'behavior': [ # behavior that can apply to various types of critter
            'build nests out of #weird_material#',
            'make jewelry-like adornments for themselves from plants',
            'wear hats made from cup-shaped leaves or blossoms',
            'collect #weird_material# and offers its collection to' \
                    'potential mates',

            'mate for life, and remain alone if their mate dies',
            '#cry_verb# human laughter',
            '#cry_verb# an infant\'s scream',
            '#cry_verb# clanking metal',
            '#cry_verb# grinding stones',
            '#cry_verb# dripping water',
            '#cry_verb# a scream of fear',
            '#cry_verb# a wolf howl',
            '#cry_verb# a lion\'s roar',

            'can run as fast as 30 miles per hour',
            'can eat plastic',
            'can drink near-freezing or boiling water',
            'can sever a person\'s head from their body in one stroke',
            'befriend spiders',
            'can kill with one venemous bite',
            'can jump as high as 30 feet',
            'sleep for as much as 18 hours a day',
            'groom each other to show affection',
            'dye patches of their back with #cold_color# sap',
        ],
        'weird_material': [
            'human skin',
            'scavenged bones',
            'scavenged teeth',
            'stolen articles of clothing',
            'flower petals',
            'sap extracted from trees and hardened into a strong resin',
            'wires stolen from electronics',
            'pages of books',
            'human hair',
            'stolen shoes',
            'bright-colored threads and scraps of fabric',
            'fruit skins',
            'globules of their saliva',
        ],
        'cry_verb': [
            'emit cry that sounds like',
            'have a call that sounds like',
            'make a sound like',
        ],

        'human_interaction': [
            'Locals believe #belief#',
            'Local children like to catch them and keep them as pets',
            'They are hunted for food, and considered a delicacy',
            'They are considered a pest',
            'Locals do not acknowledge their presence',
        ],
        'belief': [
            'they are manifestations of the spirits of the dead',
            'they can travel into the afterlife',
            'they know how you will die',
            'they know your secrets',
            'they have secret names',
            'they steal memories, causing forgetfulness',
            'they feed on human sadness',
            'they can communicate with infants',
            'they can speak to the dead',
            'they are representatives of the divine',
            'they can speak with humans if they choose to',
            'they bring good luck',
            'they bring bad luck',
            'they are harbingers of birth',
            'they are harbingers of death',
            'they are harbingers of change',
            'they watch our dreams as we sleep',
        ],
    }

    # added after so that the odds aren't skewed
    rules['bird_behavior'] = rules['behavior'] + [
        'can mimick human speach'
        '#cry_verb# ocean waves',
        '#cry_verb# radio static',
        '#cry_verb# gusts of wind',
        '#cry_verb# bits of music',
        '#cry_verb# running water',
        '#cry_verb# rainfall',
        'can fly for days without rest',
    ]

    if terrain == 'coast':
        rules['bird_type'] += ['sea birds', 'aquatic birds']
        rules['color'] += ['gray', 'pale blue']

    if 'tropical' in climate:
        rules['color'] += [
            'brightly colored', 'multicolored', '#warm_color#',
            'bright #warm_color# and #cold_color', '#cold_color#'
        ]
        rules['type'].append('#insect#')
    elif climate in ['arid', 'semi_arid', 'hot_desert']:
        rules['color'] += [
            'dusty #warm_color#', 'muted #warm_color#', '#warm_color#']
    else:
        rules['color'] += [
            '#warm_color#', '#cold_color#']

    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)
