# Your name: Noah Gustafson 
# Your student id: 43869005
# Your email: negustaf@umich.edu
# List who you worked with on this homework: Maxton Fil

# commit 6

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse through the object and return a list of book titles (as printed on the Goodreads website) in the format given below. Make sure to strip() any newlines from the book titles.

    ['Book title 1', 'Book title 2'...]
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), 'r') as f:
        file = f.read()
    soup = BeautifulSoup(file, 'html.parser')
    aTags = soup.find_all('a', class_ = 'bookTitle')
    lst = []
    for aTag in aTags:
        spanTags = aTag.find_all('span')
        for spanTag in spanTags:
            lst.append(spanTag.text)
    return lst

def get_new_releases():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from "https://www.goodreads.com/genres/fantasy". Parse through the object and return a list of URLs for each of the books in the "NEW RELEASES TAGGED 'FANTASY'" section using the following format:

    ['https://www.goodreads.com/book/show/23106013-battle-ground', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to your list, and discard the rest.
    """
    soup = BeautifulSoup(requests.get('https://www.goodreads.com/genres/fantasy').text, 'html.parser')
    aTags = soup.find_all('a')
    hrefLst = []
    for aTag in aTags:
        tagsStrings = aTag.get('href')
        if tagsStrings is not None:
            hrefLst.append(tagsStrings)
    r = re.compile('\/book\/show\/\S*')
    newLst = list(filter(r.match, hrefLst))
    lst = []
    count = 0
    for item in newLst:
        if count != 15:
            newItem = 'https://www.goodreads.com' + item
            count += 1
            lst.append(newItem)
    return lst

def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book information from a book's webpage, given the URL of the book. Parse through the BeautifulSoup object, and capture the book title, book author, and star-rating. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', 'its star rating')

    HINT: Using BeautifulSoup's find() method may help you here. You can easily capture CSS selectors with your browser's inspector window. Make sure to strip() any newlines from the book title and star rating.
    """
    soup = BeautifulSoup(requests.get(book_url).text, 'html.parser')
    bookTitle = soup.find(id = 'bookTitle').get_text(strip=True)
    bookAuthor = soup.find(class_ = 'authorName').find('span').get_text(strip=True)
    starRating = soup.find(itemprop = 'ratingValue').get_text(strip=True)
    tup = (bookTitle, bookAuthor, float(starRating))
    return tup

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2019" page in "best_books.htm". This function should create a BeautifulSoup object from a filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL https://www.goodreads.com/choiceawards/best-fiction-books-2019, then you should append ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2019") to your list of tuples.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as f:
        file = f.read()
    soup = BeautifulSoup(file, 'html.parser')
    catlst = []
    categories = soup.find_all("h4", class_="category__copy")
    for category in categories:
        catlst.append(category.text.strip())
    titlelst = []
    bookTitle = soup.find_all('img', class_ = 'category__winnerImage')
    for book in bookTitle:
        titlelst.append(book.get('alt'))
    urllst = []
    urls = soup.find_all(class_ = 'category clearFix')
    for url in urls:
        urllst.append(url.find('a')['href'])
    tuplst = list(zip(catlst, titlelst, urllst))
    return tuplst

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the one that is returned by summarize_best_books()), writes the data to a csv file, and saves it to the passed filename.

    The first row of the csv should contain "Category", "Book title", and "URL", respectively as column headers. For each tuple in data, write a new row to the csv, placing each element of the tuple in the correct column.
    This function should not return anything.
    When you are done your CSV file should look like this:
    
    Category,Book title,URL
    Some category,Book1,url1
    Another category,Book2,url2
    Yet another category,Book3,url3
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows([('Category', 'Book Title', 'URL')])
        writer.writerows(data)
    f.close()

