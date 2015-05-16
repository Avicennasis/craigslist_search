#parses garage sale page, opens individual postings, looks for keywords
import urllib2
from bs4 import BeautifulSoup
import smtplib
import time

craigslist_region = 'boston'
url = 'http://' + craigslist_region + '.craigslist.org/search/gms/'

html = urllib2.urlopen(url)
html = html.read()
soup = BeautifulSoup(html)

def send_text(message):
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login( '@GMAIL_USERNAME@gmail.com', 'GMAIL_PASSWORD' )
    message = '\n' + message
    server.sendmail( 'header', 'YOUR_ATT_PHONENUMBER@mms.att.net', message )
    '''
    Note: For non-AT&T customers, other popular carriers can be reached by using these:
        T-Mobile : @tmomail.net
        Verizon : @vtext.com
        Sprint : @messaging.sprintpcs.com
        Nextel : @messaging.nextel.com
        Virgin Mobile : @vmobl.com
    '''

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
    url_beginning = 'http://' + craigslist_region +'.craigslist.org/'
    for item in url_list:
        post_url = url_beginning + item
        post_html = urllib2.urlopen(post_url)
        post_html = BeautifulSoup(post_html.read())
        meta_tags = post_html.find('meta')
        post_parent = meta_tags.parent
        post_parent = post_parent.contents
        
        post_body = post_parent[7]
        keywords = ['mario','ps3','ps4','xbox','gameboy','linux','sega','brewing'] #insert your own!
        for item in keywords:
            if str(post_body).find(item) is not -1:
                send_text(post_url)
       

url_list = GrabLinks()
SearchLinks(url_list)
