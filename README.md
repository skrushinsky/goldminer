# GoldMiner

Добывает с сайта [forexpf.ru](http://www.forexpf.ru/) цены драгоценных металлов и курсы валют. Результат может возвращаться либо как текст либо как JSON, что задается аргументом командной строки. См. [подробное описание результата](http://github.com/skrushinsky/goldminer/wiki/GoldMinerResult).

Очередная порция данных приходит в течение интервала от 2 до 5 минут, если в конфигурации не задано иное. Скрапер выдерживает случайные интервалы между запросами, иммитируя поведение человека. Чтобы скрыть IP-адрес хоста, с которого производятся запросы, можно [настроить программу на сеть Tor](http://github.com/skrushinsky/goldminer/wiki/GoldMinerAnonymity).

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
$ python tests/forex_test.py
```

### Запуск

```
$ python scripts/main.py --help
$ python scripts/main.py --once

2017-03-12T20:33:26+00|58.721:58.731|63.367:63.387|1204.500:1204.800|17.030:17.060|937.000:947.000|746.600:749.600

$ python scripts/main.py 
2017-03-12T20:45:22+00|58.721:58.731|62.927:62.947|1204.500:1204.800|17.030:17.060|937.000:947.000|746.600:749.600
2017-03-12T20:49:20+00|58.721:58.731|62.680:62.700|1204.500:1204.800|17.030:17.060|937.000:947.000|746.600:749.600
2017-03-12T20:49:41+00|58.721:58.731|62.680:62.700|1204.500:1204.800|17.030:17.060|937.000:947.000|746.600:749.600
2017-03-12T20:53:42+00|58.721:58.731|62.889:62.909|1204.500:1204.800|17.030:17.060|937.000:947.000|746.600:749.600

```
Подробнее в разделе [Примеры запуска](http://github.com/skrushinsky/goldminer/wiki/GoldMinerUsage).

- - -

Подробнее о программировании краулеров (ботов, скраперов, веб-роботов, парсеров) на сайте [www.crawlers.info](http://www.crawlers.info).
