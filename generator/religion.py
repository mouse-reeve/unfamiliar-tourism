''' facts about the city's religion '''
import random
import tracery
from utilities import format_text

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
        'start': [
            'is depicted as #depiction#'],
        'depiction': '#single#' \
            if data['deity_form_secondary'] == 'none' \
            else '#dual#',
        'single': '#primary_form#',
        'dual': [
            'a hybrid #primary_form# and #secondary_form#',
            'a #primary_form# with a #secondary_form# head',
            'half #primary_form# and half #secondary_form#',
        ],
        'primary_form': '#%s#' % data['deity_form'],
        'secondary_form': '#%s#' % data['deity_form_secondary'],
        'animal': [
            'serpent', 'bird', 'fish', 'feline', 'canine', 'lizard', 'deer',
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
        rules['person'].concat('man', 'woman')


    grammar = tracery.Grammar(rules)
    for god in gods:
        description = grammar.flatten('#start#')
        god['description'] = format_text(description)

    return gods
