# bookscraper
Web Scraper / Web Crawler for books.toscrape.com

This program takes online book data on books.toscrape.com and stores it in a local SQLite database. 

Quick file rundown:
- bookscraper.py ~ where all the magic happens: this file contains all the scraping logic and function documentation 
- test.py ~ a small unit test suite
- books.db ~ the SQLite database where everything is stored

Example use:


Sources:
- https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3
- https://www.programiz.com/python-programming/datetime/current-time
- https://stackoverflow.com/questions/36768068/get-meta-tag-content-property-with-beautifulsoup-and-python
- https://www.sqlitetutorial.net/sqlite-python/insert/
- https://stackoverflow.com/questions/4098008/create-table-in-sqlite-only-if-it-doesnt-exist-already
- https://dev.to/albertulysses/unit-testing-your-web-scraper-1aha
