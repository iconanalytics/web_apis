import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import re
import os
import urllib

domain_name= "http://dietandhealths.com/"
all_slugs = [a for a in os.listdir('C:\\My Web Sites\\DietandHealthsDump\\dietandhealths.com')]
all_slugs=["index.html"]
#print((all_slugs))

for slug_item in all_slugs:
    url_to_dump = "http://www.dietandhealths.com/"+slug_item
    slug = re.findall(r'.com/(\S+)', url_to_dump)[0]  #0 index because one list value is expected always

    print("slug: "+slug)

#r = requests.get(url_to_dump)

    try:

        html = urlopen(url_to_dump).read().decode('utf-8')


        soup = BeautifulSoup(html,'html.parser')

        original_html = ((soup.prettify()))

    #print(len(re.findall("dietandhealths", original_html)))

    #ref = ((re.findall("http://dietandhealths.com", original_html)))
    #print((re.findall(r'\"http[s]*:\/\/[dietandhealths.com]+[/][a-z A-z 0-9 . \- \/]+\"$', original_html )))
        all_domain_links=((re.findall(r'http[s]*:\/\/[dietandhealths.com]+[/][a-z A-z 0-9 . \? \= \% \- \/]+', original_html )))

        for domain_link in all_domain_links:
            local_file = re.findall(r'.com/(\S+)', domain_link)[0] #local file is the name that will be used to store domain link locally
            print("local file: "+local_file)

            basedir = os.path.dirname(local_file)
            print("base directory for local file: "+basedir)
            if basedir != '' and not os.path.isdir(basedir) and (basedir != slug): #if the directory does not exist, make it. Dont make a directory with same name as slug
                try:
                    os.makedirs(basedir)
                except FileExistsError as ex: #this happens if a file share the same name as a folder, current quick fix is to delete file to allow folder (rob peter to pay paul scheme)
                    os.remove(ex.filename)
                    os.makedirs(basedir)
            if not os.path.isfile(local_file) and (local_file != slug): #if the file does not exist, download it. dont download slug if it is referenced in html code 
                try:
                    #r= urlretrieve(domain_link, str(local_file))
                    print("domain link to fetch: "+domain_link)
                    domain_link = domain_link.split(" ")[0] # to solve the problem with size attribute in html image name
                    with urllib.request.urlopen(domain_link) as remote_link_file:
                        try:
                            with open(local_file,'wb') as loc_file:
                                loc_file.write(remote_link_file.read())
                                loc_file.close()
                                remote_link_file.close()
                        except PermissionError:
                            print("PERMISSION ERROR WITH "+local_file) #some webfiles are written as what Windows will see as a folder. Cant handle this for now
                        except OSError:
                            print("OS ERROR WITH "+local_file) # probably due to dynamic url which cannot be converted to local url for now

                except urllib.error.HTTPError as url_ex:

                    if url_ex.getcode() in [403,404,500]:
                        print (str(url_ex.getcode())+" error when retrieveing "+local_file)
                    else:
                        raise url_ex
                    

        formatted_html = re.sub(domain_name,"",original_html) #replace absolute address with relative address

        soup = BeautifulSoup(formatted_html,'html.parser')

    #print(formatted_html)

        if os.path.exists(slug): #if a local file with slug name exists, delete it. This is possible because the HTML code of a slug can ref the slug
            print("A file with the SLUG name exists: "+slug)
            os.remove(slug)
        with open(slug, "w",encoding='utf-8') as file:
            file.write(str(soup))
            file.close()

    except Exception as ex_slug:
        print(ex_slug)
        print("Exception fetching Slug..."+slug)


'''
from urllib.request import urlopen
html = urlopen("http://www.dietandhealths.com/").read().decode('utf-8')
print(html)
'''