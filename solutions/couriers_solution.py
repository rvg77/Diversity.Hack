# -*- coding: utf-8 -*-

import sys
from lib.entities import *
sys.path.append("..")

import lib.entities

def nearest(courier, orders, avalibales) :
    many = -1
    id = -1
    size = len(orders)

    for i in range(size) :
        order = orders[i]
        
        if avalibales[i] == False:
            continue
        if courier.can_deliver(order) == -1:
            continue
        if courier.profit(order) <= 0 :
            continue

        new_many = courier.profit(order)
        
        if many < new_many :
            many = new_many
            id = i

    return id

# итоговый профит - 263240
def couriers_solution(dataset) :
    orders = list(dataset.orders)
    depots = list(dataset.depots)
    couriers = list(dataset.couriers)
    events = []
    
    # Сортирую по разному значению, такой профит:
    #
    # pickup_point.end          -> 262627
    # pickup_point.start        -> 263234
    # dropoff_point.end         -> 263122
    # dropoff_point.start       -> 263240
    # ---                       -> 263427 -- WIN !!!
    #
 
    #orders = sorted(orders, key=lambda order: order.dropoff_point.start)

    size_couriers = len(couriers)
    size_orders   = len(orders)

    avalibales = [True] * size_orders
    
    for i in range(size_couriers) :
        print(i)
        while (True) :
            courier = couriers[i]
            id_order = nearest(courier, orders, avalibales)
            order = orders[id_order]

            if id_order == -1:
                break

            avalibales[id_order] = False
            finish_time = courier.can_deliver(order)
            events.append(Event(courier, "pickup", order, order.pickup_point))
            events.append(Event(courier, "dropoff", order, order.dropoff_point))

            couriers[i].set_point(order.dropoff_point, finish_time)

    return events