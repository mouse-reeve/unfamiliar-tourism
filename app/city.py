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
        match (p:position)--(c:climate)--(t:city_type)--(m:primary_material)--(m2:secondary_material)--(x:motif),
        (m)--(s:stories)
        where (p)--(t) and (c)--(m) and (t)--(s)
        return * skip %d limit 1
        ''' % random.randint(0, 10080)
        result = self.graph.run(query)
        data = result.data()

        self.add_data(data)
        self.data['climate'] = climates[self.data['climate']]

        # government, religion, and public spaces
        query = '''
        match (d:diety_form)--(d2:diety_form_secondary),
              (s:divine_structure),
              (n:worship), (n2:worship), (n3:worship),
              (g:government)--(e:exchange)
        return * skip %d limit 1 ''' % random.randint(0, 196608)
        result = self.graph.run(query)
        data = result.data()
        self.add_data(data)


    def add_data(self, data):
        ''' process in neo4j results '''
        for item in data[0].values():
            label = list(item.labels())[0]
            item = item.properties['name']
            if label in self.data:
                if not isinstance(self.data[label], list):
                    self.data[label] = [self.data[label], item]
                else:
                    self.data[label].append(item)
            else:
                self.data[label] = item



    def weather(self, month):
        ''' determine the weather for a given date '''
        # [temp, rainy days, snowy days, humidity]
        stats = self.data['climate']['stats'][month]

        temp_deviation = self.data['climate']['temp_range']/2
        temp = random.normalvariate(stats[0], temp_deviation)
        deviation = abs(temp - stats[0]) / temp_deviation

        precipitation = False
        if stats[2] and random.random() > stats[2]/30.0 * 2:
            deviation = 1 - ((stats[2] / 30.0) * 2)
            precipitation = 'snow'
        elif stats[1] and random.random() > stats[1]/30.0:
            deviation = 1 - ((stats[1] / 30.0) * 2)
            precipitation = 'rain'

        temps = ['freezing', 'cold', 'warm', 'hot', 'blistering', 'blistering']
        temp_desc = temps[0] if temp < 0 else temps[int((temp + 5)/10)]

        report = {
            'temp': temp,
            'temp_description': temp_desc,
            'humidity': stats[3],
            'precipitation': precipitation,
            'deviation': deviation,
            'climate': self.data['climate']['name'],
        }
        return report
