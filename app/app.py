''' City generator websever app '''
from architecture import Architecture
from city import City
from climates import weather
from cuisine import Cuisine
from datetime import datetime
from fashion import Fashion
from foreigntongue import Language
from news import News
from utilities import get_latin

from flask import Flask, redirect, render_template
import json
import random
import re

app = Flask(__name__)

def before_request():
    ''' temp code for testing because this version of flask
    isn't picking up template changes '''
    app.jinja_env.cache = {}
app.before_request(before_request)


@app.route('/')
def request_new_city():
    ''' send visitors to a particular seed '''
    seed = datetime.now().time().strftime('%H%M%S%f')
    return redirect('/%s' % seed)


@app.route('/<seed>')
def load_city(seed):
    ''' create the webpage from the datafile '''
    # attempt to load existing datafile for seed
    data = collect_data(seed)

    return render_template('index.html', **data)


@app.route('/<seed>/<card>')
def load_card(seed, card):
    ''' load just a single card for the city '''
    data = collect_data(seed)
    data['this_card'] = card
    return render_template('section.html', **data)


def collect_data(seed):
    ''' grab the data for a city and update it with changeable fields '''
    try:
        if app.debug:
            raise(IOError)
        data = json.load(open(
            app.static_folder + '/datafiles/' + seed + '.json', 'r'))
    except IOError:
        data = generate_datafile(seed)

    random.seed(seed)

    # the last couple things that are generated on the fly
    data['color'] = generate_color
    data['get_exchange_rate'] = \
        lambda: calculate_exchange_rate(
            data['exchange_rate'],
            datetime.now().strftime('%Y%m%d'))
    month = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November',
             'December'][datetime.now().month]

    data['weather'] = weather(data['climate'], month, seed, datetime.now().day)
    return data


