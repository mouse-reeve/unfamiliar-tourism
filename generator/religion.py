''' facts about the city's religion '''
import random
import tracery
from utilities import format_text, get_latin

def get_religion(data, lang):
    ''' generate religion '''
    religion = {}
    religion['name'] = lang.get_word('NNP', 'religion')

    religion['gods'] = []
    god_count = 2

    # you need a lot of gods to pull off a divine hierarchy
    if data['divine_structure'] == 'hierarchical':
        god_count += 2
    god_count += abs(int(random.normalvariate(2, 20)))

    religion['god_count'] = god_count

    for i in range(god_count):
        religion['gods'].append({
            'name': lang.get_word('NNP', 'god-%d' % i),
        })
    religion['gods'] = describe_gods(
        religion['gods'], data)

    if data['divine_structure'] == 'hierarchical':
        religion['gods'] = create_hierarchy(religion['gods'])

    religion['religiosity'] = random.choice(['high', 'medium', 'low'])

    # note on structure:
    # "multifaceted" means that various gods are faces of a single divinity
    # "various" means that gods exist discreetly
    # "hierarchical" means they exist discreetly and with some more important
    religion['divine_structure'] = data['divine_structure']
    religion['worship'] = data['worship']
    religion['deity_forms'] = [data['deity_form'],
                               data['deity_form_secondary']]
    return religion


def create_hierarchy(gods):
    ''' arrange gods into a hierarchical pantheon
    There will be at least two tiers '''
    # min number of gods is 4
    pantheon = []
    top_max = 1 + int(len(gods) * 0.3)
    top = random.randint(1, top_max)
    for god in gods[:top]:
        god['rank'] = 1

    # only create three tiers if there are enough gods
    if len(gods) - top < 5:
        for god in gods[top:]:
            god['rank'] = 2
    else:
        mid_max = 1 + int((len(gods) - top_max) * 0.4)
        pantheon.append(gods[top:mid_max])
        for god in gods[top:mid_max]:
            god['rank'] = 2

        for god in gods[mid_max:]:
            god['rank'] = 3

    return gods

def describe_gods(gods, data):
    ''' basic description of the deity '''

    rules = {
        'start': '#single#' \
            if data['deity_form_secondary'] == 'none' \
            else '#dual#',
        'single': 'a #primary_form#',
        'dual': [
            'a hybrid #primary_form# and #secondary_form#',
            'a #primary_form# with a #secondary_form#\'s head',
            'half #primary_form# and half #secondary_form#',
        ],
        'primary_form': '#%s#' % data['deity_form'],
        'secondary_form': '#%s#' % data['deity_form_secondary'],
        'animal': [
            'serpent', 'bird', 'fish', 'lizard', 'deer', 'rat', 'dog',
            'rabbit', 'rodent', 'beetle', 'spider', 'snake', 'cat'],
        'plant': [
            'tree', 'tangle of vines', 'flower', 'seed pod', 'thick foliage',
            'tuft of grass'],
        'element': [
            'flame', 'ball of fire', 'boulder', 'gust of wind',
            'winding river', 'rain', 'cloud', 'plume of smoke',
            'pillar of stone', 'pillar of packed earth', 'slab of stone',
            'waterfall'],
        'human': '#descriptor# #person#',
        'descriptor': [
            'ancient', 'beautiful', 'hideous', 'wizended',
            'elderly', 'young', 'handsome', 'gigantic', 'diminutive', 'rotund',
            'athletic'],
        'person': ['person', 'human', 'child'],
    }
    if len(data['genders']) == 2:
        rules['person'] += ['man', 'woman']


    grammar = tracery.Grammar(rules)
    for god in gods:
        description = grammar.flatten('#start#')
        god['description'] = format_text(description)

    return gods

def describe_shrine(god, activity, data):
    ''' short description of a shrine for pins '''
    rules = {
        'start': 'A #descriptor# shrine to #god#.',
        'descriptor': '#adjective# #material#',
        'adjective': [
            'small', 'elaborate', 'popular', 'charming', 'sacred',
            'tucked-away', '' * 5],
        'god': [
            'the god #god_name#, who #appearance#',
            '#god_name#, a god who #appearance#',
        ],
        'appearance': 'is depicted as #depiction#',
        'god_name': get_latin(god['name'], capitalize=True),
        'depiction': god['description'],
        'material': [data['primary_material'], '' * 10],
        'sacrifice': 'Look for small sacrifices of #sacrifice_item# left ' \
                     'by belivers.',
        'sacrifice_item': [
            'blood', 'hair', 'teeth', 'fresh fruit' * 5,
            'loose change', 'bread', 'handmade icons' * 3],
        'omens': 'You may find a believer casting their fortune with '\
                 '#omen_object#.',
        'omen_object': [
            'polished stones', 'divining cards', 'lots', 'finger bones',
            'animal bones', 'stones', 'ceramic tiles', 'marble tiles',
            'carved sticks'],
    }
    if activity in ['sacrifice', 'omens']:
        rules['start'] += ' #%s#' % activity
    grammar = tracery.Grammar(rules)
    return format_text(grammar.flatten('#start#'))

def describe_temple(god, activity, data):
    ''' longer description of a temple and religious activity '''
    materials = {
        'brick': ['clay', 'ceramic'],
        'straw': ['woven straw', 'woven'],
        'wood': ['wooden', 'carved wood'],
        'stone': ['carved stone', 'stone', 'marble', 'stone inlayed'],
        'cloth': ['woven', 'tapestry'],
        'glass': ['blown glass', 'glass', 'stained glass'],
        'metal': ['hammered metal', 'metal', 'metal inlayed'],
        'tile': ['mosaic', 'tile mosaic'],
        'concrete': ['cement', 'brutalist', 'molded concrete'],
    }
    rules = {
        'start': [
            'This temple, devoted to #god#, is famous for its artfully ' \
                'crafted #material# icons and decorations.',
            'Believers gather at this temple #activity#.',
        ],
        'god': [
            'the god #god_name#, who #appearance#',
            '#god_name#, a god who #appearance#',
        ],
        'appearance': 'is depicted as #depiction#',
        'activity': '#%s#' % activity,
        'prayer': 'to pray to #god# for good fortune and health',
        'oracle': 'to consult the oracle, who sits on a #secondary_material# '\
                  'dais and dispenses advice and wisdom',
        'posession': 'for a ceremony in which #god_name#, who is believed to '\
                     'take the form of #depiction#, posesses a true believer '\
                     'and acts through their body, causing them to #movement#.',
        'glossolalia': 'for a ritual in which believers channel the word of '\
                       '#god#, and chant in a mysterious divine language.',
        'sacrifice': '#prayer#',
        'omen': '#prayer#',
        'movement': [
            'dance', 'spasm', 'leap and cavort', 'sway and sing',
            'contort into unnatural positions'],
        'god_name': get_latin(god['name'], capitalize=True),
        'depiction': god['description'],
        'material': materials[data['primary_material']] +
                    materials[data['secondary_material']],
    }
    grammar = tracery.Grammar(rules)
    return format_text(grammar.flatten('#start#'))

