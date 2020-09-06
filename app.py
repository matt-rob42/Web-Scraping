#from lxml import etree # had to edit out - contradiction in HTML methods

from lxml import html


#tree = etree.parse("fundamentals\src\src\web_page.html")
## this parses out the elements of the tree - does it
## maintain the hirarchical structure??

# print(tree)
# ## we can also reveal the raw data of the tree:

# print(etree.tostring(tree))

## Now that we have an element tree object, we can extract any element that we might want
## we use tree.find() with the parameter as the element we want

# title_element = tree.find("head/title")

# print(title_element.text) ## .text gives us a str rep

# paragraph_element = tree.find("body/p")

# print(paragraph_element.text) ## Basically need the whole path to element

## we also have a find all method - 

# list_items = tree.findall("body/ul/li")

# for item in list_items:
#     print(item.text)

## However, this doesn't give us the nested "a" tag - here's
## how to find that:

# for item in list_items:
#     a = item.find("a")
#     if a is not None:
#         print(f"{item.text} {a.text}")
#     else:
#         print(item.text)


##Now, what if we want to deal with larger pages that have many, many tags?

## we will use "xpath", which allows us to avoid using the full path to a tag

# title_element = tree.xpath("//title")[0] #note this returns a list!
## so must slice it
# print(title_element.text)

# paragraph_element = tree.xpath("//p/text()")[0]
# 
# print(paragraph_element) ## This is the way to do it by putting
## the text conversion in the initial call (line 49)

## Now for the list:

# list_items = tree.xpath("//li")

# for item in list_items:
#     text = ''.join(map(str.strip, item.xpath(".//text()"))) ##period is important to remove the whitespace!
#     print(text) ## join gets it into a nice, readable format!

#### We can also use CSS selectors to help us in scraping
#### normally these are used to "paint" HTML with a format,
#### but we can use them to acquire tags
#### pip install cssselect

# html = tree.getroot()


# title_element = html.cssselect("title")[0] 

## so must slice it
# print(title_element.text)


# list_items = tree.xpath("li")
# for item in list_items:
#     text = ''.join(map(str.strip, html.cssselect("title"))) ##period is important to remove the whitespace!
#     pass#print(text.text) ## This is a simlified version using CSS Select


####### 

################################################

###Lecture - what are xpath and css in theory?

## xpath is the xmp path language, css is cascading style sheets

### we have a rich ability to select elements by their tags 

### Examples:

## see the attached file "code.html"

## simple query - select the h1 tag, returns its contents
## BUT in a large page, likely many h1 tags, so we need a way to narrow this
## (like a WHERE clause in SQL)

## we can query by class by using the dot notation - 
## BUT since this class occurs in multiple locations,
## we return multiple values - i.e. div class AND span class
## To narrow this, we use div.intro, span.intro etc.

## we can also search by ids - use the # notation
## #location returns the values on line 11
## note that locations are unique

## now what if we had something like lines 28 and 29 - 
## where the tag has two or more classes:
## so if we write .bold, we return two classes, to specify:
## .bold.italic

## if we want to select by other things in the code, e.g.
## on line 19, the data identifier, we use:
## li[data-identifier=7]

## now what if we wanted to filter things even more?
## selecting *only* things that start with something specific:
## on line 25: a[href^=https], the ^ means an exact match at beginning
## OR on line 26, a[href$=fr] does exact match at the end!
## OR to find anywhere a[href*=google] matches anywhere

## Now, what if we wanted attributes based on position???
## e.g. in line 8 onwards, div.intro p gives us all the p tags

## if we want all the direct children of the div, use div.intro > p

## if we only want p elements immediately after the div.intro, 
## then use div.intro + p

## now say for line 18 we wanted the first li
## li:nth-child(1) this gives us the nth based on parameter
## could also do multiples with li:nth-child(1), li:nth-child(3) etc.
## could also do li:nth-child(odd) etc.


### Now xpath - probably more generally useful

## simple select  //h1

### now say we want only p's where the class attribute is set to intro:
## //div[@class='intro']/p

## now if we wanted to select multiple classes:
## //div[@class='intro' or @class='outro']

## we can get just text with: //div[@class='intro']/p/text

## now what if we wanted to select only the href with https?
## we would use //a[starts-with(@href, 'https')] first param is 
## where to look, second is what to look for
## to look at end, use: //a[ends-with(@href, 'fr')]

## finally, for the contains search: 
## //a[contains(@href, 'google')]

#### POSITIONAL SELECTION WITH XPATH:

##//ul[@id='items']/li[1]

## now, let's look at using xpath to navigate "up"
## I believe this means from sub elements to elements
## this is basically the reverse of how we were navigating before

## to do this:
## //p[@id='unique']/parent::div (note this is for a slightly different
# file that I was too lazy to download)
## instead of parent, we could use ancestor to get *all* the 
## parents!
## can also use preceding to get everything before that

