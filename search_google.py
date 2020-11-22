import requests
import json





API_KEY = "AIzaSyAHFJi3FiHIvuM64a-Km5mqXExX0-C-dow"  
#api key from https://console.cloud.google.com/apis/credentials?folder=&organizationId=&project=pythonwebsearch 

CSE_ID = "011125311224649493392:r49ie4v4cav"

MAX_SERP_PAGES= 10
query = "marine barbecues galleymate"
result_start = 0

index = 1
for page_number in range(10): 

    get_cmd = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&start={}".format(API_KEY,CSE_ID,query,(page_number*10)+1)
    #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list  parameters for search documentation
    response = requests.get(get_cmd)

    search_result = json.loads(((response.content)))

    for position in range (10):
        result_link = (search_result["items"][position]["link"])
        print(str(index) + " "+result_link)
        if "boatelectric.com" in result_link:
            raise Exception
        index = index + 1

