# Bookscraper
## a web scraper / web crawler for books.toscrape.com

This program takes online book data on books.toscrape.com and stores it in a local SQLite database. Developed with Linux Mint and Python 3.8.

## Quick file rundown:
- bookscraper.py ~ where all the magic happens: this file contains all the scraping logic and function documentation 
- test.py ~ a small unit test suite
- books.db ~ the SQLite database where everything is stored

## Set Up
First (Optional) Step: create and activate python virtual environemnt or anaconda environment first (skipping this step could cause package dependency/compatibility issues if your machine is used for many projects)

Changing the working directory to wherever you extract the downloaded folder to
```
truman@laptop ~ $ cd /path/to/extracted/bookscraper-main
```

#### Creating python virtual environment:
either (after installing virtualenv) choosing a specific python version
```
truman@laptop ~/bookscraper-main ~ $  virtualenv --python=/usr/bin/python3.9 /path/to/new/environment/VIRTUALENVNAME 
```
or using whatever your PATH is set to (probably fine)
```
truman@laptop ~/bookscraper-main ~ $ python3 -m venv /path/to/new/environment/VIRTUALENVNAME 
```
#### You can then activate the environment using:
```
truman@laptop ~/bookscraper-main ~ $ source /path/to/new/environment/VIRTUALENVNAME/bin/activate
```

Then install neccesary packages to run the scripts
```
(VIRTUALENVNAME) truman@laptop ~/bookscraper-main ~ $ pip install -r requirements.txt 
```

## Run Tests:
(VIRTUALENVNAME) truman@laptop ~/bookscraper-main ~ $ pytests tests.py 
collected 2 items                                                              

tests.py ..                                                              [100%]
============================== 2 passed in 0.19s ===============================

## Example use:
(VIRTUALENVNAME) truman@laptop ~/bookscraper-main ~ $ python bookscraper.py
Row appended: 1
Row appended: 2
Row appended: 3
...
Row appended: 1000
Done scraping

Sources:
- https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3
- https://www.programiz.com/python-programming/datetime/current-time
- https://stackoverflow.com/questions/36768068/get-meta-tag-content-property-with-beautifulsoup-and-python
- https://www.sqlitetutorial.net/sqlite-python/insert/
- https://stackoverflow.com/questions/4098008/create-table-in-sqlite-only-if-it-doesnt-exist-already
- https://dev.to/albertulysses/unit-testing-your-web-scraper-1aha
