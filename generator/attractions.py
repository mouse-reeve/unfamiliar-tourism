''' describe tourist simple attractions '''
import random
import religion
import tracery
from utilities import get_latin, format_text

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
        elif building == 'temple':
            god = available_gods.pop()
            pin['name'] = '%s Temple' % \
                get_latin(data['religion']['name'], capitalize=True)
            pin['description'] = religion.describe_temple(
                god, random.choice(data['religion']['worship']), data)
        elif building == 'statue':
            pin['name'] = 'Statue of %s' % data['ruler']['name']
            pin['description'] = describe_statue(data)
        elif building in ['capitol', 'palace']:
            earliest = data['founded']
            authoritarianism = data['stats']['authoritarianism']
            pin['name'] = '%s %s' % (
                get_latin(data['country'], capitalize=True), building)
            # TODO: this should be it's own tracery grammar
            pin['description'] = \
                '''Built in {date}, this imposing {material} building houses
                the seat of the {country} nation's government. You aren't likely
                to set eyes on {article} {feeling} {title}, but the building is
                abuzz with clerks and functionaries.'''.format(
                    country=get_latin(data['country'], capitalize=True),
                    date=random.randint(earliest - 1, earliest + 20),
                    material=data['primary_material'],
                    article='a' if data['government'] == 'oligarchy' else 'the',
                    feeling='beloved' \
                            if authoritarianism < 0.5 \
                            else 'controversial' \
                            if authoritarianism > 0.7 else '',
                    title=data['ruler']['title']
                )
        elif building == 'bakery':
            name = lang.get_word('NNP', '%s%d' % (building, i))
            product = random.choice(
                ['bread', 'pastries', 'sweets', 'baked goods'])
            pin['description'] = describe_specialty(name, product, data)
        elif building == 'bookstore':
            # TODO: this deserves a longer description
            name = lang.get_word('NNP', '%s%d' % (building, i))
            product = random.choice(
                ['book-buying', 'reading', 'literature'])
            pin['name'] = '%s %s' % (get_latin(name, capitalize=True), building)
            pin['description'] = describe_specialty(name, product, data)
        elif building == 'perfumery':
            name = lang.get_word('NNP', '%s%d' % (building, i))
            pin['name'] = '%s %s' % (get_latin(name, capitalize=True), building)
            pin['description'] = describe_specialty(name, 'perfume', data)
        elif building == 'kiln':
            name = lang.get_word('NNP', '%s%d' % (building, i))
            pin['name'] = '%s %s' % (get_latin(name, capitalize=True), building)
            pin['description'] = describe_specialty(name, 'pottery', data)
        else:
            name = lang.get_word('NNP', '%s%d' % (building, i))
            pin['name'] = '%s %s' % \
                    (get_latin(name, capitalize=True), building)
        pins.append(pin)
    return pins

def describe_specialty(name, product, data):
    ''' the city is famous for .... bread? '''
    rules = {
        'start': [
            '#city# is #famous# for its #product#, and #superlative#.',
            '#product# is big business in #city#, and #superlative#.',
            '#city#\'s name is practically synonymous with #product#, ' \
                'and #superlative#.',
        ],
        'product': product,
        'name': get_latin(name, capitalize=True),
        'city': get_latin(data['city_name'], capitalize=True),
        'famous': [
            'famous', 'world renowned', 'renowned', 'known',
            'known far and wide',
        ],
        'superlative': [
            'this is the #best# destination to partake',
            'there\'s no better introduction to the local specialty than ' \
                '#name#',
            'it doesn\'t get better than #name#',
            '#name# is the best in the business',
        ],
        'best': ['best', 'number one'],
    }

    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)


def describe_statue(data):
    ''' a statue in the city '''
    name = data['ruler']['name']
    title = data['ruler']['title']
    article = 'a' if data['ruler']['multiple'] else 'the'
    return '%s is %s %s %s.' % (
        name,
        article,
        get_latin(data['city_name'], capitalize=True),
        title
    )
