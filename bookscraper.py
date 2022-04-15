#Author: Truman Daniels
#First version: 4/14/2022

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sqlite3
import re

def monetary(input_str):
    """
    Description:    
        Converts a monetary string, into a float

    Format:
        monetary(str) --> float

    Inputs:
        input_str - an input string

    Output:
        a float

    Example Usage:
        >>> monetary("£53.22")
        53.22        
    """
    amount = re.sub('[^0-9.]', '', input_str)
    return float(amount)

def scrape_single_book_page(url):
    """
    Description:
        A function that scrapes a single product page for a book and returns a dictionary
        with scraped information 

    Format:
        scrape_single_book_page(str) -> dict

    Inputs:
        url - a string that contains product page information i.e. somewhere on books.toscrape.com/catalogue   

    Output:
        a python dictionary containing the keys 'url', 'title', 'price', 'stock_status', and 'date_scraped'
    
    Example Usage:
        >>> scrape_single_book_page(url="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
        {'url': 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', 
         'title': 'A Light in the Attic', 
         'price': 51.77, 
         'stock_status': 'In stock (22 available)',
         'date_scraped': '04/14/22'}
    """
    page = requests.get(url)
    if page.status_code == 200: #200 means everything went okay!
        pass
    else:
        raise RuntimeError("Invalid Status Response Code (This probably means the website doesn't want you to scrape it!)") from error
    soup = BeautifulSoup(page.text, 'html.parser')
    for book_tree in soup.find_all(class_='col-sm-6 product_main'):
        title = book_tree.find("h1").contents[0]
        price = book_tree.find(class_="price_color").contents[0].replace("Â", "")
        stock_status = book_tree.find(class_="instock availability").contents[2].replace("\n", "").lstrip().rstrip()
    for tag in soup.find_all("meta"):
        if tag.get("name") == "description":
            description = tag.get("content")
    
    return {"url": url,
            "title": title,
            "price": monetary(price),
            "stock_status": stock_status,
            "date_scraped": datetime.now().strftime("%m/%d/%y")
           }

def get_book_urls_from_page(page=1):
    """
    Description:
        a function that gets all the url links on the browisng page

    Format:
        get_book_urls_from_page(int or str) --> list

    Inputs:
        page - a string that contains a main product page i.e. http://books.toscrape.com/catalogue/page-1.html 
        is the first page, which links to ~20 books  

    Output:
        a python list containing urls to each book listed on a given page 
        this is usually ~20
    
    Example Usage:
        >>> get_book_urls_from_page(page=1)
            ['http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
             'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html', 
                ...
             'http://books.toscrape.com/catalogue/mesaerion-the-best-science-fiction-stories-1800-1849_983/index.html', 
             'http://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html', 
             'http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html']
    """

    base_page_url= "http://books.toscrape.com/catalogue/page-"+str(page)+".html"
    url_list = []
    page = requests.get(base_page_url)
    if page.status_code == 200: #200 means everything went okay!
        pass
    else:
        raise Exception("Invalid Status Response Code")
    soup = BeautifulSoup(page.text, 'html.parser')
    for book_tree in soup.find_all(class_='image_container'):
        for link in book_tree.find_all('a'):
            url = "http://books.toscrape.com/catalogue/" + str(link.get('href'))
            url_list.append(url)
    return url_list


def if_no_table_create_one(db_path, verbose=True):
    """
    Description:
        creates a table named "Books" in the database at the location
        of db_path if none already exists. Does not overwrite previous table

    Format:
        if_no_table_create_one(str, bool) --> None
    
    Inputs:
        db_path - a string of the path to the database
        verbose - a bool (default=True) describing if the function should print info
    
    Output:
        None
    """

    # Connecting to sqlite
    # connection object
    conn = sqlite3.connect(db_path)

    # cursor object
    cur = conn.cursor()

    # Creating table
    table = """
            CREATE TABLE Books (
            URL TEXT NOT NULL,
            Title TEXT NOT NULL,
            Price£ FLOAT NOT NULL,
            Stock_Status TEXT NOT NULL,
            Date_Scraped TEXT NOT NULL
            );
            """

    try:
        # if the table does not exist yet, below line with throw error
        cur.execute(table)
        if verbose==True: 
            print("Table created.")
    except sqlite3.OperationalError as e:
        #if the table already exists
        if verbose==True:
            print(e)

    # Close the database connection
    conn.close()
    return None

def add_book_to_database(db_path, input_dict, verbose=True):
    """
    Description:
        Connects to database and inserts a new row based on an input_dictionary
        if verbose=True, as a side effect prints "Row appended: <last row in database>"
        Note: there is no duplicate entry check, so you may scrape the same data multiple times

    Format:
        if_no_table_create_one(str, dict, bool) --> None

    Inputs:
        db_path - a string of the path to the database
        input_dict - a python dictionary containing the keys 'url', 'title', 'price', 'stock_status', and 'date_scraped'
        verbose - a bool (default=True) describing if the function should print info
    
    Output:
        None

    Example Usage:
        >>> add_book_to_database(db_path=r"/home/truman/Documents/BookScraper/books.db", input_dict=, verbose=True)
        Row appended: 99

    """

    if_no_table_create_one(db_path, verbose=False)
    conn = sqlite3.connect(db_path)
    sql = ''' INSERT INTO Books(URL,Title,Price£,Stock_Status, Date_Scraped)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    data_tuple = (input_dict["url"], input_dict["title"], input_dict["price"], input_dict["stock_status"], input_dict["date_scraped"])
    cur.execute(sql, data_tuple)
    conn.commit()
    if verbose==True:
        print("Row appended: " + str(cur.lastrowid))
    
    # Close the database connection
    conn.close()
    return None

def main(db_path, seconds_to_wait_between_scrapes=5, page_start=1, page_end=50, verbose=True):
    """
    Description:
        The main function that orchestrates everything:
        Basically, it gets the url for every book product page
        and scrapes them at a given interval (default every 5 seconds)

        Note: there is no duplicate entry check, so you may scrape the same data multiple times

    Format:
        main(str, int or float, bool) --> None
    
    Inputs:
        db_path - a string of the path to the databaseath
        seconds_to_wait_between_scrapes - (default 5) a int or float which 
        page_start - a int (default=1) which describes which page to start from i.e. http://books.toscrape.com/catalogue/page-1.html  
        page_end - a int (default=50) which describes which page to end at i.e. http://books.toscrape.com/catalogue/page-50.html
        verbose - a bool(default=True) describing if the function should print info

    Example Usage:
        >>> main(r"/home/truman/Documents/BookScraper/books.db")
        Done scraping

    """

    for pg in range(page_start, page_end): #go through each browsing page
        url_list = get_book_urls_from_page(page=pg) #create a list of book URLs on that page
        for url in url_list:
            add_book_to_database(db_path=db_path, input_dict=scrape_single_book_page(url), verbose=verbose) #scrape each url
            time.sleep(seconds_to_wait_between_scrapes) #wait a little

    print("Done scraping")
    return None

    
if __name__ == '__main__':
    DATABASE = r"/home/truman/Documents/BookScraper/books.db"
    main(db_path=DATABASE) 
