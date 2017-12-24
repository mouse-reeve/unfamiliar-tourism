''' all the information about a city in one json blob '''
import architecture
import events
import cuisine
import fashion
from graph import load_graph_data
from history import History
import religion
import wildlife

from foreigntongue import Language

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

    # economy
    data['currency'] = lang.get_word('NN', 'currency')
    data['exchange_rate'] = abs(random.normalvariate(0, 10))

    # ----- GENDER
    data['genders'] = []
    gender_count = random.choice([2, 3, 5])
    if gender_count == 2:
        data['genders'] = [
            {'name': lang.get_word('NN', 'male')},
            {'name': lang.get_word('NN', 'female')}
        ]
    else:
        for i in range(0, gender_count):
            data['genders'].append(
                {'name': lang.get_word('NN', 'gender-%d' % i)})


    # ------------------------ GRAPH DATA ------------------------- #
    ''' everything that's stored in neo4j gets loaded now. the following
    fields depend on what is set at this point. '''
    data.update(load_graph_data())

    # paris for art, san francisco for tech, tenochtitlan for death
    notabilities = [
        'visual_art',
        'performance',
        'death',
        'magic',
        'technology',
        'writing',
        'food',
        'education',
    ]
    if data['industry'] == 'weaving':
        notabilities += ['textiles'] * 5

    data['notability'] = random.choice(notabilities)


    # ----- RELIGION
    data['religion'] = religion.get_religion(data, lang)
    del data['divine_structure']
    del data['deity_form']
    del data['deity_form_secondary']
    del data['worship']

    # ----- HISTORY
    history = History(data, lang)
    data.update(history.generate_history())

    # ------------------------ DESCRIPTIONS ------------------------- #
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

    # ----- Calendar
    data['calendar'] = events.get_calendar(data['notability'])


    # ------------------------ DISPLAY ITEMS ------------------------- #
    # these are the cards that get displayed about the city

    data['cards'] = [
        {
            'title': 'events',
            'cards': [] # these will be populated on load in app.py
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

