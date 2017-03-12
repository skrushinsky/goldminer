# GoldMiner

Добывает данные о ценах на золото и серебро, а также курсы валют.

## Обзор
	
Рабочей программой является **скрапер**, который периодически заходит на [http://www.forexpf.ru/](http://www.forexpf.ru/) и собирает:

* **xau**, цена золота, USD
* **xag**, цена серебра, USD
* **usd**, курс доллара по отношению к рублю
* **eur**, курс евро по отношению к рублю

Результат может возвращаться либо как текст либо как JSON, формат задается аргументом комендной строки.

Очередная порция данных приходит в течение интервала от 2 до 5 минут, если в конфигурации не задано иное. Скрапер специально выдерживает случайные интервалы между запросами, чтобы иммитировать поведение человека и тем самым снизить риск обнаружения. Если нужно, чтобы запросы к сайту были анонимны, удобно [использовать сеть Tor](http://github.com/skrushinsky/goldminer/wiki/GoldMinerAnonymity).


### Платформа:

  * [Python 2.7](http://python.org)
  * [Requests](http://docs.python-requests.org/en/master/)

Более подробная документация располагается на [wiki](http://github.com/skrushinsky/goldminer/wiki).


## Как пользоваться

### Установка


```
python setup.py install develop
```

Скрипт setup.py установит при необходимости следующие основный зависимости:

* [Requests](http://docs.python-requests.org/en/master/)
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [lxml](http://lxml.de)

Скопируйте файл `conf/default.conf` в `conf/local.conf`. Если нужно: внесите в local.conf изменения.


### Конфигурация

По умолчанию используется файл `conf/local.conf`. Он является модифицированной версией
`conf/default.conf`. Путь к альтернативной конфигурации можно задать опцией командной строки `-c` (`--conf`). 

Конфигурация представляет собой простой INI-файл. См. [подробное описание](http://github.com/skrushinsky/goldminer/wiki/GoldMinerConfiguration)


### Тестирование


Из верхнего каталога приложения:
```
$ python tests/scrapper_test.py
```

#### Примеры запуска

```
$ python scripts/main.py 
```

Для справки:

```
$ python scripts/main.py --help
```

Записывать котировки в текстовый файл так, чтобы каждая серия данных представляла собой строку

```
$ python scripts/main.py >> ./quotes.txt
```
