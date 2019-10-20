# -*- coding: utf-8 -*-

import json
from random import randint
from copy import copy
#from scipy.stats import rv_discrete

START_TIME = 360
PAYMENT_COURIER = 2


class PointTime(object):
    def __init__(self, id, x, y, start=0, end=1440, type='pickup'):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.start = start
        self.end = end

    def dist_to(self, point):
        return 10 + abs(self.x - point.x) + abs(self.y - point.y)

    def is_valid(self):
        return self.start <= self.end

    def in_time(self, t):
        return self.start <= t <= self.end


class Courier(object):
    def __init__(self, json_data):
        self.id = json_data['courier_id']
        self.point = PointTime(json_data['courier_id'], json_data['location_x'], json_data['location_y'])
        self.time = 360

    def set_point(self, point_, time_):
        self.point = point_
        self.time = time_
    
    def cost(self, order):
        finish_time = self.can_deliver(order)
        if finish_time == -1:
            raise Exception('beda')
         
        return (finish_time - self.time) * PAYMENT_COURIER

    # Возвращает прибыль компании от похода курьера
    def profit(self, order):
        finish_time = self.can_deliver(order)
        if finish_time == -1:
            return -1
        
        return order.payment - self.cost(order)

    # Возвращает время прибытие товара или -1, если не успеет
    def can_deliver(self, order):
        time_to_aim = self.point.dist_to(order.pickup_point) + self.time
        
        if time_to_aim >= order.pickup_point.end:  # ??? >= !!!!!!!!!!!!!!!!!!!!!!!
            return -1
        
        new_time = max(time_to_aim, order.pickup_point.start)

        time_to_finish = new_time + order.time_deliver
        
        if time_to_finish >= order.dropoff_point.end:  # ??? >= !!!!!!!!!!!!!!!!!!!!
            return -1

        return max(time_to_finish, order.dropoff_point.start)


class Order(object):
    def __init__(self, json_data):
        self.id = json_data['order_id']
        self.pickup_point = PointTime(json_data['pickup_point_id'], json_data['pickup_location_x'],
                                      json_data['pickup_location_y'], json_data['pickup_from'],
                                      json_data['pickup_to'], type='pickup')

        self.dropoff_point = PointTime(json_data['dropoff_point_id'], json_data['dropoff_location_x'],
                                      json_data['dropoff_location_y'], json_data['dropoff_from'],
                                       json_data['dropoff_to'], type='dropoff')

        self.payment = json_data['payment']
        
        self.time_deliver = self.pickup_point.dist_to(self.dropoff_point)


class Depot(object):
    def __init__(self, json_data):
        self.id = json_data['point_id']
        self.point = PointTime(json_data['point_id'], json_data['location_x'], json_data['location_y'])


class Event(object):
    def __init__(self, courier, action, order, point):
        self.courier = courier
        self.action = action
        self.order = order
        self.point = point

    def get_dict(self):
        res = {"courier_id": self.courier.id,
               "action": self.action,
               "order_id": self.order.id,
               "point_id": self.point.id}
        return res


class State(object):
    def __init__(self, dataset):
        self.orders = dataset.orders
        self.max_money = sum([order.payment for order in self.orders])
        self.free_orders = []
        self.depots = dataset.depots
        self.couriers = dataset.couriers
        self.paths = [[] for i in range(10001)]

        for courier in self.couriers:
            if len(self.paths[courier.id]) == 0:
                point_time = PointTime(courier.id, courier.point.x, courier.point.y)
                self.paths[courier.id].append(Event(courier, 'start', Order, point_time))

        for order in self.orders:
            self.free_orders.append(order)

    def energy(self):
        """
        Aggregates all salaries and profits and returns the substraction.
        :return: returns the pure profit()
        """
        profit = 0
        salary = 0

        for path in self.paths:
            for event in path[1:]:
                if event.order is not None:
                    try:
                        profit += event.order.payment
                    except BaseException:
                        print(event.action)

            end_time = self.end_day_time(path)
            if end_time == -1:
                return self.max_money
            salary += 2 * (end_time - START_TIME)

        return self.max_money - profit / 2 + salary

    def get_neighbour(self):
        new_state = copy(self)
        probabilities = [0.5, 0.5]
        mutations = [new_state.delete_order, new_state.add_order]
        distribution = rv_discrete(values=(range(len(mutations)), probabilities))
        while True:
            current_mutation = mutations[distribution.rvs()]
            if current_mutation():
                break

        return new_state

    @staticmethod
    def end_day_time(path):
        curr_time = 360
        for i in range(len(path) - 1):
            curr_time += path[i].point.dist_to(path[i + 1].point)
            curr_time = max(curr_time, path[i + 1].point.start)
            if not path[i + 1].point.in_time(curr_time):
                return -1

        return curr_time

    def add_order(self):
        courier = self.couriers[randint(0, len(self.couriers) - 1)]
        if len(self.free_orders) == 0:
            return False

        delete_index = randint(0, len(self.free_orders) - 1)
        new_order = self.free_orders[delete_index]
        pick_event = Event(courier, 'pickup', new_order, new_order.pickup_point)
        drop_event = Event(courier, 'dropoff', new_order, new_order.dropoff_point)
        path = self.paths[courier.id]
        path_len = len(path)

        for i in range(1, path_len + 1):
            for j in range(i + 1, path_len + 2):
                new_path = copy(path)

                new_path.insert(i, pick_event)
                new_path.insert(j, drop_event)
                if self.end_day_time(new_path) != -1:
                    self.paths[courier.id] = new_path
                    del self.free_orders[delete_index]
                    return True
        return False

    def delete_order(self):
        courier = self.couriers[randint(0, len(self.couriers) - 1)]
        path = self.paths[courier.id]
        if len(path) <= 1:
            return False

        delete_pos = randint(1, len(path) - 1)
        order2delete = path[delete_pos].order

        path = [event for event in path if event.action == 'start' or event.order.id != order2delete.id]
        self.paths[courier.id] = path

        self.free_orders.append(order2delete)
        return True

    def convert_to_json(self, fd):
        res = []
        for path in self.paths:
            res += [event.get_dict() for event in path[1:]]

        json.dump(res, fd)
