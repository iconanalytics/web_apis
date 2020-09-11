import requests

"""
processed before(important)
is buynow (important)
is it an active page alive (optional)
has it got authority (important)
has desired key words (optional)
has a blog (optional)
price

out: summary

keywords:review blog health boat wireless radio frequency rf electronic technology business

https://archive.org/wayback/available?url=goeshealth.com&timestamp=19800101
http://web.archive.org/web/20110201165620/http://goldendoodleadvice.com/
http://web.archive.org/web/20070518055407/http://www.standardpoodlesusa.com/Traveling-With-Your-Poodle.html

"""

class BaseWeb:

    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
    
    def getKey(self):
        return self.key

    def getSecret(self):
        return self.secret

class PyCurl():

    def __init__(self):
        

        domain_to_check= 'alphafemale.biz'

        url = "https://api.godaddy.com/v1/domains/available?domain={}".format(domain_to_check)
       
        #url = "https://api.godaddy.com/v1/domains/GetMyDidNotWinSummary?"

        headers = {'Authorization':"sso-key e4s6zQGTgmWX_5DuTfnQgHGVXcC7mqXxpJm:8TnRryvwUD4TBuAo74LdVt"}
        response = requests.get(url,headers=headers)
        #url = "https://auctions.godaddy.com/gdAuctionsWSAPI/gdAuctionsBiddingWS.asmx?wsdl"
        #r = requests.post(url,headers)
        #print(r.content)
        #response = requests.get(url,headers)
        #print(str(response.content))
        print(response.json())
        
        '''

        TRIED OUT USING SOAP FOR AUCTIONS API ACCESS, seems like code worked, but access was denied"
        
        request = u"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <GetAuctionListByAuctionType xmlns="GdAuctionsBiddingWSAPI_v2">
            <pageNumber>string</pageNumber>
            <rowsPerPage>string</rowsPerPage>
            <beginsWithKeyword>string</beginsWithKeyword>
            <auctionType>string</auctionType>
            </GetAuctionListByAuctionType>
        </soap:Body>
        </soap:Envelope>"""
        #print(request)

        encoded_request = request.encode('utf-8')

        headers = {"Host": "auctions.godaddy.com",
            "Content-Type": "text/xml; charset=utf-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "GdAuctionsBiddingWSAPI_v2/GetAuctionListByAuctionType",
            'Authorization':"sso-key e4s6zQGTgmWX_5DuTfnQgHGVXcC7mqXxpJm:8TnRryvwUD4TBuAo74LdVt"}

        response = requests.post(url="http://auctions.godaddy.com/gdAuctionsWSAPI/gdAuctionsBiddingWS_v2.asmx",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

        print (response.content) #print response.text


        request = u"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <GetServiceStatus xmlns="GdAuctionsBiddingWSAPI_v2" />
        </soap:Body>
        </soap:Envelope>"""
        encoded_request = request.encode('utf-8')
        
        #doc: https://auctions.godaddy.com/gdAuctionsWSAPI/gdAuctionsBiddingWS_v2.asmx?op=GetServiceStatus
        headers = {"Host": "auctions.godaddy.com",
            "Content-Type": "text/xml; charset=utf-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "GdAuctionsBiddingWSAPI_v2/GetServiceStatus",
            'Authorization':"sso-key e4s6zQGTgmWX_5DuTfnQgHGVXcC7mqXxpJm:8TnRryvwUD4TBuAo74LdVt"}

        response = requests.post(url="http://auctions.godaddy.com/gdAuctionsWSAPI/gdAuctionsBiddingWS_v2.asmx",
                        headers = headers,
                        data = encoded_request,
                        verify=False)
        
    '''

def main():
    p = PyCurl()
main()
