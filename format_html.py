from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os

domain_name = "http://dietandhealths.com/"
files_to_format = os.listdir(".")
files_to_format = [a for a in files_to_format if os.path.splitext(a)[1] ==".html" and os.path.isfile(a)]

for file_to_format in files_to_format:
    print("formatting file "+file_to_format+"....")

    file = open(file_to_format, 'r',encoding='utf-8')
    html_to_format=file.read()
    file.close()



    html_to_format=re.sub("category/diet-plans-tips","category/diet-plans-tips.html",html_to_format)  #to fix menu items
    html_to_format=re.sub("category/weight-loss-diet","category/weight-loss-diet.html",html_to_format)
    html_to_format=re.sub("category/diet-food-menu","category/diet-food-menu.html",html_to_format)
    html_to_format=re.sub("category/diet-products","category/diet-products.html",html_to_format)
    html_to_format=re.sub("category/pregnancy","category/pregnancy.html",html_to_format)

    html_to_format=re.sub(domain_name,"../",html_to_format) #change all absolute urls to relative


    soup = BeautifulSoup(html_to_format,'html.parser')


    (soup.find("meta",  {"name":"google-site-verification"})).decompose()  # remove original google tracking id
    (soup.find("meta",  {"name":"msvalidate.01"})).decompose() #remove original bing tracking id


    soup.find('a', {'class':'icon-twitter'}).decompose() #remove header twitter information
    soup.find('a', {'class':'icon-facebook'}).decompose() #remove header facebook information
    soup.find('a', {'class':'icon-facebook'}).decompose() #remove header email information

    soup.find('ul', {'class':'footer-social-icons'}).decompose() #remove social media footer information
    soup.find('div', {'class':'copyright'}).decompose() #remove earlier copyright information

    #print(soup.select(".copyright"))


    '''
    for tag in (soup.select('a')):
        try:
            print(tag['href'].sting.replace('category/diet-plans-tips','category/diet-plans-tips.html'))

        except KeyError: #for some reason i need to find out, key error occurs for some hrefs
            pass

    '''
    with open(file_to_format, "w",encoding='utf-8') as file:
        file.write(str(soup))
        file.close()

    #print(soup.prettify())