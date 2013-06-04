from __future__ import division

from django.utils import simplejson
from django.utils.functional import lazy, Promise
from django.utils.encoding import force_unicode


class LazyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj
        
## A little generator to pluck out max values ##
def drill(item):
    if isinstance(item, int) or isinstance(item, float):
        yield item
    elif isinstance(item, list):
        for i in item:
            for result in drill(i):
                yield result
    elif isinstance(item, dict):
        for k,v in item.items():
            for result in drill(v):
                yield result

def get_max_value(nested_dicts):
    max_value = max([item for item in drill(nested_dicts)])
    return max_value

def get_ratio(num1, num2):
    '''requires ints or int-like strings'''
    return int(round(float(num1) / float(num2), 2)*100)


GEOGRAPHIES_MAP = {
    'nation': {
        'parent': None,
        'children': 'regions, zctas, urban areas, cbsas',
        'descendants': 'regions, zctas, urban areas, cbsas, divisions, states, school districts, congressional districts, urban growth areas, state legislative districts, public use microdata areas, places, counties, voting districts, traffic analysis zones, county subdivisions, subminor civil divisions, census tracts, block groups, census blocks'
    },
    'regions': {
        'parent': 'nation',
        'children': 'divisions',
        'descendants': 'divisions, states, school districts, congressional districts, urban growth areas, state legislative districts, public use microdata areas, places, counties, voting districts, traffic analysis zones, county subdivisions, subminor civil divisions, census tracts, block groups, census blocks'
    },
    'zctas': {
        'parent': 'nation',
        'children': None,
        'descendants': None,
    },
    'urban areas': {
        'parent': 'nation',
        'children': None,
        'descendants': None,
    },
    'cbsas': {
        'parent': 'nation',
        'children': None,
        'descendants': None,
    },
    'divisions': {
        'parent': 'regions',
        'children': 'states',
        'descendants': 'states, school districts, congressional districts, urban growth areas, state legislative districts, public use microdata areas, places, counties, voting districts, traffic analysis zones, county subdivisions, subminor civil divisions, census tracts, block groups, census blocks'
    },
    'states': {
        'parent': 'divisions',
        'children': 'school districts, congressional districts, urban growth areas, state legislative districts, public use microdata areas, places, counties',
        'descendants': 'school districts, congressional districts, urban growth areas, state legislative districts, public use microdata areas, places, counties, voting districts, traffic analysis zones, county subdivisions, subminor civil divisions, census tracts, block groups, census blocks'
    },
    'school districts': {
        'parent': 'states',
        'children': None,
        'descendants': None,
    },
    'congressional districts': {
        'parent': 'states',
        'children': None,
        'descendants': None,
    },
    'urban growth areas': {
        'parent': 'states',
        'children': None,
        'descendants': None,
    },
    'state legislative districts': {
        'parent': 'states',
        'children': None,
        'descendants': None,
    },
    'public use microdata areas': {
        'parent': 'states',
        'children': None,
        'descendants': None,
    },
    'places': {
        'parent': 'states',
        'children': None,
        'descendants': None,
    },
    'counties': {
        'parent': 'states',
        'children': 'voting districts, traffic analysis zones, county subdivisions, census tracts',
        'descendants': 'voting districts, traffic analysis zones, county subdivisions, subminor civil divisions, census tracts, block groups, census blocks'
    },
    'voting districts': {
        'parent': 'counties',
        'children': None,
        'descendants': None,
    },
    'traffic analysis zones': {
        'parent': 'counties',
        'children': None,
        'descendants': None,
    },
    'county subdivisions': {
        'parent': 'counties',
        'children': 'subminor civil divisions',
        'descendants': 'subminor civil divisions',
    },
    'subminor civil divisions': {
        'parent': 'county subdivisions',
        'children': None,
        'descendants': None,
    },
    'census tracts': {
        'parent': 'counties',
        'children': 'block groups',
        'descendants': 'block groups, census blocks',
    },
    'block groups': {
        'parent': 'census tracts',
        'children': 'census blocks',
        'descendants': 'census blocks',
    },
    'census blocks': {
        'parent': 'block groups',
        'children': 'census blocks',
        'descendants': 'census blocks',
    },
}