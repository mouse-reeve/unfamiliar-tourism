''' misc helper functions '''
import re

def format_text(text):
    ''' fix a/an type issues in tracery '''
    return re.sub(r'\b([Aa]) ([aeiouAEIOU])', r'\1n \2', text)
