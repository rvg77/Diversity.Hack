<p align="center">
  <img src="https://avatars.mds.yandex.net/get-ydo/472106/2a0000016717d8ae36d8ff4954faf115da30/320x320" />
</p>

# We wanted to graduate from MIPT younger (Мы хотели закончить физтех молодыми)

## Short solution descriptions:

First one — ```simple_solution()``` doesn't look on the price and consistently chooses for each courier the closest free order, calculates the company profit by sum over all couriers(order_price - courier_salary). Solution works fast.

Second one — ```courier_solution()``` works in similar way, but chooses for each courier not the closest order but the most profitable. Courier work until he can benefit the company.  Works fast, result: **263240**.

Third one — ```order_solution()``` for each order chooses the courier that can provide the company with the best profit. These profits make up the sum. By the way, the order of orders(haha) is defined like the earlier the order is available, the earlier we take this order into consideration. Works fast, result: **258676**.

For ```hard_courier_solution()``` function ```best_courier()``` was added, it builds for each courier the chain of actions for the whole day and computes the profit, chooses from them the best one and adds this chain to events list, courier and orders of this chain becomes unavailable. Works for about 40 minutes, result: **266572**.

Fifth one — ```hard_hard_curier_solution()``` chooses the best courier based not on the whole chain but only the 3 first actions of the day and adds to event only one action(of course, updates the courier position). Works for about a half of the day, result: **270566**.

## How to run solutions:


Compile with `make`

Makefile has parameters:

### Main:

`DF` - __name__ of file with data (e.g. - contest)
`OF` - __name__ of solution file (e.g. - hard_hard_curier)


### Additional
`DATA_DIRECTORY` - path to directory with data
`OUTPUT_DIRECTIORY` - path to answers directory

`DATA_PREFICS` - prefix of data file
`SOLUTION_PREFICS` - prefix of answer files
`PYTHON` - python interpreter

### Run:

By default we run hard_hard_couriers, on dataset contest. 

We can run hard_couriers on dataset simple:

`make DF=simple OF=hard_couriers`

So the output will be recalculated. To run check.py on the output:

`make check DF=simple OF=hard_couriers`
