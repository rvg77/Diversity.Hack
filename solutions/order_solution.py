# -*- coding: utf-8 -*-

import sys
from lib.entities import *
sys.path.append("..")

import lib.entities

def nearest(order, couriers) :
    many = -1
    id = -1
    size = len(couriers)

    for i in range(size) :
        courier = couriers[i]
        
        if courier.can_deliver(order) == -1:
            continue
        if courier.profit(order) <= 0 :
            continue

        new_many = courier.profit(order)
        
        if many < new_many :
            many = new_many
            id = i

    # Раскоментить, что бы получить 14.285714285714286% затрат на челиков
    #if (couriers[id].Cost(order) * 5 > couriers[id].Profit(order)) :
    #    return -1
    return id

# итоговый профит - 258676
def order_solution(dataset) :
    orders = list(dataset.orders)
    depots = list(dataset.depots)
    couriers = list(dataset.couriers)
    events = []
    
    # Сортирую по разному значению, такой профит:
    #
    # pickup_point.end          -> 238125 237311
    # pickup_point.start        -> 152474 152710
    # dropoff_point.end         -> 256880 258676 !!! win
    # dropoff_point.start       -> 217584 215999
    # ---                       -> 207018 206373
    #
 
    orders = sorted(orders, key = lambda order: order.dropoff_point.end)

    size_order = len(orders)

#    profit = 0

    for i in range(size_order) :
        order = orders[i]
        id_courier = nearest(order, couriers)
        courier = couriers[id_courier]

        if id_courier == -1:
            continue

#        profit += courier.Profit(order)
        finish_time = courier.can_deliver(order)
        events.append(Event(courier, "pickup", order, order.pickup_point))
        events.append(Event(courier, "dropoff", order, order.dropoff_point))

        couriers[id_courier].set_point(order.dropoff_point, finish_time)

#    print(profit)
    return events