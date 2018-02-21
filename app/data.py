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
    }

    # ------------------------ GRAPH DATA ------------------------- #
    ''' everything that's stored in neo4j gets loaded now. the following
    fields depend on what is set at this point. '''
    graph_dump = load_graph_data()
    if not graph_dump:
        return False
    data.update(graph_dump)

    # ----- GENERAL FACTS
    data['country'] = lang.get_word('LOC', 'country')
    data['city_name'] = lang.get_word('LOC', 'city')
    data['neighboring_city'] = lang.get_word('LOC', 'city2')

    data['language'] = {
        'name': lang.get_word('NNP', 'language'),
        'stats': lang.get_stats()
    }

    # ----- GEOGRAPHY
    data['geography'] = {
        'region': lang.get_word('LOC', 'region'),
        'river': lang.get_word('LOC', 'river'),
    }
    data['geography'][data['terrain']] = lang.get_word('LOC', data['terrain'])
    data['geography']['neighborhoods'] = [
        lang.get_word('LOC', 'neighborhood%d' % i) for i in range(5)]


    # great -- now we can have a card about language
    data['cards']['survive'].append('language')

    # economy -- this goes in the top bar, so no card
    data['currency'] = lang.get_word('NN', 'currency')
    data['exchange_rate'] = abs(random.normalvariate(0, 10))
    data['bills'] = [5, 10, 15, 20, 50, 100]
    data['coins'] = [1, 5, 10, 100]

    # the graph got us a handful of places to visit
    data['cards']['visit'] += data['building']

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
                {'name': lang.get_word('NN', 'gender-%d' % i)})

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
        'vegetables': [{'name': lang.get_word('NNP', 'vegetable%d' % i),
                        'description': cuisine.vegetable()} for i in range(2)],
    }

    data['cards']['learn'].append('fruit')


    # ------- WILDLIFE
    data['wildlife'] = data['cuisine']['animals'][0]
    data['cards']['learn'].append('wildlife')

    # ------- FASHION
    data['body_mod'] = fashion.body_mod(gender_count, data['motif'])

    # ----- BUILDINGS
    lang.get_word('NN', 'restaurant')
    data['restaurant'] = {
        'name': lang.get_word('JJ', 'serene'),
    }

    data['cuisine']['dish'] = {
        'name': lang.get_word('NN', 'local_dish'),
        'description': cuisine.local_dish(data),
    }
    data['restaurant']['description'] = architecture.eatery(
        get_latin(data['restaurant']['name'], capitalize=True),
        data['cuisine']['dish'],
        'restaurant',
        data
    )
    data['cards']['cuisine'].append('restaurant')


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
    lang.get_word('NN', 'fruit')
    lang.get_word('NN', 'pastry')
    lang.get_word('NN', 'alcohol')
    lang.get_word('NN', 'tea')

    lang.get_word('NN', 'hello')
    lang.get_word('NN', 'thanks')
    lang.get_word('NN', 'goodbye')
    lang.get_word('NN', 'sorry')
    lang.get_word('NN', 'where')
    lang.get_word('NN', 'name')
    lang.get_word('PRP', 'i')
    lang.get_word('NN', 'coin')

    data['dictionary'] = lang.dictionary

    # ----- SLOGAN
    data['slogan'] = slogan(data)

    return data
