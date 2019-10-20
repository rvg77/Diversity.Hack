# -*- coding: utf-8 -*-

import sys
from lib.entities import *
sys.path.append("..")

import lib.entities

# самое выгодное предложение для курьера
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

# самый выгодный курьер для компании
def best_courier(couriers, orders, avalibales_couriers, avalibales_orders) :
    many = 0
    id = -1
    size = len(couriers)

    disavalibal_ = []
    finish = couriers[0]

    for i in range(size) :
        if avalibales_couriers[i] == False:
            continue

        courier_point = PointTime(couriers[i].point.id, couriers[i].point.x, couriers[i].point.y)
        courier_time = couriers[i].time
        
        new_many = 0

        disavalibal = []

        iter = 0
        while (iter < 3) :
            iter += 1
            courier = couriers[i]
            order_id = nearest(courier, orders, avalibales_orders)
            order = orders[order_id]

            if order_id == -1 :
                break

            avalibales_orders[order_id] = False
            
            disavalibal.append(order_id)
            
            new_many += courier.profit(order)
            finish_time = courier.can_deliver(order)

            couriers[i].set_point(order.dropoff_point, finish_time)

        if new_many > many :
            many = new_many
            id = i
            disavalibal_ = disavalibal
            finish = couriers[i]
        
        couriers[i].point = courier_point
        couriers[i].time = courier_time

        for disav in disavalibal :
            avalibales_orders[disav] = True
        
    return id

# итоговый профит - 270566
def hard_hard_couriers_solution(dataset) :
    orders = dataset.orders
    depots = dataset.depots
    couriers = dataset.couriers
    events = []
 
    #orders = sorted(orders, key = lambda order: order.dropoff_point.start)

    size_couriers = len(couriers)
    size_orders   = len(orders)

    avalibales_couriers = [True] * size_couriers
    avalibales_orders = [True] * size_orders
    
    i = 0

    sum_many = 0

    while (True) : 
        print(i)
        best_id = best_courier(couriers, orders, avalibales_couriers, avalibales_orders)
        
        courier = couriers[best_id]
        
        if best_id == -1:
            break

        id_order = nearest(courier, orders, avalibales_orders)
        order = orders[id_order]

        avalibales_orders[id_order] = False

        finish_time = courier.can_deliver(order)
        
        many = courier.profit(order)
        sum_many += many
        print("best = ", best_id, "many = ", many, "sum_many = ", sum_many)

        events.append(Event(courier, "pickup", order, order.pickup_point))
        events.append(Event(courier, "dropoff", order, order.dropoff_point))

        couriers[best_id].set_point(order.dropoff_point, finish_time)
        
        i += 1



    return events