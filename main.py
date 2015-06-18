#parses garage sale page, opens individual postings, looks for keywords
import urllib2
from bs4 import BeautifulSoup
import smtplib
import time
from lxml import html
import requests
import re

craigslist_region = 'pittsburgh'
url = 'http://' + craigslist_region + '.craigslist.org/search/gms'
# Need to find a way to add on pages to this link. '?s=100' for page 2, etc.

html = urllib2.urlopen(url)
html = html.read()
soup = BeautifulSoup(html)

def GrabLinks():
    links = []
    current_link = 'link'
    for link in soup.find_all('a'):
        if str(link.get('href')).startswith('/gms') == True:
            if current_link == link.get('href'): pass
            else:
                links.append(link.get('href'))
                current_link = link.get('href')
        else: pass
    return links
    
def SearchLinks(url_list):
    url_beginning = 'http://' + craigslist_region +'.craigslist.org'
    for item in url_list:
        post_url = url_beginning + item
        post_html = urllib2.urlopen(post_url)
        post_html = BeautifulSoup(post_html.read())
        section_tags = post_html.find('section')
        post_parent = section_tags.parent
        post_parent = post_parent.contents

        
        post_body = post_parent[7]
        keywords = ['mario','Mario','ps3','PS3','ps4','PS4','xbox','Xbox','gameboy','Gameboy','linux','Linux','sega','Sega','brewing','Brewing','books','Books','guitar','Guitar'] #insert your own!
#This is probably better done with regex - I'll have to come back to it.

        for item in keywords:
            if str(post_body).find(item) is not -1:
                print(post_url) + ' I found ' + item + ' here! :D'
# This returns an entry if something is not found. Good for troubleshooting. Uncomment if you want to see negative results as well.
#            if str(post_body).find(item) is -1:
#                print(post_url) + ' No ' + item + ' here. :(' 
       

url_list = GrabLinks()
SearchLinks(url_list)
