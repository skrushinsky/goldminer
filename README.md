# GoldMiner

Добывает данные о ценах на золото и серебро, а также курсы валют.
	
Рабочей программой является **скрапер**, который периодически заходит на [http://www.forexpf.ru/](http://www.forexpf.ru/) и собирает цены на драгоценные металлы и курсы валют, см. [Подробное описание](https://github.com/skrushinsky/goldminer/wiki/GoldMinerResult). Результат может возвращаться либо как текст либо как JSON, что задается аргументом командной строки.

Очередная порция данных приходит в течение интервала от 2 до 5 минут, если в конфигурации не задано иное. Скрапер специально выдерживает случайные интервалы между запросами, чтобы иммитировать поведение человека и тем самым снизить риск обнаружения. Чтобы скрыть IP-адрес хоста, с которого производятся запросы, можно [настроить программу на сеть Tor](http://github.com/skrushinsky/goldminer/wiki/GoldMinerAnonymity).

Платформа:

  * [Python 2.7](http://python.org)
  * [Requests](http://docs.python-requests.org/en/master/)

Подробная документация располагается на [wiki](http://github.com/skrushinsky/goldminer/wiki).

## Как пользоваться

### Установка

```
$ python setup.py install develop
$ cp conf/default.conf conf/local.conf
```
Если нужно: внесите в `local.conf` изменения.

См. [Подробнее об установке](http://github.com/skrushinsky/goldminer/wiki/GoldMinerSetup).

### Конфигурация

Конфигурация представляет собой простой INI-файл. См. [подробное описание](http://github.com/skrushinsky/goldminer/wiki/GoldMinerConfiguration)

По умолчанию используется файл `conf/local.conf`. Он является модифицированной версией
`conf/default.conf`. Путь к альтернативной конфигурации можно задать опцией командной строки `-c`.

Обратите внимание: `local.conf` не входит в дистрибутив, его нужно создать руками как копию `default.conf` (см. выше).

### Тестирование

Для запуска Unit-тестов понадобится [фреймворк Nose](http://nose.readthedocs.io/en/latest/).

Из верхнего каталога приложения:

```
$ nosetests tests/*
```

Или:

```
$ python tests/scrapper_test.py
$ python tests/scrapper_test.py
```

### Запуск

```
$ python scripts/main.py --help
$ python scripts/main.py --once

2017-03-12T09:19:48|58.978|62.992|1204.500|17.030

$ python scripts/main.py 
2017-03-12T09:05:21|58.978|62.992|1204.500|17.030
2017-03-12T09:39:22|58.978|62.992|1204.500|17.030
...
2017-03-12T13:30:18|58.978|62.992|1204.500|17.030
```
Подробнее в разделе [Примеры запуска](http://github.com/skrushinsky/goldminer/wiki/GoldMinerUsage).

- - -
