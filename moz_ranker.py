
import requests
import json


class MozRanker:

    def __init__(self,target):

        target = target.lower()

        api_host = "https://lsapi.seomoz.com/linkscape"


        end_pt="url-metrics"
        cols="68719476736"  #{domain authority:68719476736 }
        limit="10"
        access_id = "mozscape-149b8b21cf"
        expires = "1363389027"
        signature = "b808392c158303da9e30384ba71d4a7f"


        query = "{}/{}/{}?Cols={}&Limit={}&AccessID={}&Expires={}&Signature={}".format(api_host,end_pt,target,cols,limit,access_id,expires,signature)
        #query = "https://lsapi.seomoz.com/linkscape/url-metrics/moz.com?Cols=4&Limit=10&AccessID=NKzHzYz2BI4SXf&Expires=1363389027&Signature=LmXYcPqc%2BkapNKzHzYz2BI4SXfC% 3D"
        
        #got the content of header form header in web browser when i entered access id as username and signature as password
        headers = {
        "authorization": "Basic bW96c2NhcGUtMTQ5YjhiMjFjZjpiODA4MzkyYzE1ODMwM2RhOWUzMDM4NGJhNzFkNGE3Zg==",
        }


    #print(query,header)
        response = requests.post(query,headers=headers)

        domain_authority_json = json.loads(((response.content).decode("ascii")))

        try:

            self.domain_authority = domain_authority_json['pda']
        
        except KeyError:  # the api throws error sometimes, do not know why, catch it
            raise KeyError
            #self.domain_authority = -1

        #print (type(self.domain_authority))

def main():
    ranker = MozRanker("boatelectric.com")
    print(ranker.domain_authority)


main()
