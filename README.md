# mipt-algorithms

ДЗ3: граф import-зависимостей по .py файлам (тестировал на scrapy, коммит ebfb049).

Требования: Python 3. graph_analyzer.py без внешних пакетов. verify.py нужен networkx (requirements.txt).

Запуск:

```
python3 graph_analyzer.py stats /путь/к/scrapy
python3 graph_analyzer.py impact /путь/к/scrapy scrapy/crawler.py
python3 graph_analyzer.py cycles /путь/к/scrapy
python3 graph_analyzer.py order /путь/к/scrapy
```

Путь: корень репозитория. Каталоги test, tests, __tests__, .git, venv и т.п. при обходе пропускаются.

cycles: код выхода 1 если есть циклы, 0 если нет.

Проверка через networkx:

```
pip install -r requirements.txt
python3 verify.py /path/to/scrapy
```
