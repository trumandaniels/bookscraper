import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sqlite3


def scrape_single_book_page(url):
    """
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
         'price': '£51.77', 
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
            "price": price,
            "stock_status": stock_status,
            "date_scraped": datetime.now().strftime("%m/%d/%y")
           }

def get_book_urls_from_page(page=1):
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
    # Connecting to sqlite
    # connection object
    conn = sqlite3.connect(db_path)

    # cursor object
    cur = conn.cursor()

    # Drop the GEEK table if already exists.
    # cursor_obj.execute("DROP TABLE IF EXISTS GEEK")

    # Creating table
    table = """
            CREATE TABLE Books (
            URL TEXT NOT NULL,
            Title TEXT NOT NULL,
            Price TEXT NOT NULL,
            Stock_Status TEXT NOT NULL,
            Date_Scraped TEXT NOT NULL
            );
            """

    try:
        cur.execute(table)
        if verbose==True:
            print("Table created.")
    except sqlite3.OperationalError as e:
        if verbose==True:
            print(e)

    # Close the connection
    conn.close()

def add_book_to_database(db_path, input_dict, verbose=True):
    if_no_table_create_one(db_path, verbose=False)
    conn = sqlite3.connect(db_path)
    sql = ''' INSERT INTO Books(URL,Title,Price,Stock_Status, Date_Scraped)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    data_tuple = (input_dict["url"], input_dict["title"], input_dict["price"], input_dict["stock_status"], input_dict["date_scraped"])
    cur.execute(sql, data_tuple)
    conn.commit()
    if verbose==True:
        print("Row appended: " + str(cur.lastrowid))
    
    # Close the connection
    conn.close()
    return None

def main(db_path, seconds_to_wait_between_scrapes=5, verbose=True):
    for pg in range(1, 50):
        url_list = get_book_urls_from_page(page=pg)
        for url in url_list:
            add_book_to_database(db_path=db_path, input_dict=scrape_single_book_page(url), verbose=verbose)
            time.sleep(seconds_to_wait_between_scrapes)
    print("Done scraping")

    
if __name__ == '__main__':
    database = r"/home/truman/Documents/BookScraper/books.db"
    main(db_path=database) 
