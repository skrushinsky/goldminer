# GoldMiner

Добывает текущие данные о ценах на золото и серебро, а также курсы валют.

## Платформа:

  * [Python](http://python.org)
  * [Requests](http://docs.python-requests.org/en/master/)

	
Основной рабочей программой является **скрапер**, который периодически заходит на [http://www.forexpf.ru/](http://www.forexpf.ru/) и собирает информацию о ценах на золото, серебро, а также курсы евро и доллара. Данные обновляются в течение интервала от 2 до 5 минут (если в конфигурации не задано иное). Скрапер специально выдерживает случайные интервалы между запросами, чтобы снизить риск обнаружения. Запросы к сайту анонимны, через сеть Tor.

Скрапер возвращает следующие данные:


* **xau**, цена золота, USD
* **xag**, цена серебра, USD
* **usd**, курс доллара по отношению к рублю
* **eur**, курс евро по отношению к рублю
* **ts**, дата и время получения результата, в формате ISO-8601, UTC


## Как пользоваться

### Установка

```
python setup.py install develop
```

### Конфигурация

По умолчанию используется файл `conf/local.conf`. Он является модифицированной версией
`conf/default.conf`. Путь к альтернативной конфигурации можно задать опцией командной строки `-c` (`--conf`). 

Конфигурация представляет собой простой INI-файл.

### Запуск

```
$ python scripts/scrap.py
```

Для справки:

```
$ python scripts/main.py --help

usage: main.py [-h] [-c CONF] [-l LOGFILE] [-v] [-f {json,text}]

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  configuration file
  -l LOGFILE, --logfile LOGFILE
                        log file
  -v, --verbose         increase output verbosity
  -f {json,text},
  --format {json,text}  output format  

```

Записывать котировки в текстовый файл так, чтобы каждая серия данных представляла собой строку

```
$ python scripts/main.py >> ./quotes.txt
```
