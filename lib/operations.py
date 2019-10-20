import json
from lib.entities import *


class Dataset(object):
    def __init__(self):
        self.couriers = []
        self.orders = []
        self.depots = []

    def read_json(self, fd):
        data = json.load(fd)
        for entry in data['couriers']:
            self.couriers.append(Courier(entry))

        for entry in data['orders']:
            self.orders.append(Order(entry))

        for entry in data['depots']:
            self.depots.append(Depot(entry))