def extra_credit(filepath):
    """
    EXTRA CREDIT (15 Points)
    
    Sometimes when processing text data, it is useful to extract a list of people, places, and things that a document is about. This allows us to quickly tag documents by their content and can allow for faster search and retrieval, as well as providing a brief summary of the document's contents. In the field of Natural Language Processing, this task is called Named Entity Recognition (NER).
    
    These days, most NER is done using Artificial Intelligence. But, we can create a simple entity recognizer using Regex! Since English conveniently capitalizes proper nouns, we can use this to construct a regex pattern to easily grab many named entities from text.
    
    For the purposes of this assignment, we will define a named entity as follows:
    - Named entities contain 2 or more capitalized words, with no lowercase words in-between them
    - The words must be separated by spaces
    - The first word must contain at least 3 letters
    
    Write a new function ​extra_credit()​ that takes a single ​filepath​ parameter. It should create a BeautifulSoup object from the filepath, given that ​filepath​ corresponds to the webpage for a book on Goodreads.com. Extract the description** of the book from the BeautifulSoup object and find all the named entities (using the criteria given above) within the book description. This function should return a list of all named entities present in the book description for the given ​filepath​. 
    
    Your list should be in the following format:

    [‘Named Entity_1’, ‘Named Entity_2, .....]

    You do not need to write any test cases for this function.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as f:
        file = f.read()
    soup = BeautifulSoup(file, 'html.parser')
    description = soup.find(id = 'freeText4791443123668479528').get_text(strip=True)
    lst = []
    NERs = re.findall(r'\b([A-Z][a-z]{2,}(?:\s+[A-Z](?:\w)*(?:\.[0-9])?){1,})\b', description)
    for NER in NERs:
        if 'For' not in NER:
            lst.append(NER)
    return lst

def main():
    '''
    get_titles_from_search_results('search_results.htm')
    get_new_releases()
    get_book_summary('https://www.goodreads.com/book/show/49247242-ring-shout')
    summarize_best_books('best_books.htm')
    write_csv(summarize_best_books('best_books.htm'), 'mynewcsv.csv')
    #extra_credit(filepath)
    '''

class TestCases(unittest.TestCase):
    # call get_new_releases() and save it to a static variable: new_release_urls
    new_release_urls = get_new_releases() # must be called with TestCases.new_release_urls in test cases below

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)

        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(titles, list)

        # check that each title in the list is a string
        for item in titles:
            self.assertIsInstance(item, str)

        # check that the first title is correct (open search_results.htm and find it)
        self.assertEqual(titles[0], 'Harry Potter and the Deathly Hallows (Harry Potter, #7)')

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1], 'Harry Potter: The Prequel (Harry Potter, #0.5)')

    def test_get_new_releases(self):
        # check that TestCases.new_release_urls is a list
        self.assertIsInstance(TestCases.new_release_urls, list)

        # check that the length of TestCases.new_release_urls is correct (15 URLs)
        self.assertEqual(len(TestCases.new_release_urls), 15)

        # check that each URL in the TestCases.new_release_urls is a string
        for item in TestCases.new_release_urls:
            self.assertIsInstance(item, str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        self.assertEqual(TestCases.new_release_urls[0], 'https://www.goodreads.com/book/show/50623864-the-invisible-life-of-addie-larue')
        self.assertEqual(TestCases.new_release_urls[1], 'https://www.goodreads.com/book/show/49504061-the-once-and-future-witches')
        self.assertEqual(TestCases.new_release_urls[2], 'https://www.goodreads.com/book/show/50892349-magic-lessons')
        self.assertEqual(TestCases.new_release_urls[3], 'https://www.goodreads.com/book/show/48717744-the-tower-of-nero')
        self.assertEqual(TestCases.new_release_urls[4], 'https://www.goodreads.com/book/show/52735921-kingdom-of-the-wicked')
        self.assertEqual(TestCases.new_release_urls[5], 'https://www.goodreads.com/book/show/50892360-black-sun')
        self.assertEqual(TestCases.new_release_urls[6], 'https://www.goodreads.com/book/show/50622362-among-the-beasts-briars')
        self.assertEqual(TestCases.new_release_urls[7], 'https://www.goodreads.com/book/show/11503920-return-of-the-thief')
        self.assertEqual(TestCases.new_release_urls[8], 'https://www.goodreads.com/book/show/50892288-the-hollow-places')
        self.assertEqual(TestCases.new_release_urls[9], 'https://www.goodreads.com/book/show/49247242-ring-shout')
        self.assertEqual(TestCases.new_release_urls[10], 'https://www.goodreads.com/book/show/50358085-the-neil-gaiman-reader')
        self.assertEqual(TestCases.new_release_urls[11], 'https://www.goodreads.com/book/show/36253143-lightbringer')
        self.assertEqual(TestCases.new_release_urls[12], 'https://www.goodreads.com/book/show/41187447-a-golden-fury')
        self.assertEqual(TestCases.new_release_urls[13], 'https://www.goodreads.com/book/show/49151031-the-midnight-bargain')
        self.assertEqual(TestCases.new_release_urls[14], 'https://www.goodreads.com/book/show/54205369-the-lives-of-saints')

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary() for each URL in TestCases.new_release_urls
        summaries = []
        for url in TestCases.new_release_urls:
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (15)
        self.assertEqual(len(summaries), 15)

        # check that each item in the list is a tuple
        for item in summaries:
            self.assertIsInstance(item, tuple)

            # check that each tuple has 3 elements
            self.assertTrue(len(item), 3)

            # check that the first two elements in the tuple are string and the third element in the tuple, i.e. star-rating is a float
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], str)
            self.assertIsInstance(item[2], float)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        callBooks = summarize_best_books('best_books.htm')

        # check that we have the right number of best books (20)
        self.assertEqual(len(callBooks), 20)

        # assert each item in the list of best books is a tuple
        for item in callBooks:
            self.assertIsInstance(item, tuple)

            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Testaments (The Handmaid's Tale, #2)", 'https://www.goodreads.com/choiceawards/best-fiction-books-2019'
        self.assertEqual(callBooks[0], ('Fiction', "The Testaments (The Handmaid's Tale, #2)", 'https://www.goodreads.com/choiceawards/best-fiction-books-2019'))
       
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2019'
        self.assertEqual(callBooks[-1], ('Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2019'))

    def test_write_csv(self):
        # call summarize_best_books on best_books.htm and save the result to a variable
        callBooks = summarize_best_books('best_books.htm')

        # call write csv on the variable you saved
        write_csv(callBooks, 'mynewcsv.csv')

        # read in the csv that you wrote
        f = open('mynewcsv.csv', 'r')

        # check that there are 21 lines in the csv
        self.assertEqual(len(f.readlines()), 21)

        # check that the header row is correct
        for line in f.readlines():
            self.assertEqual(line[0], [('Category', 'Book Title', 'URL')])

            # check that the next row is 'Fiction', "The Testaments (The Handmaid's Tale, #2)", 'https://www.goodreads.com/choiceawards/best-fiction-books-2019'
            self.assertEqual(line[1], ['Fiction', "The Testaments (The Handmaid's Tale, #2)", 'https://www.goodreads.com/choiceawards/best-fiction-books-2019'])
        
            # check that the last row is 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2019'
            self.assertEqual(line[-1], ['Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2019'])
        f.close()

if __name__ == '__main__':
    main()
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)
