''' Nature! '''
import random
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
            'eat clay to aid their digestion',
            'perform elaborate dances to attract a mate',
            'can turn their heads almost all the way around',
            'howl at the moon',
            'hunt by smell',
            'are totally blind, and navigate by sound',
            'have to eat their bodyweight in food each day',
            'can catch and spread human diseases',
            'run faster than horses',
            'are born a downy coat that they later shed',
            'have digestive systems that can filter out toxins and poisons',
            'rely on one variety of rare, native grass as a dietary staple',
            'have perfectly #cold_color# eyes',
            'have different colored eyes',
            'vastly outnumber humans',
            'have #cold_color#ish #warm_color# blood',
            'scavenge scraps of cloth to swaddle their young',
            'kidnap and raise other animal\'s young as their own',
            'have complex family and social relationships',
            'give each other gifts of particularly beautiful stones',
            'have names for each other',
            'are fastidiously tidy',
            'eat their mates',
            'are consumed by their own offspring',
            'can change gender at will',
            'can reproduce asexually if they are unable to find a mate',
            'can go %d weeks without eating' % random.randint(2, 5),
            'can solve complex puzzles and open doors',
            'live up to %d years of age' % random.randint(20, 200),
            'prefer to take over human structure\'s for nests',
            'build huts for themselves out of woven branches',
            'taste with their feet',
            'have regional dialects and accents',
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
            'they steal children who wander too far from their homes',
            'they protect infants from sickness and ill fortune',
            'they can transform into humans under certain conditions',
            'they can return from death',
            'their bones have healing properties',
            'they can predict the weather',
            'they can read and understand human language',
            'it is bad luck to hurt them',
            'they hold wild bacchanalias in the dead of night',
            'they imitate voices of loved ones to lure people into traps',
        ],
    }

    # added after so that the odds aren't skewed
    rules['bird_behavior'] = rules['behavior'] + [
        'can mimick human speach'
        'mimicks ambient noises and speach',
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
            'bright #warm_color# and #cold_color#', '#cold_color#'
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
