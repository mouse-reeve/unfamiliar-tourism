''' buildings and built environment '''
import tracery
from utilities import format_text

def building(primary_material, secondary_material):
    ''' a generic building '''
    rules = {
        'start': 'a %s building with %s' % \
            (primary_material, secondary_material)
    }
    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)
