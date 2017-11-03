''' Nature! '''
import tracery
from utilities import format_text

class Wildlife(object):
    ''' generate nature '''
    def __init__(self, climate, terrain):
        self.climate = climate
        self.terrain = terrain

    def animal(self):
        ''' urban wildlife '''
        rules = {
            'start': '#type#. #human_interaction#.',
            'type': [
                '#bird#', '#rodent#', '#raccoon#', '#coyote#'
            ],
            'insect': 'insects that #behavior#',
            'bird': '#size#, #color# #bird_type# with #bird_accent# ' \
                    'that #bird_behavior#',
            'rodent': '#size# rodents that #behavior#',
            'raccoon': '#size#, raccoon-like animals that #behavior#',
            'coyote': '#size# species of wild dog that #behavior#',
            'fish': 'slimy fish that #behavior#',

            # birds
            'bird_type': ['raptors', 'songbirds', 'birds'],
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
                'builds nests out of #weird_material#',
                'makes jewelry-like adornments for itself from plants',
                'wears hats made from cup-shaped leaves or blossoms',
                'collects #weird_material# and offers its collection to' \
                        'potential mates',

                'mates for life, and dies when its mate dies',
                '#cry_verb# human laughter',
                '#cry_verb# an infant\'s scream',
                '#cry_verb# metal clanking',
                '#cry_verb# the background hubbub of a cocktail party',

                'run as fast as 30 miles per hour',
                'can eat plastic',
                'drink boiling water',
                'sever a person\'s head from their body in one stroke',
                'befriend spiders',
                'kill instantly with one venemous bite',
                'jump as high as 30 feet'
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
            ],
            'cry_verb': [
                'cry like',
                'have a call that sounds like'
            ],

            'human_interaction': [
                'Locals believe #belief#',
                'Local children like to catch them and keep them as pets',
                'They are hunted for food, and considered a delicacy',
            ],
            'belief': [
                'that they are the spirits of the dead',
                'they can travel into the afterlife',
                'they know how you will die',
                'they watch our dreams as we sleep',
            ],
        }

        # added after so that the odds aren't skewed
        rules['bird_behavior'] = rules['behavior'] + [
            'can mimick human speach'
            '#cry_verb# ocean waves',
            '#cry_verb# radio static',
            '#cry_verb# gusts of wind',
            '#cry_verb# notes on a piano',
            '#cry_verb# running water',
            '#cry_verb# rainfall',
            'can fly for days without rest',
        ]

        if self.terrain == 'coast':
            rules['type'].append('#fish#')
            rules['bird_type'] += ['sea birds', 'aquatic birds']
            rules['color'] += ['gray', 'pale blue']

        if 'tropical' in self.climate:
            rules['color'] += [
                'brightly colored', 'multicolored', '#warm_color#',
                'bright #warm_color# and #cold_color', '#cold_color#'
            ]
            rules['type'].append('#insect#')
        elif self.climate in ['arid', 'semi_arid', 'hot_desert']:
            rules['color'] += [
                'dusty #warm_color#', 'muted #warm_color#', '#warm_color#']
        else:
            rules['color'] += [
                '#warm_color#', '#cold_color#']

        grammar = tracery.Grammar(rules)
        sentence = grammar.flatten('#start#')

        return format_text(sentence)
