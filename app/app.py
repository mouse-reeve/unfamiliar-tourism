''' simple http app using hotline library '''
from city import City
from cuisine import Cuisine
from datetime import datetime
from fashion import Fashion
from foreigntongue import Language, get_latin, get_ipa

from flask import Flask, redirect, render_template
import random

app = Flask(__name__)

city_cache = {}

def before_request():
    ''' temp code for testing because this version of flask
    isn't picking up template changes '''
    app.jinja_env.cache = {}
app.before_request(before_request)


@app.route('/')
def load_city():
    ''' send visitors to a particular seed '''
    seed = datetime.now().time().strftime('%H%M%S%f')
    return redirect('/%s' % seed)

@app.route('/<seed>')
def generate_city(seed=None):
    ''' generate a city '''
    if seed in city_cache and not app.debug:
        city_cache[seed][1] += 1
        return city_cache[seed][0]

    random.seed(seed)
    lang = Language()

    # ---- Name the country, language, and citites
    data = {'seed': seed}

    def get_placename(definition):
        ''' 25% of the time use a phrase as a place name '''
        if random.random() > 0.25:
            return lang.get_word('LOC', definition)

        words = [
            lang.get_word('JJ', 'swarming'),
            lang.get_word('NN', 'wasp')
        ]
        definition += '; literally, "swarming wasps"'
        return lang.get_phrase('LOC', words, definition)

    data['country'] = get_placename(
        'That country\'s name; ' + \
        'the lands and people of that nation')

    city_definition = 'A city in ' + get_latin(data['country'])
    data['city'] = {
        'name': get_placename(city_definition)
    }

    data['translate'] = lambda w, pos: lang.get_word(pos, w)

    data['language'] = lang.get_word(
        'NNP',
        'The official language of ' + get_latin(data['country']) + \
           ', spoken in ' + get_latin(data['city']['name']))


    # GENDER
    data['genders'] = []
    gender_count = random.choice([2, 3, 5])
    if gender_count == 2:
        data['genders'] = [
            {
                'name': lang.get_word('NN', 'male'),
                'pronoun': lang.get_word('PRP',
                                         'Male pronoun'),
            }, {
                'name': lang.get_word('NN', 'female'),
                'pronoun': lang.get_word('PRP',
                                         'Female pronoun'),
            }
        ]
    else:
        for _ in range(0, gender_count):
            data['genders'].append({
                'name': lang.get_word('NN', 'a gender'),
                'pronoun': lang.get_word(
                    'PRP',
                    'a gender pronoun'),
            })


    # ------- Graph data - climate, info, lotsa stuff
    city = City()
    if city.error:
        return render_template('error.html', error='Database failure')

    data.update(city.data)

    # allow the weather to be calculated on the fly in the templates
    app.jinja_env.globals.update(get_weather=city.weather)


    # ----- RELIGION
    data['religion'] = {}
    data['religion']['name'] = lang.get_word(
        'NNP',
        'the religion of ' + get_latin(data['country'])
    )

    god_definition = 'a local god of the %s religion' % \
                     get_latin(data['religion']['name'])

    data['religion']['gods'] = []
    god_count = 2

    # you need a lot of gods to pull off a divine hierarchy
    if data['divine_structure'] == 'heirarchical':
        god_count += 2
    god_count += abs(int(random.normalvariate(2, 2)))

    for _ in range(god_count):
        data['religion']['gods'].append(
            lang.get_word('NNP', god_definition))

    if data['divine_structure'] == 'heirarchical':
        data['religion']['gods'] = \
                create_pantheon_hierarchy(data['religion']['gods'])

    # ------ FOOD
    cuisine = Cuisine(data['climate'],
                      data['secondary_material'],
                      data['motif'])

    data['cuisine'] = {
        'tea': {
            'description': cuisine.tea(),
            'cup_description': cuisine.teacup(),
            'name': lang.get_word('NN', 'tea')
        },
        'fruits': []
    }
    for _ in range(0, 3):
        data['cuisine']['fruits'].append(
            lang.get_word('NNP', cuisine.fruit())
            )


    # fashion
    fashion = Fashion(gender_count, data['climate'], data['motif'])
    data['body_mod'] = fashion.body_mod()



    data['dictionary'] = lang.dictionary
    rendered = render_template('index.html', **data)
    city_cache[seed] = [rendered, 1]
    return rendered


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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