def generate_datafile(seed):
    ''' generate a city '''

    random.seed(seed)
    lang = Language()

    # ---- Name the city, country, and language
    data = {'seed': seed}

    data['country'] = lang.get_word(
        'LOC',
        'That country\'s name; ' + \
        'the lands and people of that nation')

    city_definition = 'A city in ' + latin_filter(data['country'])
    data['city'] = {
        'name': lang.get_word('LOC', city_definition)
    }

    lang_definition = 'The official language of ' + \
                       latin_filter(data['country']) + \
                      ', spoken in ' + latin_filter(data['city']['name'])
    data['language'] = {
        'name': lang.get_word('NNP', lang_definition),
        'stats': lang.get_stats()
    }


    # ------- Graph data - climate, info, lotsa stuff
    city = City()
    if city.error:
        return render_template('error.html', error='Database failure')

    data.update(city.data)


    # ------ Factoids
    data['city_age'] = random.choice(['new', 'modern', 'ancient'])

    # physical isolation
    data['isolation'] = random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5])
    # how culturally conservative it is
    data['insularity'] = random.randint(data['isolation'], 5)
    # isolation means lower max population
    data['population'] = random.randint(
        1000 * data['isolation'], int(10000000/(data['isolation'] ** 4)))


    # ------- ECONOMY
    data['currency'] = lang.get_word('NN', 'currency')
    data['exchange_rate'] = abs(random.normalvariate(0, 10))


    # ------- GENDER
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


    # ------- RELIGION
    data['religion'] = {}
    data['religion']['name'] = lang.get_word(
        'NNP',
        'the religion of ' + latin_filter(data['country'])
    )

    god_definition = 'a god of the %s religion' % \
                     latin_filter(data['religion']['name'])

    data['religion']['gods'] = []
    god_count = 2

    # you need a lot of gods to pull off a divine hierarchy
    if data['divine_structure'] == 'hierarchical':
        god_count += 2
    god_count += abs(int(random.normalvariate(2, 20)))

    data['religion']['god_count'] = god_count

    for _ in range(god_count):
        data['religion']['gods'].append(
            lang.get_word('NNP', god_definition))

    if data['divine_structure'] == 'hierarchical':
        data['religion']['gods'] = \
                create_pantheon_hierarchy(data['religion']['gods'])

    # note on structure:
    # "multifaceted" means that various gods are faces of a single divinity
    # "various" means that gods exist discreetly
    # "hierarchical" means they exist discreetly and with some more important
    data['religion']['divine_structure'] = data['divine_structure']
    data['religion']['worship'] = data['worship']
    data['religion']['deity_forms'] = [data['deity_form'],
                                       data['deity_form_secondary']]
    del data['divine_structure']
    del data['deity_form']
    del data['deity_form_secondary']
    del data['worship']

    # ------ FOOD
    cuisine = Cuisine(data['climate'],
                      data['secondary_material'],
                      data['motif'])

    data['cuisine'] = {
        'fruit': cuisine.fruit(),
        'tea': cuisine.tea(),
        'teacup': cuisine.teacup()
    }

    # ------- FASHION
    fashion = Fashion(gender_count, data['climate'], data['motif'])
    data['body_mod'] = fashion.body_mod()

    # ----- BUILDINGS
    architecture = Architecture(data['city_type'], data['primary_material'],
                                data['secondary_material'], data['motif'])
    data['architecture'] = {
        'temple': architecture.building()
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

    # ------- City-specific cards to display
    data['cards'] = [
        {
            'title': 'learn',
            'cards': ['language', 'wildlife', 'news', 'religion', 'government']
        }, {
            'title': 'sights',
            'cards':  data['building'] + \
                      ['teahouse', 'bathhouse', 'public_ovens']
        }, {
            'title': 'dine',
            'cards': ['fruit', 'bread', 'meal', 'tea']
        }, {
            'title': 'survival guide',
            'cards': ['transit', 'etiquette', 'more_etiquette']
        }, {
            'title': 'seasonal',
            'cards': ['festival', 'holiday', 'event']
        }
    ]

    if len(data['genders']) > 2:
        data['cards'][0]['cards'].append('gender')


    # lookup words we'll need later. doing this now instead of on the fly
    # so that the lang library isn't a dependency
    lang.get_word('NN', 'region')
    lang.get_word('NN', 'market')
    lang.get_word('NN', 'fruit')
    lang.get_word('NN', 'tea')

    lang.get_word('NN', 'hello')
    lang.get_word('NN', 'thanks')
    lang.get_word('NN', 'goodbye')

    data['dictionary'] = lang.dictionary

    filepath = app.static_folder + '/datafiles/' + seed + '.json'

    # save a copy for future (re)loads
    with open(filepath, 'w') as fp:
        json.dump(data, fp, default=lambda x: x.__dict__)
    return data


def create_pantheon_hierarchy(gods):
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


# ---- Calculators for variable data fields
def generate_color():
    ''' a hex color '''
    return '#' + ''.join(hex(random.randint(10, 13))[2:] for _ in range(0, 3))


def calculate_exchange_rate(base_rate, date):
    ''' fluxuating exchange rate '''
    rand_state = random.getstate()
    random.seed(date)
    rate = abs(random.normalvariate(base_rate, 3))
    random.setstate(rand_state)
    return '{0:.2f}'.format(rate)


# ---- Template filters
@app.template_filter('ipa')
def ipa_filter(word):
    ''' template filter for formatting foreign words '''
    text = ''
    word = word.__dict__ if not isinstance(word, dict) else word
    for syllable in word['lemma']:
        text = text + ''.join(l['IPA'] for l in syllable)
    return re.sub('/', '', text)


@app.template_filter('latin')
def latin_filter(word):
    ''' template filter for formatting foreign words '''
    return get_latin(word)


@app.template_filter('number_format')
def number_format_filter(n):
    ''' 1,000,000 not 1000000 '''
    words = [
        'zero', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight', 'nine'
    ]

    if n < 10:
        return words[n]
    return '{:,}'.format(n)


@app.template_filter('group_cards')
def group_cards_filter(cards, column_count=3):
    ''' create columns for a card grid '''
    per_column = int(len(cards) / column_count) or 1
    grouped = [cards[:per_column],
               cards[per_column:(per_column * 2)],
               cards[per_column * 2:per_column * 3]]
    # add any remaining cards to a stack at random
    for remaining in cards[per_column * 3:]:
        grouped[random.randint(1, 2)].append(remaining)
    return grouped


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

