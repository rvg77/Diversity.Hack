# Dostavisto
# Мы хотели закончить физтех молодыми

# что бы запустить генерацию решения надо вызвать

```make``` 

Код сгенерируется в файл __couriers_solution_output__



## Краткое описание подходов:

Первый вариант решения ```simple_solution()```, не смотря на стоимость заказа, выбирает последовательно для каждого курьера самый близкий (по расстоянию) заказ из еще не принятых к выполнению, считает прибыль фирмы как сумму прибыли по каждому курьеру (разность стоимости заказа и зарплаты курьера за его выполнение). Работает быстро, на выборке contest_input результат не получен.

Следующий вариант ```courier_solution()``` действует похожим образом, но теперь выбирает для каждого курьера из доступных не самый близкий заказ, а самый выгодный (по размеру прибыли, получаемой компанией от работы этого курьера). Причём каждый курьер обрабатываетс один раз - мы “не отпускаем” его до тех пор, пока есть заказ приносящий выгоду компании. Работает быстро, полученный результат 263240.

Вариант ```order_solution()``` для каждого заказа выбирает курьера, при выполнении заказа которым компания получит большую прибыль. Вся эта прибыль суммируется. При этом, порядок заказов для выбора его исполнителя определяется временем окончания времени, доступного для выгрузки(чем раньше это время заканчивается, тем раньше мы беремся за его распределение). Работает быстро, полученный результат 258676.

Для варианта ```hard_courier_solution()``` добавлена функция ```best_courier()```, которая из еще свободных курьеров выбирает самого выгодного для компании (строит для курьера цепочку действий на день и считает прибыль от его действий за весь день; выбирает среди возможных прибылей от всех курьеров наибольшую и добавляет в events всю цепочку действий для данного курьера; курьер и заказы из этой цепочки становятся недоступными). Таким образом последовательно строятся маршрутные листы для всех курьеров. Работает 40 минут, полученный результат 266572.

Вариант ```hard_hard_curier_solution()``` выбирает самого выгодного курьера не по всей цепочке действий за день, а только по первым трем, в events добавляются не все действия, а только первый из них. При этом каждый раз для курьера запоминаем его положение и время, в которое он там оказался. Работает полдня, полученный результат 270566.

## Как запустить решения:



Проект компилируется с помощью утилиты make

Makefile имеет параметры:

### Основные:

DF - __название__ файла с данными (например - contest)
OF - __название__ файла-решение (например - hard_hard_curier)


### Дополнительные
DATA_DIRECTORY - путь к дериктории с данными
OUTPUT_DIRECTIORY - путь к дериктории для вывода ответа

DATA_PREFICS - префикс к файлу с данными
SOLUTION_PREFICS - префикс к файлу с решениями

PYTHON - интерпритатор питона

### Запускаем:

По умолчанию мы запускаем решение hard_hard_couriers, на данных contest. 

Можно запустить, например, решение hard_couriers на тесте simple

Для этого надо запустить:

make DF=simple OF=hard_couriers

В таком случае выход программы пересчитается. Что бы натравить скрипт check.py на выход программы, можно запустить

make check DF=simple OF=hard_couriers
