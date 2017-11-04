''' facts about the city's religion '''
import random

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
        religion['gods'].append(
            lang.get_word('NNP', 'god-%d' % i))

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
    pantheon.append(gods[:top])
    # only create three tiers if there are enough gods
    if len(gods) - top < 5:
        pantheon.append(gods[top:])
    else:
        mid_max = 1 + int((len(gods) - top_max) * 0.4)
        pantheon.append(gods[top:mid_max])
        pantheon.append(gods[mid_max:])

    return pantheon
