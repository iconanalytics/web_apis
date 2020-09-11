import requests

from bs4 import BeautifulSoup

from urllib.request import urlopen

import re

class Webpage:
    def __init__(self,domain_to_scrape):

        self.domain_to_scrape = domain_to_scrape

        if domain_to_scrape.startswith("http"): # if domain has schema already, do not worry about adding one

            self.webpage_html = urlopen(self.domain_to_scrape).read().decode('utf-8')
        
        else: #append schema

            try: #try https first

                self.webpage_html = urlopen("https://"+self.domain_to_scrape).read().decode('utf-8')

            except Exception: # if there is an exception, try http

                self.webpage_html = urlopen("http://"+self.domain_to_scrape).read().decode('utf-8')


        self.webpage_soup = BeautifulSoup(self.webpage_html,'html.parser')


    def webpage_keyword_count(self, keyword):
        return len(re.findall(keyword, self.webpage_html))

    def is_keyword_in_domain_name(self,keyword):

        return keyword in self.domain_to_scrape

    def is_live_hosted_page(self): # check if page is parked or live
        backlink_threshold = 10 # if there are  10 internal backlinks that contain the domain name, then domain is live, we assume that links are absolute urls
        number_of_internal_backlinks = 0
        for link in self.webpage_soup.findAll('a'):
            if link.has_attr('href'):
                if self.domain_to_scrape.lower() in link['href'].lower():
                    number_of_internal_backlinks = number_of_internal_backlinks + 1
                    if number_of_internal_backlinks >= backlink_threshold:
                        return True

        return False


def main():
    domain = "https://auctions.godaddy.com/trpItemListing.aspx?miid=330776329&isc=json_all_listings"
    domain = "RMMANDPSA.COM"

    try:
        webpage = Webpage(domain)
        print(webpage.is_keyword_in_domain_name("health"))
        print(webpage.webpage_keyword_count(keyword="godaddy"))
        
        print(webpage.is_live_hosted_page())
    except IOError as ex:
        print("there was an exception")
        print(ex)



main()


