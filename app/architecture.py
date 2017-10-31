''' buildings and built environemnt '''
import tracery
from utilities import format_text

class Architecture(object):
    ''' descriptions of buildings '''
    def __init__(self, city_type, primary_material, secondary_material, motif):
        self.city_type = city_type
        self.primary_material = primary_material
        self.secondary_material = secondary_material
        self.motif = motif

    def building(self):
        ''' a generic building '''
        rules = {
            'start': 'a %s building with %s' % (self.primary_material, self.secondary_material)
        }
        grammar = tracery.Grammar(rules)
        sentence = grammar.flatten('#start#')

        return format_text(sentence)
