''' facts about a city '''
from climates import climates

from py2neo import authenticate, Graph
from py2neo.packages.httpstream.http import SocketError
from py2neo.database.status import Unauthorized, GraphError
import random
import settings

user = settings.NEO4J_USER
password = settings.NEO4J_PASS
auth = authenticate('localhost:7474', user, password)

try:
    graph = Graph()
except (SocketError, Unauthorized, GraphError) as e:
    graph = None

class City(object):
    ''' creates a city based on interrelated traits '''

    def __init__(self):
        self.error = False
        self.graph = graph
        if not self.graph:
            try:
                self.graph = Graph()
            except (SocketError, Unauthorized, GraphError):
                self.error = True
                return
        self.data = {}

        # location, climate, and architecture
        query = '''
        match (terr:terrain)--(c:climate)--(t:city_type)--(m:primary_material)--(m2:secondary_material)--(x:motif)
        where (terr)--(t) and (c)--(m) and (m)--(:stories)--(t)
        return * skip %d limit 1
        ''' % random.randint(0, 9520 - 1)


        from datetime import datetime
        print('queries starting')
        now = datetime.now()
        result = self.graph.run(query)

        data = result.data()

        self.add_data(data)

        # the number of options for this query can vary, so get the count
        # then the resul
        query = '''
        match (i:industry)--(m:primary_material {name: '%s'})--(s:stories)--(t:city_type {name: '%s'})
        with i, m, s, t optional match (b:building)--(i)
        ''' % (self.data['primary_material'], self.data['city_type'])
        result = self.graph.run(query + 'return count(*)')
        count = result.evaluate()

        query = query + 'return b, i, s skip %d limit 1' \
                % random.randint(0, count - 1)
        result = self.graph.run(query)
        data = result.data()
        self.add_data(data)

        climate_name = self.data['climate']
        self.data['climate'] = climates[self.data['climate']]
        self.data['climate']['id'] = climate_name

        # government, religion, and public spaces
        query = '''
        match (d:diety_form)--(d2:diety_form_secondary),
              (s:divine_structure),
              (n:worship)--(b:building), (n2:worship)--(b1:building), (n3:worship)--(b2:building),
              (b3:building)--(g:government)--(e:exchange)
        return distinct * skip %d limit 1 ''' % random.randint(0, 82944 - 1)
        result = self.graph.run(query)
        print ('\n run time (sec): ', (datetime.now() - now).total_seconds())
        data = result.data()
        self.add_data(data)


    def add_data(self, data):
        ''' process in neo4j results '''
        for item in data[0].values():
            if not item:
                # optional match on building can produce a null
                continue
            label = list(item.labels())[0]
            item = item.properties['name']
            if label in self.data:
                if not isinstance(self.data[label], list):
                    self.data[label] = [self.data[label], item]
                else:
                    self.data[label].append(item)
            else:
                self.data[label] = item

