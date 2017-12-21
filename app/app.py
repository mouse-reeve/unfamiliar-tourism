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

    # so that the template knows who it is, and that it's a card
    data['this_card'] = card
    return render_template('section.html', **data)


def collect_data(seed):
    ''' grab the data for a city and update it with changeable fields '''

    # ----- load the data from saved files or generate it
    try:
        if app.debug:
            raise(IOError)
        data = json.load(open(
            app.static_folder + '/datafiles/' + seed + '.json', 'r'))
    except IOError:
        data = generate_datafile(seed)
        if not data:
            return render_template('error.html', error='Database failure')

        # save a copy for future (re)loads
        filepath = app.static_folder + '/datafiles/' + seed + '.json'
        with open(filepath, 'w') as fp:
            json.dump(data, fp, default=lambda x: x.__dict__)

    random.seed(seed)

    # template utility functions
    data['color'] = generate_color

    # fields that change day-to-day
    data['get_exchange_rate'] = \
        lambda: calculate_exchange_rate(
            data['exchange_rate'],
            datetime.now().strftime('%Y%m%d'))

    month = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November',
             'December'][datetime.now().month - 1]
    data['weather'] = weather(data['climate'], month, seed, datetime.now().day)

    date = datetime.now() + timedelta(days=1)
    calendar_end = datetime.now() + timedelta(days=8)
    data['cards'][0]['cards'] = []
    while date < calendar_end:
        if date.strftime('%m%d') in data['calendar']['special']:
            data['cards'][0]['cards'] += \
                    data['calendar']['special'][date.strftime('%m%d')]
        date += timedelta(days=1)

    return data


# ---- Calculators for data fields that aren't fixed
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

