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
            'start': 'a #type# that #behavior#',
            'type': [
                '#bird#', '#rodent#', '#raccoon#', '#coyote#'
            ],
            'rodent': '#size# rodent',
            'raccoon': '#size#, raccoon-like animal',
            'coyote': '#size# species of wild dog',
            'fish': 'slimy fish',
            'bird': ['#size#, #color# #bird_type# with #bird_accent#'],
            'bird_type': ['raptor', 'songbird', 'bird'],
            'bird_accent': [
                'dark #color# wings', 'a #warm_color# throat',
                'a #cold_color# belly', 'a #cold_color# tail',
                'a striking #warm_color# beak', 'sharp talons',
                'a long, flowing tail', 'a crooked beak'],
            'size': ['large', 'small', 'tiny'],
            'color': ['white', 'brown'],
            'warm_color': ['red', 'pink', 'orange', 'yellow'],
            'cold_color': ['green', 'blue', 'teal', 'purple'],

            'behavior': [
                'makes #build_thing#', 'can #physical_feat#',
                'mates #mating#', 'makes a cry like #sound#'],
            'build_thing': [
                'underground burrows', 'nests', 'tiny houses',
                'necklaces for itself from plants and trash',
                'and wears hats of cup-shaped leaves or blossoms'],
            'mating': [
                'for life, and dies when its mate dies'],
            'sound': [
                'human laughter', 'an infant\'s scream', 'ocean waves',
                'radio static', 'gusts of wind', 'notes on a piano',
                'metal clanking', 'running water', 'rainfall'],
            'physical_feat': [
                'run as fast as 30 miles per hour',
                'live without food or water for ten days',
                'drink boiling water',
                'sever a persons head from their body in one stroke',
                'befriend spiders',
                'kill instantly with one venemous bite',
                'jump as high as 30 feet'],
        }
        if self.terrain == 'coast':
            rules['type'].append('fish')
            rules['bird_type'] += ['sea bird', 'aquatic bird']
            rules['color'] += ['gray', 'pale blue']

        if 'tropical' in self.climate:
            rules['color'] += [
                'brightly colored', 'multicolored', '#warm_color#',
                'bright #warm_color# and #cold_color', '#cold_color#'
            ]
        elif self.climate in ['arid', 'semi_arid', 'hot_desert']:
            rules['color'] += [
                'dusty #warm_color#', 'muted #warm_color#', '#warm_color#']
        else:
            rules['color'] += [
                '#warm_color#', '#cold_color#']

        grammar = tracery.Grammar(rules)
        sentence = grammar.flatten('#start#')

        return format_text(sentence)
