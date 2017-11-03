''' facts about a city '''
from climates import climates
import settings

from datetime import datetime
from py2neo import authenticate, Graph
from py2neo.packages.httpstream.http import SocketError
from py2neo.database.status import Unauthorized, GraphError
import random

user = settings.NEO4J_USER
password = settings.NEO4J_PASS
auth = authenticate('localhost:7474', user, password)

def load_graph_data():
    ''' run hella queries. they're split up to optimize query time '''
    try:
        graph = Graph()
    except (SocketError, Unauthorized, GraphError):
        return False
    data = {}

    # for benchmarking query time
    now = datetime.now()

    # location, climate, and architecture
    query = '''
    match (terr:terrain)--(c:climate)--(t:city_type)--(m:primary_material)--(m2:secondary_material)--(x:motif)
    where (terr)--(t) and (c)--(m) and (m)--(:stories)--(t)
    return * skip %d limit 1
    ''' % random.randint(0, 9520 - 1)

    result = graph.run(query)
    new_data = result.data()
    data = add_data(data, new_data)

    # the number of options for this query can vary, so get the count
    # then the result
    query = '''
    match (i:industry)--(m:primary_material {name: '%s'})--(s:stories)--(t:city_type {name: '%s'})
    with i, m, s, t optional match (b:building)--(i)
    ''' % (data['primary_material'], data['city_type'])
    result = graph.run(query + 'return count(*)')
    count = result.evaluate()

    query = query + 'return b, i, s skip %d limit 1' \
            % random.randint(0, count - 1)
    result = graph.run(query)
    new_data = result.data()
    data = add_data(data, new_data)

    climate_name = data['climate']
    data['climate'] = climates[data['climate']]
    data['climate']['id'] = climate_name

    # government, religion, and public spaces
    query = '''
    match (d:deity_form)--(d2:deity_form_secondary)
    return * skip %d limit 1 ''' % random.randint(0, 17 - 1)
    result = graph.run(query)
    new_data = result.data()
    data = add_data(data, new_data)

    query = '''
    match (s:divine_structure)
    return * skip %d limit 1 ''' % random.randint(0, 3 - 1)
    result = graph.run(query)
    new_data = result.data()
    data = add_data(data, new_data)

    query = '''
    match (n:worship)--(b:building),
          (n1:worship)--(b1:building),
          (n2:worship)--(b2:building)
    return distinct * skip %d limit 1 ''' % random.randint(0, 2184 - 1)
    result = graph.run(query)
    new_data = result.data()
    data = add_data(data, new_data)

    query = '''
    match (b:building)--(g:government)
    return * skip %d limit 1 ''' % random.randint(0, 6 - 1)
    result = graph.run(query)
    new_data = result.data()

    print ('\n run time (sec): ', (datetime.now() - now).total_seconds())

    return add_data(data, new_data)


def add_data(data, new_data):
    ''' process in neo4j results '''
    for item in new_data[0].values():
        if not item:
            # optional match on building can produce a null
            continue
        label = list(item.labels())[0]
        item = item.properties['name']
        if label in data:
            if not isinstance(data[label], list):
                data[label] = [data[label], item]
            else:
                data[label].append(item)
        else:
            data[label] = item
    return data

