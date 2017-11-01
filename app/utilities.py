''' misc helper functions '''
import re

def format_text(text):
    ''' fix a/an type issues in tracery '''
    return re.sub(r'\b([Aa]) ([aeiouAEIOU])', r'\1n \2', text)


def get_latin(word, capitalize=False):
    ''' formatting foreign words '''
    text = ''
    word = word.__dict__ if not isinstance(word, dict) else word
    for syllable in word['lemma']:
        text = text + ''.join(l['latin'] for l in syllable)
    text = re.sub('/', '', text)

    if capitalize:
        return text[0].upper() + text[1:]
    return text
