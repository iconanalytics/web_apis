"""
To run this code from scratch go to https://marketplace.akc.org/search-puppies
select poodle type, standard, toy or mini. General poodle will not work
then use inspect tool of chrome developer tools to copy the body of the html to a file
save that file for each page of the search result.
saving the view source file will not work, unfortunately
"""

from bs4 import BeautifulSoup

import requests

import os




def find_value_of_key(entry,key,start_index):  #function for find the value in "key":"value" string representation (entry)
    
    key_index = (entry.find(key,start_index,len(entry)))
    first_quote_index = (entry.find("\"",key_index+len(key),len(entry)))+1
    second_quote_index = (entry.find("\"",first_quote_index,len(entry)))
    value = (entry[first_quote_index:second_quote_index])
    #print(value)
    return [value,second_quote_index]
#poodle_vendors_page = requests.get('https://marketplace.akc.org/puppies/poodle?breed=193&page={}'.format(poodle_vendors_page_number))

save_poodle_page = False

if save_poodle_page == True: #SAVING SOURCE HTML WITH REQUESTS DOES NOT WORK WITH REST OF CODE
    for poodle_vendors_page_number in range(25):
        poodle_vendors_page = requests.get('https://marketplace.akc.org/puppies/poodle?breed=193&page={}'.format(poodle_vendors_page_number+1))
        poodle_file = open("akc_poodle_vendors//"+"poodle_breeder_page{}.txt".format(poodle_vendors_page_number+1),"w")
        poodle_file.write(str(poodle_vendors_page.content))
        poodle_file.close()

onlyfiles = os.listdir("akc_poodle_vendors")
#poodle_vendors_page =  "akc_poodle_vendors//toy_poodle_breeder_page1.txt"

poodle_vendor_csv = open("poodle_vendor_table.csv","a")

for poodle_vendors_file in list(onlyfiles):
    try:
        poodle_vendors_page  = open("akc_poodle_vendors//"+poodle_vendors_file,encoding="utf-8").read()
    except UnicodeDecodeError:
        raise Exception
    soup = BeautifulSoup(poodle_vendors_page)

    breeder_infos = soup.find_all('a',class_="sc-cJSrbW iCqeYh")  #sc-cJSrbW iCqeYh sc-eqIVtm crUPZC is the class name of the div that contains the breeder list

    for breeder_info in breeder_infos:


        breeder_url = (breeder_info["href"])
        breeder_akc_marketplace_url = "https://marketplace.akc.org"+breeder_url
        breeder_akc_page = requests.get(breeder_akc_marketplace_url).content
        breeder_akc_page = str(breeder_akc_page)
        #print(len(breeder_akc_page))

        
        breeder_akc_marketplace_url = breeder_akc_marketplace_url[:[i for i, letter in enumerate(breeder_akc_marketplace_url) if letter == '/'][-2]]
        
        print(breeder_akc_marketplace_url)
        poodle_vendor_csv.write(poodle_vendors_file[0:poodle_vendors_file.index("_")]+";")
        
        for breeder_key in ["breeder-listing\",\"title","contact_name",'display_phone',"city","state_name","display_zip","external_website"]:
            breeder_value = find_value_of_key(breeder_akc_page,"\"{}\":".format(breeder_key),0)[0]
            if breeder_key == "external_website" and "\\/" in breeder_value:
                breeder_value = breeder_value[breeder_value.rindex("\\/")+2:]

            if breeder_value ==  "created_at": #signature for empty website
                breeder_value = ""

            if breeder_value ==  "service": #signature for empty phone number
                breeder_value = ""
            
            print(breeder_value)

            poodle_vendor_csv.write(breeder_value+";")
        poodle_vendor_csv.write(breeder_akc_marketplace_url)
        poodle_vendor_csv.write("\n")


#print((breeder_info))
#print(list(soup.children))