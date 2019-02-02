import bs4
import urllib.request
from bs4 import BeautifulSoup as soup
import os

my_url = 'https://scryfall.com/sets'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def new_page (url):
    # set a request to the url
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read() # The data u need
    response.close()

    # and parses the HTML code
    page_soup = soup(data, "html.parser")
    return page_soup

def set_main_folder():
    if not os.path.exists("Magic_Images"):
        os.mkdir("Magic_Images")
    os.chdir("Magic_Images")

def set_collection_folder(set):
    path_name = os.path.dirname (os.path.realpath(__file__)).split("/")[-1]
    print (path_name)
    if not (path_name == "Magic_Images"): # already on a previous set
        os.chdir("..")
    if not os.path.exists(set):
        os.mkdir(set)
    os.chdir(set)

def download_card(id, image):
    if not os.path.exists(id + ".jpg"):
        urllib.request.urlretrieve(image, id)
        os.rename(id, id + ".jpg")

def download_all_cards_in_set(set):
    # set new webpage
    name_full_set = set.text.replace("\n", "").split(" ")
    name_full_set = ("_").join(list(filter(None, name_full_set)))

    name_set = set.find('small').text
    new_page_html = new_page (my_url + "/" + name_set.lower())

    set_collection_folder(name_full_set)

    # create a list of cards
    list_of_cards_in_set = new_page_html.findAll('img')

    del list_of_cards_in_set[-1] #last one is not in the list

    print ("Donwloading the whole set: " + full_list[pos].find('small').text)
    # set attributes for our cards
    for y in list_of_cards_in_set:
        #print (y)

        name_card = y["title"].replace(" ", "_")
        image_card = y["src"];
        if (image_card == ""): # Error happened for some cards
            image_card = y["data-src"]

        print ("Donwloading: " + name_card)
        download_card(name_card, image_card)


def find_sets(html):
    list_of_sets =  page_soup.findAll( 'td',attrs={'class':'flexbox'})
    return list_of_sets

def find_single_set(l, filter_name):
    for it, x in enumerate(l):
        if (x.find('small').text == filter_name):
            return it
    return -1

#### MAIN CODE ####


page_soup = new_page (my_url)
full_list = find_sets(page_soup)

pos = find_single_set(full_list, "10E") # find position of Magic 2012 Set in list
#print (pos)

set_main_folder()

download_all_cards_in_set(full_list[pos])





#set_main_folder()
#download_all_cards_in_set()




#card = list_of_cards_in_set[0]
#print (card)
