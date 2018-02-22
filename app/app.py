''' City generator websever app '''
from climates import weather
from utilities import get_latin
from data import generate_datafile

from flask import Flask, redirect, render_template
from datetime import datetime, timedelta
import json
import random
import re

app = Flask(__name__)


@app.route('/')
@app.route('/city')
def request_new_city():
    ''' send visitors to a particular seed '''
    seed = datetime.now().time().strftime('%H%M%S%f')
    return redirect('/city/%s' % seed)


@app.route('/city/<seed>')
def load_city(seed):
    ''' create the webpage from the datafile '''
    clean_seed = re.sub(r'(?![a-zA-Z0-9]).', '', seed)
    if not clean_seed:
        clean_seed = datetime.now().time().strftime('%H%M%S%f')

    if seed != clean_seed:
        return redirect('/%s' % clean_seed)

    seed = clean_seed
    # attempt to load existing datafile for seed
    data = collect_data(seed)
    if data == 'oops':
        return render_template('error.html', error='Database failure')

    return render_template('index.html', **data)


@app.route('/city/<seed>/datafile')
def load_city_data(seed):
    ''' create the webpage from the datafile '''
    # attempt to load existing datafile for seed
    data = collect_data(seed)

    return json.dumps(data, default=lambda x: x.__dict__)


@app.route('/city/<seed>/<card>')
def load_card(seed, card):
    ''' load just a single card for the city '''
    data = collect_data(seed)

    # so that the template knows who it is, and that it's a card
    data['this_card'] = card
    return render_template('section.html', **data)

@app.errorhandler(404)
def page_not_found(_):
    ''' catch bad paths '''
    return render_template('error.html', error='Not found'), 404


def collect_data(seed):
    ''' grab the data for a city and update it with changeable fields '''

    # ----- load the data from saved files or generate it
    try:
        data = json.load(open(
            app.static_folder + '/datafiles/' + seed + '.json', 'r'))
    except IOError:
        data = generate_datafile(seed)
        if not data:
            return render_template('error.html', error='Database failure'), 500

        if not app.debug:
            # save a copy for future (re)loads
            filepath = app.static_folder + '/datafiles/' + seed + '.json'
            with open(filepath, 'w') as fp:
                json.dump(data, fp, default=lambda x: x.__dict__)

    random.seed(seed)

    # template utility functions
    data['color'] = lambda bg=True: generate_color(data['climate']['id'],
                                                   background=bg)

    # fields that change day-to-day
    data['get_exchange_rate'] = \
        lambda: calculate_exchange_rate(
            data['exchange_rate'],
            datetime.now().strftime('%Y%m%d'))

    data['weather'] = weather(data['climate'], seed, datetime.utcnow())
    data['weather']['forecast'] = []

    forecast_date = datetime.utcnow()
    for _ in range(0, 7):
        data['weather']['forecast'].append(
            weather(data['climate'],
                    seed,
                    forecast_date))
        forecast_date += timedelta(days=1)

    return data


# ---- Calculators for data fields that aren't fixed
def generate_color(climate, background=True):
    ''' a hex color '''
    hue = list(range(0, 360))

    if climate in ['hot_desert', 'arid', 'semi_arid']:
        hue += (30 * list(range(345, 360))) + \
               (30 * list(range(0, 60)))
    elif climate in ['oceanic', 'subpolar_oceanic', 'subarctic']:
        hue += (30 * list(range(180, 260)))
    elif climate in ['tropical_rainforest', 'tropical_monsoon']:
        hue += (30 * list(range(85, 160)))


    hue = random.choice(hue)

    saturation = '40%' if background else '45%'
    brightness = '70%' if background else '30%'
    color = 'hsl(%d, %s, %s)' % (hue, saturation, brightness)
    return color


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


@app.template_filter('capitalize')
def capitalize_filter(word):
    ''' template filter for capitalizing a sentence'''
    return word[0].upper() + word[1:]


@app.template_filter('allcaps')
def caps_filter(word):
    ''' template filter for ALL CAPS '''
    return word.upper()


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

    # trim any unusued columns so that cards use available space
    grouped = [g for g in grouped if g]
    return grouped


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

