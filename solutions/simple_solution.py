import sys
from lib.entities import *
sys.path.append("..")


def nearest(courier, orders, avalibales) :
    lenght_ = -1
    id = -1
    size = len(orders)

    for i in range(size) :
        order = orders[i]
        new_lenght = courier.point.dist_to(order.pickup_point)
        
        if ((new_lenght < lenght_ or id == -1) and avalibales[i]) :
            lenght_ = new_lenght
            id = i
        
    return id


# courters  - list courter
# orders    - list ovder
# depots    - list depot
def simple_solution(dataset):
    orders = list(dataset.orders)
    depots = list(dataset.depots)
    couriers = list(dataset.couriers)
    
    events = []

    orders_size = len(orders)
    avalibales = [True] * orders_size
    
    for courier in couriers :
        id_order = nearest(courier, orders, avalibales)
        
        if id_order == -1:
            break

        avalibales[id_order] = False
    
        events.append(Event(courier, "pickup", orders[id_order], orders[id_order].pickup_point))
        events.append(Event(courier, "dropoff", orders[id_order], orders[id_order].dropoff_point))
    
    return events

if __name__ == "__main__":
    pass
