''' all the information about a city in one json blob '''
import architecture
from calendar import Calendar
import cuisine
import fashion
import religion
from slogan import slogan
import wildlife

from graph import load_graph_data
from foreigntongue import Language
from utilities import get_latin

from datetime import datetime
from collections import defaultdict
import random
import json
import sys

def generate_datafile(seed):
    ''' let's generate a city! it's hard to stay focused, so our goal
    can be to make:
        1. notable landmarks
        2. events one could attend
        3. places to eat
        4. survival guide
    '''

    random.seed(seed)
    lang = Language()

    # for events, populate a calendar, and then on pageload, the appropriate
    # cards for time of year will show up.
    # the timestamp is a day in the year 2008, since 2008 is a leap year
    data = {
        'seed': seed,
        'cards': defaultdict(lambda: []),
        'calendar': Calendar(),
        'pins': [],
    }

    # ------------------------ GRAPH DATA ------------------------- #
    ''' everything that's stored in neo4j gets loaded now. the following
    fields depend on what is set at this point. '''
    graph_dump = load_graph_data()
    if not graph_dump:
        return False
    data.update(graph_dump)

    # ----- GENERAL FACTS
    data['city_name'] = lang.get_word('LOC', 'city')
    data['country'] = lang.get_word(
        'LOC', 'country',
        definition='The country in which %s is situated' % \
                get_latin(data['city_name'], capitalize=True))
    data['city_name'].set_definition('A city in %s' % \
            get_latin(data['country'], capitalize=True))
    data['neighboring_city'] = lang.get_word(
        'LOC', 'city2', definition='A city near %s in %s' % \
                (get_latin(data['city_name'], capitalize=True),
                 get_latin(data['country'], capitalize=True)))

    data['language'] = {
        'name': lang.get_word('NNP', 'language',
                              definition='The local language'),
        'stats': lang.get_stats()
    }

    # ----- GEOGRAPHY
    data['geography'] = {
        'region': lang.get_word(
            'LOC', 'region',
            definition='The region of %s in which %s is situated' % \
                    (get_latin(data['country'], capitalize=True),
                     get_latin(data['city_name'], capitalize=True))),
        'river': lang.get_word('LOC', 'river', definition='A river in %s' % \
                get_latin(data['country'], capitalize=True)),
    }
    data['geography'][data['terrain']] = lang.get_word('LOC', data['terrain'])
    data['geography']['neighborhoods'] = [
        lang.get_word('LOC', 'neighborhood%d' % i)
        for i in range(10)]
    data['geography']['streets'] = [
        lang.get_word('LOC', 'hood%d' % i)
        for i in range(10)]


    # great -- now we can have a card about language
    data['cards']['survive'].append('language')

    # economy -- this goes in the top bar, so no card
    data['currency'] = lang.get_word('NN', 'currency',
                                     definition='The local currency')
    data['exchange_rate'] = abs(random.normalvariate(0, 10))
    data['bills'] = [5, 10, 15, 20, 50, 100]
    data['coins'] = [1, 5, 10, 100]

    # ----- helper functions for naming folks
    def get_person(identifier, title, gender_count, surname=None):
        ''' create a basic person bio '''
        given_name = lang.get_word('NNP', identifier+'given')
        surname = surname or lang.get_word('NNP', identifier+'sur')
        fullname = get_name(given_name, surname)
        return {
            'given_name': given_name,
            'surname': surname,
            'name': fullname,
            'title': title,
            'gender': random.randint(0, gender_count)
        }


    surname_first = bool(random.randint(0, 1))
    def get_name(given_name, surname):
        ''' just print out the latin name of whoever '''
        name = [get_latin(surname, capitalize=True),
                get_latin(given_name, capitalize=True)]
        return ' '.join(name) if surname_first else ' '.join(name[::-1])

    # ----- GENDER
    data['genders'] = []
    gender_count = random.choice([2, 3, 5])

    # and make it easier to generate a random name
    data['get_person'] = lambda title: get_person(str(random.random()),
                                                  title,
                                                  gender_count)
    if gender_count == 2:
        data['genders'] = [
            {'name': lang.get_word('NN', 'male')},
            {'name': lang.get_word('NN', 'female')}
        ]
    else:
        for i in range(0, gender_count):
            data['genders'].append(
                {'name': lang.get_word('NN', 'gender-%d' % i,
                                       definition='A gender')})

    if gender_count > 2:
        # the presence of multiple genders is worth noting, so add a card
        data['cards']['survive'].append('gender')


    # misc facts
    data['city_age'] = random.choice([50] + [500] * 5 + [1000] * 5)
    data['founded'] = int(datetime.now().year - \
        abs(random.normalvariate(data['city_age'], data['city_age']/2)))

    isolation = random.randint(4, 10) / 10.0
    data['stats'] = {
        'isolation': isolation,
        'insularity': random.randint(int(isolation * 10), 10) / 10.0,
        'population': random.randint(
            1000 * isolation, int(10000000/(isolation ** 4))),
        'minorities': random.randint(0, 3),
        'ruler': get_person('ruler', 'Ruler', gender_count),
        'authoritarianism': random.random(),
    }


    if data['stats']['authoritarianism'] > 0.8:
        data['cards']['survive'].append('authoritarianism')
    if data['stats']['authoritarianism'] > 0.97:
        data['advisory'] = random.sample(
            ['crime', 'civil unrest', 'terrorism', 'armed conflict',
             'strikes and protests', 'political tension',
             'risk of kidnapping'], 2)
    elif data['stats']['authoritarianism'] > 0.97:
        # watch yourself
        data['advisory'] = random.choice(
            ['risk of arrest and long-term detention',
             'repressive poltiical climate'])

    # on the topic of government, maybe we should have related events
    if data['government'] == 'republic':
        data['calendar'].arbitrary_date('Elections! Or something like that.')
    elif data['government'] == 'monarchy':
        data['calendar'].arbitrary_date('A day all about the great ruler')
    elif data['government'] == 'oligarchy':
        data['calendar'].arbitrary_date('Gathering of the ruling families')
    elif data['government'] == 'theocracy':
        # a theocratic government should have hella religious holidays
        data['calendar'].recurring_event('The weekly religious observance')

    if data['government'] in ['monarchy', 'theocracy'] and \
            random.random() > 0.7:
        data['calendar'].arbitrary_date('Coronation of a new ruler')


    # ----- RELIGION
    data['religion'] = religion.get_religion(data, lang)
    del data['divine_structure']
    del data['deity_form']
    del data['deity_form_secondary']
    del data['worship']

    # lets have some religious buildings
    for building in data['building']:
        if building == 'shrine':
            god = random.choice(data['religion']['gods'])
            data['pins'].append({
                'description':
                    'A shrine to the god %s, who %s' %
                    (get_latin(god['name'], capitalize=True),
                     god['description']),
            })


    # ------------------------ DESCRIPTIONS ------------------------- #

    # ----- FOOD
    data['cuisine'] = {
        'fruit': cuisine.fruit(data['climate']['name']),
        'tea': cuisine.tea(data['climate']['name']),
        'teacup': cuisine.teacup(data['primary_material'], data['motif']),
        'animals': [{'name': lang.get_word('NNP', 'critter%d' % i),
                     'description': wildlife.animal(
                         data['climate']['name'],
                         data['terrain'])} for i in range(3)],
        'vegetables': [{'name': lang.get_word('NN', 'vegetable%d' % i),
                        'description': cuisine.vegetable()} for i in range(2)],
    }

    for veggie in data['cuisine']['vegetables']:
        veggie['name'].set_definition('A vegetable native to %s; %s' % \
                (get_latin(data['city_name'], capitalize=True),
                 veggie['description']))

    data['cards']['learn'].append('fruit')


    # ------- WILDLIFE
    data['wildlife'] = data['cuisine']['animals'][0]
    data['cards']['learn'].append('wildlife')

    # ------- FASHION
    data['body_mod'] = fashion.body_mod(gender_count, data['motif'])

    # ----- BUILDINGS
    lang.get_word('NN', 'restaurant')

    data['cuisine']['dish'] = []

    # TODO: these should be generated
    name_options = ['tasty', 'delicious', 'outsider']
    for i in range(3):
        data['cuisine']['dish'].append({
            'name': lang.get_word('NN', 'local_dish%d' % i),
            'description': cuisine.local_dish(data),
        })
        lang.get_word('NN', 'local_dish%d' % i).set_definition(
            data['cuisine']['dish'][i]['description'])

        restaurant_name = lang.get_word('JJ', name_options[i])
        data['pins'].append({
            'type': 'food',
            'name': get_latin(restaurant_name, capitalize=True),
            'description': architecture.eatery(
                get_latin(restaurant_name, capitalize=True),
                data['cuisine']['dish'][i],
                'restaurant',
                data),
        })


    if (random.random() > 0.0):
        lang.get_word('NN', 'teahouse')
        data['teahouse'] = {
            'name': lang.get_word('JJ', 'serene'),
        }
        data['teahouse']['description'] = architecture.eatery(
            get_latin(data['teahouse']['name'], capitalize=True),
            data['cuisine']['dish'][0],
            'teahouse',
            data
        )
        data['cards']['cuisine'].append('teahouse')

    # ------------------------ DISPLAY ITEMS ------------------------- #
    # reformat the cards object to work with the ui

    # ----- Whitelist cards that are ready
    ready = ['language', 'fruit', 'wildlife', 'restaurant']
    for group in data['cards']:
        data['cards'][group] = [c for c in data['cards'][group] if c in ready]
    data['cards'] = [{'title': 'events', 'cards': []}] + \
        [{'title': c, 'cards': data['cards'][c]} for c in data['cards'] \
         if data['cards'][c]]


    # extract the calendar into a json format
    data['calendar'] = data['calendar'].get_calendar()

    # lookup words we'll need later. doing this now instead of on the fly
    # so that the lang library isn't a dependency
    lang.get_word('NN', 'market')
    lang.get_word(
        'NN', 'fruit',
        definition='A type of fruit native to the %s region' % \
                    get_latin(data['geography']['region'],
                              capitalize=True))
    lang.get_word('NN', 'pastry')
    lang.get_word('NN', 'alcohol')
    lang.get_word('NN', 'tea')

    lang.get_word('NN', 'hello')
    lang.get_word('NN', 'thanks')
    lang.get_word('NN', 'goodbye')
    lang.get_word('NN', 'sorry')
    lang.get_word('RB', 'where')
    lang.get_word('NN', 'name')
    lang.get_word('PRP', 'i', definition='I; first-person pronoun')
    lang.get_word('NN', 'coin')
    lang.get_word('VB', 'be', definition='To be')

    data['dictionary'] = lang.dictionary

    # ----- SLOGAN
    data['slogan'] = slogan(data)

    return data

if __name__ == '__main__':
    try:
        seed = sys.argv[1]
    except IndexError:
        seed = 0

    sys.stdout.write(
        json.dumps(generate_datafile(seed), default=lambda x: x.__dict__)
    )
