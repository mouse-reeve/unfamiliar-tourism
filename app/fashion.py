''' what the natives wear '''
import tracery
from utilities import format_text
from wordlists import hard_materials

def body_mod(genders, motif):
    ''' describe a body modification '''
    pattern = {
        'circles': [
            'black bands of ink',
            'circles of interlocking lines and shapes',
            'chain-like patterns of broken rings',
            'a pattern like the splash of raindrops in a puddle',
            'radiating symmetrical designs like the tiles on Mosques',
            'concentric circles like staring eyes',
        ],
        'patterning': [
            'patterns almost like the trumps in a deck of playing cards',
            'precise, fine-lined patterns like expensive lace',
            'curving blocks of color',
            'abstract flourishes like you might find on a title page',
        ],
        'triangles': [
            'bands of equilateral triangles',
            'neat chevron lines of black ink'
        ],
        'squares': [
            'a grid of small, carefully drawn squares',
            'a row of rectangles symbolizing various life events',
            'diamond shaped blocks of black ink',
            'straight, dark lines, at odds with the curve of the body',
        ],
        'representation': [
            'depictions of leaves and flowers',
            'tangled vines as if the body was the trunk of an old tree',
            'shadows of animals',
            'blocks of text that tell strange and obscure stories',
        ]
    }
    rules = {
        'start': '#genders# #type# and #hair_mod#.',
        'genders': 'the women' if genders == 2 else 'people',
        'type': [
            'pierce their #pierce_spot# with #jewelry#',
            'tattoo their #tattoo_spot# with #motif#',
            '#hair_removal# their #hair_spot# bald'],
        'pierce_spot': ['lips', 'ears', 'noses', 'cheeks'],
        'tattoo_spot': [
            'hands', 'arms', 'faces', 'necks', 'bodies', 'palms',
            'chests', 'backs', 'torsos'],
        'motif': pattern[motif],
        'jewelry': [
            '#material# bangles', 'polished #material# spikes',
            'jewelry carved from #material#',
            'finely crafted #material# jewelry'],
        'hair_removal': ['pluck', 'shave'],
        'hair_spot': ['eyebrows', 'temples', 'faces'],
        'hair_mod': [
            'dye their hair #colors# with plant extracts, #hair_style#',
            'wear their hair cut short, #hair_style#',
            'sheer the hair to the scalp on parts of their head and ' \
                    'leave the rest long, #hair_style#',
            'indicate their social rank and status by the length of ' \
                    'their hair, #hair_style#',
            'braid their hair, #hair_style#'],
        'hair_style': [
            'pulled back with carved #material# combs',
            'letting it hang straight and loose',
            'slicked down against the scalp',
            'kept in place with colored ribbons',
            'worn short and bristling',
            'the wiry curls quite voluminous',
        ],
        'colors': ['black', 'unnatural colors', 'white', 'dark red'],
        'material': hard_materials,
    }

    grammar = tracery.Grammar(rules)
    sentence = grammar.flatten('#start#')

    return format_text(sentence)


