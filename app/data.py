''' all the information about a city in one json blob '''
import architecture
import cuisine
import fashion
from graph import load_graph_data
from news import News
import religion
import wildlife

from foreigntongue import Language

from datetime import datetime
import random

def generate_datafile(seed):
    ''' generate a city '''

    random.seed(seed)
    lang = Language()
    data = {'seed': seed}

    # ----- GENERAL FACTS
    data['country'] = lang.get_word('LOC', 'country')
    data['city_name'] = lang.get_word('LOC', 'city')

    data['language'] = {
        'name': lang.get_word('NNP', 'language'),
        'stats': lang.get_stats()
    }

    data['city_age'] = random.choice(
        ['new'] + ['modern'] * 5 + ['ancient'] * 10)

    # physical isolation / remoteness
    data['isolation'] = random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5])
    # how culturally conservative it is
    data['insularity'] = random.randint(data['isolation'], 5)
    # isolation means lower max population
    data['population'] = random.randint(
        1000 * data['isolation'], int(10000000/(data['isolation'] ** 4)))

    # economy
    data['currency'] = lang.get_word('NN', 'currency')
    data['exchange_rate'] = abs(random.normalvariate(0, 10))


    # ----- GENDER
    data['genders'] = []
    gender_count = random.choice([2, 3, 5])
    if gender_count == 2:
        data['genders'] = [
            {'name': lang.get_word('NN', 'Male')},
            {'name': lang.get_word('NN', 'Female')}
        ]
    else:
        for _ in range(0, gender_count):
            data['genders'].append({'name': lang.get_word('NN', 'A gender')})


    # ------------------------ GRAPH DATA ------------------------- #
    ''' everything that's stored in neo4j gets loaded now. the following
    fields depend on what is set at this point. '''
    data.update(load_graph_data())


    # ----- RELIGION
    data['religion'] = religion.get_religion(data, lang)
    del data['divine_structure']
    del data['deity_form']
    del data['deity_form_secondary']
    del data['worship']

    # ----- FOOD
    data['cuisine'] = {
        'fruit': cuisine.fruit(data['climate']['name']),
        'tea': cuisine.tea(data['climate']['name']),
        'teacup': cuisine.teacup(data['primary_material'], data['motif'])
    }


    # ------- WILDLIFE
    data['wildlife'] = [{
        'name': lang.get_word('NNP', 'critter-%d' % i),
        'description': wildlife.animal(data['climate']['name'],
                                       data['terrain'])} \
            for i in range(0, 3)]

    # ------- FASHION
    data['body_mod'] = fashion.body_mod(gender_count, data['motif'])

    # ----- BUILDINGS
    lang.get_word('NN', 'teahouse')
    data['teahouse'] = {
        'name': lang.get_word('JJ', 'serene'),
        'description': architecture.building(data['primary_material'],
                                             data['secondary_material'])
    }


    # ------ NEWS
    # political climate
    politics = {
        # more or less a value between 0 and 1, the probability of
        # political upheaval on any given year
        'stability': abs(int(random.normalvariate(0, 2))) / 10,
        # either a term between 2 and 10 years, or life (80 years)
        'term_length': random.randint(2, 10) \
                if data['government'] == 'republic' else 80,
    }
    news = News(data['government'],
                gender_count,
                politics,
                lang)

    data['news'] = [news.generate_event(y) \
            for y in range(2010, datetime.now().year+1)]
    data['rulers'] = news.rulers


    # ------------------------ DISPLAY ITEMS ------------------------- #
    # these are the cards that get displayed about the city

    data['cards'] = [
        {
            'title': 'events',
            'cards': ['festival', 'holiday', 'event']
        },
        {
            'title': 'survival guide',
            'cards': ['transit', 'etiquette', 'more_etiquette']
        },
        {
            'title': 'sights',
            'cards':  data['building'] + \
                      ['teahouse', 'bathhouse', 'public_ovens']
        },
        {
            'title': 'learn',
            'cards': [
                'language', 'news', 'wildlife', 'religion',
                'government'] + (['gender'] if gender_count > 2 else [])
        },
        {
            'title': 'dine',
            'cards': ['fruit', 'bread', 'meal', 'tea']
        },
    ]

    # lookup words we'll need later. doing this now instead of on the fly
    # so that the lang library isn't a dependency
    lang.get_word('NN', 'region')
    lang.get_word('NN', 'market')
    lang.get_word('NN', 'fruit')
    lang.get_word('NN', 'tea')

    lang.get_word('NN', 'hello')
    lang.get_word('NN', 'thanks')
    lang.get_word('NN', 'goodbye')
    lang.get_word('NN', 'sorry')
    lang.get_word('NN', 'where')
    lang.get_word('NN', 'name')
    lang.get_word('PRP', 'i')

    data['dictionary'] = lang.dictionary

    return data