##We can also get siblings (same parents)
## by using this:
## use preceding-sibling for this

### VIDEO - Going Down the Tree:

##//div[@class='intro']/child::node() # node is a general function, 
## we could of course return a specific tag

##to get everything afterwards, use following

## to get following siblings, use following-sibling

## to get decendents of a tag: 
## //div[@class='intro']/descendent::node()


### Digression on how web works:

## All web apps have a client-server architecture
## they comunicate in a request-response fashion

## GET is for requesting a resource
## POST, PUT etc.

## Real example:

import requests 

resp =requests.get(url ="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

# print(resp)
# this returns a 200 code - the response worked

# print(resp.text)
#pretty nice - this gives us the html (the CTRL U of the site)
## can also use content in place of text

### go to any website - in settings choose developer tools, press 
## ctrl r, then network - scroll to see the request and response headers

## we can get these with 

print(resp.headers)

# print(resp.request.headers) ## this returns the "user-agent"
## which can be a browser or a script 
## we don't want to leave it as a script, many pages will block that!

## so we copy the user agent that is produced when we hit the website
# with a browser
## e.g. Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36


## so use:

resp = requests.get(url ="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'})

# print(resp.request.headers) 

## Now how do we find tags on a page? When in dev mode, we can hit 
## the "arrow box" on the top left to allow us to inspect elements 
## and see where they are in the layout

## we can test our xpath expressions in chrome, just hit CTRL f in
## the dev tools to enter one

###############

## Now let's work on building a parser we'll use the html module:
from lxml.html import fromstring
new_tree = html.fromstring(html=resp.text) ## this builds the HTML tree

title = new_tree.xpath("//div[contains(@class, 'product_main')]/h1/text()")[0]
price = new_tree.xpath("//div[contains(@class, 'product_main')]/p[1]/text()")[0]
availibility = new_tree.xpath("//div[contains(@class, 'product_main')]/p[2]/text()")[1].strip() # this clears the whitespace!
description = new_tree.xpath("//div[@id='product_description']//following-sibling::p/text()")[0]

#print(title, price, availibility, description) ## this gets light in the attic title!
## Best practice is to store this as a dict - i.e. dict = {'title':title} etc.

## We can also refactor to clean this up, eliminting much of the repetition:

product_main = new_tree.xpath("//div[contains(@class, 'product_main')]")[0]

title = product_main.xpath(".//h1/text()")[0]
price = product_main.xpath(".//p[1]/text()")[0]
availability = product_main.xpath(".//p[2]/text()")[1].strip() # this clears the whitespace!
description = new_tree.xpath("//div[@id='product_description']//following-sibling::p/text()")[0]

# print(title, price, availability, description)

####### NOW for some data cleaning:

## we can use a regex - use the site regex 101 to test!

## for example, we want to select only the numbers from:  In stock (22 available)
## we use /d+ which selects only the digits

import re # this is the regex module

in_stock = re.compile(r"\d+").findall(availability)[0] #r indicates the regex

# print(in_stock)

### OR we can do it in python style - a function that takes a character, and checks if it is
## present

def get_digit(x):
    if x.isdigit():
        return x

in_stock = ''.join(list(filter(get_digit,availability)))

### Writing to JSON/CSV

## we will make a function to do this:

book_information = {'title':title, 
'price':price,
'description': description,
'in_stock': in_stock}

import json
import csv
import click



def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()


def write_to_csv(filename, data):
    headers = ['title', 'price', 'description', 'in_stock']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writerow(data)

@click.command()
@click.option('--bookurl', default="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", help = "provide a URL")
@click.option('--filename', default="output.json")
def scrape(bookurl, filename):
    resp = requests.get(url ="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'})
    product_main = new_tree.xpath("//div[contains(@class, 'product_main')]")[0]

    title = product_main.xpath(".//h1/text()")[0]
    price = product_main.xpath(".//p[1]/text()")[0]
    availability = product_main.xpath(".//p[2]/text()")[1].strip() # this clears the whitespace!
    description = new_tree.xpath("//div[@id='product_description']//following-sibling::p/text()")[0]


    
    book_information = {'title':title, 
    'price':price,
    'description': description,
    'in_stock': in_stock}
    extension = filename.split('.')[1]

    if extension == 'json':
        write_to_json(filename, book_information)
    elif extension == 'csv':
        write_to_csv(filename, book_information)
    else:
        click.echo("Extension provided is not supported") #echo is same deal as print

if __name__ == '__main__':
    scrape()      


    
# write_to_json("data.json", book_information)
# write_to_csv("data.csv", book_information)

### Now, what if we wanted to be able to launch the app using the command line?
## we will use a package called "click" - that will allow us to build quick 
## command line interfaces

