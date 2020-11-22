import json
import ijson
import urllib
from webpage import Webpage
from InternetWayBack import InternetWayBack
from moz_ranker import MozRanker
import os.path


"""
To work on the latest list of auctions, run godaddy_auction_ftp.py first
"""

class GodaddyAuctionJson:

    
    def __init__(self, json_file):

        

        self.index = -1 #starting index to iterate through godaddy domain list json
        auction_interest_keys = ['data.item.domainName','data.item.link','data.item.auctionType',
            'data.item.auctionEndTime','data.item.price']  # the keys in the json file that i want
        auction_interest_values = ['']*len(auction_interest_keys) # their corresponding values
        i = 0
        count = 0
        item_index = 0  #index of one of the key of interest

        self.trove_file = "trove_domain_for_dog.txt"
        #keywords = ["BOAT", "SAIL", "MARIN", "NAUTICA","ROWING"] #for boatelectric
        #keywords = ["CLINIC","DOCTOR","NURS","HEALTH","MEDIC","HOSPITAL"] 
        keywords = ["DOG","POODLE","PUP","CANINE","WHELP","POOCH","MUTT","ROVER"]
        keywords =['POODLE']


        self.done_domains = self.init_done_domains(self.trove_file)  # what domains do we know of already


        for a in ijson.parse(open(json_file, encoding="utf-8")):
            

            if a[0] in auction_interest_keys and item_index < len(auction_interest_keys):
                auction_interest_values[item_index] = a[2]
                item_index = item_index + 1
            if item_index == len(auction_interest_keys):
                item_index = 0

                #code to check if a keyword-rich auction test_domain is available for sale 
                test_domain = auction_interest_values[0]
                print ("checking out the domain {}".format(test_domain))
                

                if self.domain_not_in_trove(test_domain): #if the domain has not been shortlisted before, this is necessary to avoid wasting moz api call 

                    if any(match in test_domain for match in keywords): # check if test_domain contains keyword
                        
                        archiveddomain = InternetWayBack(test_domain)

                        if (archiveddomain.archive_exist()): #if archive exists, then check domain rating

                            

                            count = count + 1
                            print ("Moz ranker use count :{}".format(count))

                            ranker=MozRanker(test_domain)
                            domain_authority = ranker.domain_authority

                            print("domain authority is : "+str(domain_authority))

                            f = open(self.trove_file, "a")
                            f.write(str(count)+";"+str(domain_authority)+";"+auction_interest_values[4]+";"+
                            auction_interest_values[2]+";"+
                            test_domain+";"+
                            archiveddomain.oldest_archive_date()+";"+
                            archiveddomain.newest_archive_date()+";"+
                            str(archiveddomain.number_of_captures())+"\r")
                            f.close()
                #end of code

                '''
                if (auction_interest_values[2] != 'Bid'): # check domain which are NOT for Bid
                    test_domain = auction_interest_values[0]
                    print ("checking out the domain {}".format(test_domain))

                    

                    
                    try:
                        webpage = Webpage(test_domain)
                        is_live = webpage.is_live_hosted_page()

                    except IOError:
                        print("WEB FETCH ERROR")
                        is_live = False
                    except Exception as ex:
                        f = open("error_file.txt", "a")
                        f.write(test_domain+" "+str(ex)+"\r\n")
                        f.close()

                    

                    if (is_live):
                        print(str(count)+" "+auction_interest_values[4]+" "+test_domain)
                        count = count + 1
                        f = open("trove_file.txt", "a")
                        f.write(str(count)+" "+auction_interest_values[4]+" "+test_domain+"\r\n")
                        f.close()
                '''
                    

    def init_done_domains(self,trove_file): #domains that we know of

        done_domains = []
        if os.path.exists(self.trove_file):
            f = open(self.trove_file, "r")
            

            while True:
                a = f.readline()
                if not a:
                    break

                done_domains.append(a.split(";")[4])
                

            f.close()
        return done_domains

    def domain_not_in_trove(self,domain):
        #print(domain+" not in trove")
        return domain not in self.done_domains


    def next_domain(self):
        self.index = self.index +1
        #print(self.json_obj["data"][self.index]['domainName'])
        yield self.json_obj["data"][self.index]['domainName']


def main():
    auction_ftp_files = ['all_non_adult_listings.json','all_non_adult_listings2.json'
    ,'all_non_adult_listings3.json']
    for auction_ftp_file in auction_ftp_files:
        json_obj = GodaddyAuctionJson(auction_ftp_file)
    #while True:
        #print(next(json_obj.next_domain()))
        
main()