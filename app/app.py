''' simple http app using hotline library '''
from city import City
from cuisine import Cuisine
from datetime import datetime
from fashion import Fashion
from foreigntongue import Language, get_latin, get_ipa

from flask import Flask, redirect, render_template
import random
from random import Random

app = Flask(__name__)

def before_request():
    ''' temp code for testing because this version of flask
    isn't picking up template changes '''
    app.jinja_env.cache = {}
app.before_request(before_request)


@app.route('/')
def load_city():
    ''' send visitors to a particular seed '''
    seed = datetime.now().time().strftime('%H%M%S%f')
    # TODO:
    # 1. create a temporary template for the city (for nojs)
    # 2. render the loading screen at '/' with ajax to receive callback
    #    from generation script when city is ready
    # 3. run generation script that creates actual city template
    return redirect('/%s' % seed)


@app.route('/<seed>')
def generate_city(seed=None):
    ''' generate a city '''
    color_random = Random()
    color_random.seed(seed)

    random.seed(seed)
    lang = Language()

    # ---- Name the city, country, and language
    data = {'seed': seed}

    data['country'] = lang.get_word(
        'LOC',
        'That country\'s name; ' + \
        'the lands and people of that nation')

    city_definition = 'A city in ' + get_latin(data['country'])
    data['city'] = {
        'name': lang.get_word('LOC', city_definition)
    }

    data['translate'] = lang.get_word

    lang_definition = 'The official language of ' + \
                       get_latin(data['country']) + \
                      ', spoken in ' + get_latin(data['city']['name'])
    data['language'] = {
        'name': lang.get_word('NNP', lang_definition),
        'stats': lang.get_stats()
    }


    # ------- Graph data - climate, info, lotsa stuff
    city = City()
    if city.error:
        return render_template('error.html', error='Database failure')

    data.update(city.data)
    month = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November',
             'December'][datetime.now().month]
    data['weather'] = city.weather(month, seed, datetime.now().day)

    # ------ Factoids
    data['year_founded'] = 1987
    data['history'] = [
        {'description': 'The city is founded', 'year': data['year_founded']},
        {'description': 'Barbarians sack the palace', 'year': 1995},
    ]

    # physical isolation
    data['isolation'] = random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5])
    # how culturally conservative it is
    data['insularity'] = random.randint(data['isolation'], 5)
    # isolation means lower max population
    data['population'] = random.randint(
        1000 * data['isolation'], int(10000000/(data['isolation'] ** 4)))

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
        'the religion of ' + get_latin(data['country'])
    )

    god_definition = 'a god of the %s religion' % \
                     get_latin(data['religion']['name'])

    data['religion']['gods'] = []
    god_count = 2

    # you need a lot of gods to pull off a divine hierarchy
    if data['divine_structure'] == 'heirarchical':
        god_count += 2
    god_count += abs(int(random.normalvariate(2, 2)))

    data['religion']['god_count'] = god_count

    for _ in range(god_count):
        data['religion']['gods'].append(
            lang.get_word('NNP', god_definition))

    if data['divine_structure'] == 'heirarchical':
        data['religion']['gods'] = \
                create_pantheon_hierarchy(data['religion']['gods'])

    # note on structure:
    # "multifaceted" means that various gods are faces of a single divinity
    # "various" means that gods exist discreetly
    # "heirarchical" means they exist discreetly and with some more important
    data['religion']['divine_structure'] = data['divine_structure']
    data['religion']['worship'] = data['worship']
    data['religion']['diety_forms'] = [data['diety_form'],
                                       data['diety_form_secondary']]
    del data['divine_structure']
    del data['diety_form']
    del data['diety_form_secondary']
    del data['worship']

    # ------ FOOD
    cuisine = Cuisine(data['climate'],
                      data['secondary_material'],
                      data['motif'])

    data['cuisine'] = {
        'fruit': cuisine.fruit()
    }

    # fashion
    fashion = Fashion(gender_count, data['climate'], data['motif'])
    data['body_mod'] = fashion.body_mod()


    # ------- City-specific cards to display
    data['cards'] = [
        {
            'title': 'learn',
            'cards': ['weather', 'language', 'religion', 'government']
        }, {
            'title': 'sights',
            'cards': ['fruit']
        }, {
            'title': 'dine',
            'cards': ['fruit', 'fruit', 'fruit']
        }, {
            'title': 'survival guide',
            'cards': ['transit', 'etiquette', 'transit', 'transit', 'transit',
                      'transit', 'transit', 'transit', 'transit', 'transit']
        }, {
            'title': 'seasonal',
            'cards': ['festival', 'holiday', 'event']
        }
    ]
    if len(data['genders']) > 2:
        data['cards'][0]['cards'].append('gender')

    # realistically, there could be temples/shrines for various gods,
    # and this should reflect the divine structure
    data['cards'][1]['cards'] += data['religion']['worship']

    # lookup words we'll need later. doing this now instead of on the fly
    # in the partials to keep the state of random predictable, and not
    # contingent on the order in which the partials are added (or whatever)
    lang.get_word('NN', 'market')
    lang.get_word('NN', 'fruit')
    lang.get_word('NN', 'hello')
    lang.get_word('NN', 'where')
    lang.get_word('NN', 'name')
    lang.get_word('NN', 'sorry')
    lang.get_word('NN', 'thanks')
    lang.get_word('NN', 'goodbye')
    lang.get_word('NN', 'region')

    data['dictionary'] = lang.dictionary

    data['color'] = lambda: generate_color(color_random)
    return render_template('index.html', **data)


def generate_color(rand):
    ''' a hex color '''
    return '#' + ''.join(hex(rand.randint(10, 13))[2:] for _ in range(0, 3))

def create_pantheon_hierarchy(gods):
    ''' arrange gods into a hierarchical pantheon
    There will be at least two tiers '''
    # min number of gods is 4
    pantheon = []
    top_max = 1 + int(len(gods) * 0.3)
    top = random.randint(1, top_max)
    pantheon[0] = gods[:top]
    # only create three tiers if there are enough gods
    if len(gods) - top < 5:
        pantheon[1] = gods[top:]
    else:
        mid_max = 1 + int((len(gods) - top_max) * 0.4)
        pantheon[1] = gods[top:mid_max]
        pantheon[2] = gods[mid_max:]

    return pantheon


@app.template_filter('ipa')
def ipa_filter(word):
    ''' template filter for formatting foreign words '''
    return get_ipa(word)


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
    return [cards[:per_column],
            cards[per_column:(per_column * 2)],
            cards[per_column * 2:]]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

