''' describe tourist simple attractions '''
import random
import religion
from utilities import get_latin

def describe_buildings(data, lang):
    ''' finds the right describer tool '''
    pins = []
    available_gods = data['religion']['gods']
    for (i, building) in enumerate(data['building']):
        pin = {'type': building}
        if building == 'shrine':
            god = available_gods.pop()
            pin['name'] = '%s Shrine' % \
                get_latin(god['name'], capitalize=True)
            pin['description'] = religion.describe_shrine(
                god, random.choice(data['religion']['worship']), data)
        if building == 'temple':
            god = available_gods.pop()
            pin['name'] = '%s Temple' % \
                get_latin(data['religion']['name'], capitalize=True)
            pin['description'] = religion.describe_temple(
                god, random.choice(data['religion']['worship']), data)
        if building == 'statue':
            pin['name'] = describe_statue(data)
        else:
            name = lang.get_word('NNP', '%s%d' % (building, i))
            pin['name'] = '%s %s' % \
                    (get_latin(name, capitalize=True), building)
        pins.append(pin)
    return pins


def describe_statue(data):
    ''' a statue in the city '''
    name = data['ruler']['name']
    title = data['ruler']['title']
    return 'Statue of %s %s' % (title, name)

def describe_shop(data):
    return '$$$'
