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


def teahouse(data):
    ''' a charming stone hut where they serve tea '''
    rules = {
        'start': ['a #charm# #primary_material# #building#'],
        'charm': ['charming', 'quaint', 'cozy'],
        'primary_material': data['primary_material'],
        'building': 'built in the traditional style'
    }
    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)
