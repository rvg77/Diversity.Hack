# -*- coding: utf-8 -*-
from lib.entities import *
from solutions import order_solution
from solutions import simple_solution
from solutions import couriers_solution
from solutions import hard_couriers_solution
from solutions import hard_hard_couriers_solution
from lib.operations import Dataset

import argparse
import json

def make_result(func, data, output) :
    res = func(data)
    with open("{}/{}_output.json".format(output, func.__name__), 'w') as f:
        json.dump([e.get_dict() for e in res], f)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="path to file to test")
    parser.add_argument("--output", help="output with result")
    args = parser.parse_args()

    d = Dataset()
    with open(args.data, 'r') as f:
        d.read_json(f)
    
    # Раскоментить нужное решение, 
    
    #make_result(simple_solution.simple_solution, d, args.output)                          #-> none
    #make_result(order_solution.order_solution, d, args.output)                            #-> 258676
    make_result(couriers_solution.couriers_solution, d, args.output)                      #-> 263240
    #make_result(hard_couriers_solution.hard_couriers_solution, d, args.output)            #-> 266572
    #make_result(hard_hard_couriers_solution.hard_hard_couriers_solution, d, args.output)   #-> 270566 --- WIN


def state_test():
    d = Dataset()
    with open('data/input/simple_input.json', 'r') as f:
        d.read_json(f)
    print('a')
    s = State(d)
    print(len(s.paths[3]))


if __name__ == "__main__":
    main()
