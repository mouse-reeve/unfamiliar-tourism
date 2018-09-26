#!/bin/bash

seed=$1

python generator/generator.py $seed

ocean=0
if [[ $(jq '.terrain' cities/static/data/$seed/city.json) == 'ocean' ]]; then
    ocean=1
fi
echo "file:///Users/mouse/Personal/maps/index.html?seed=3712&perterbation=0.3&elevationrange=1&riverwidth=1&min=20"
echo "file:///Users/mouse/Personal/skyline-sketch/index.html?seed=5012&background=mountains&sky=block&composition=hill&palette=split&hue=86&saturation=10&lightness=80"
