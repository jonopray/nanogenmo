from __future__ import unicode_literals
from os.path import abspath, join, dirname
import random

full_path = lambda filename: abspath(join(dirname(__file__), filename))

FILES = {
    'first:male': full_path('dist.male.first'),
    'first:female': full_path('dist.female.first'),
    'last': full_path('dist.all.last'),
}

FILE_DATA = {}

for key in FILES:
    file_contents = []
    with open(FILES[key]) as name_file:
        for line in name_file:
            file_contents.append(line.split())
    FILE_DATA[FILES[key]] = file_contents

def get_name(filename):
    selected = random.random() * 90
    for name_values in FILE_DATA[filename]:
        name, _, cummulative, _ = name_values
        if float(cummulative) > selected:
            return name
    return ""  # Return empty string if file is empty

def get_first_name(gender=None):
    if gender is None:
        gender = random.choice(('male', 'female'))
    if gender not in ('male', 'female'):
        raise ValueError("Only 'male' and 'female' are supported as gender")
    return get_name(FILES['first:%s' % gender]).capitalize()

def get_last_name():
    return get_name(FILES['last']).capitalize()