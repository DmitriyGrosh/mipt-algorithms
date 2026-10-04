# mipt-algorithms

ДЗ3: граф import-зависимостей по .py файлам (тестировал на scrapy, коммит ebfb049).

Требования: Python 3. graph_analyzer.py без внешних пакетов. verify.py нужен networkx (requirements.txt).

Запуск (из папки с graph_analyzer.py):

```
python3 graph_analyzer.py <stats|impact|cycles|order> <путь_к_репозиторию> [файл]
```

Примеры:

```
python3 graph_analyzer.py stats /path/to/scrapy
python3 graph_analyzer.py impact /path/to/scrapy scrapy/spidermiddlewares/base.py
python3 graph_analyzer.py cycles /path/to/scrapy
python3 graph_analyzer.py order /path/to/scrapy
```

Путь: корень репозитория. Каталоги test, tests, __tests__, .git, venv и т.п. при обходе пропускаются.

cycles: код выхода 1 если есть циклы, 0 если нет.

Проверка через networkx:

```
pip install -r requirements.txt
python3 verify.py /path/to/scrapy
```
