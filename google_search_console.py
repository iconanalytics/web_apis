import requests


#'https://developers.google.com/oauthplayground/'

headers= {
"Host": "www.googleapis.com",
"Content-length": "0",
"Authorization": "Bearer ya29.a0AfH6SMCMJqr42gv4Z66g8M9m5jul74EoUSvrXtiSwkasFA56KVTccK5YfH0vlMbgfaWNaKqbtki1pnmKMhHWdAatabFAE3KGIPM7aC6qv_dtLGCV-O9-22wgEYEmWO_LCLUgnisk6au6U1RwtvU2AKModM1oLKa75HE",
}
response = requests.get('https://www.googleapis.com/webmasters/v3/sites',headers=headers)

print(response.content)

'''
this work for indexing. Need to verify

https://indexing.googleapis.com/v3/urlNotifications:publish

POST /v3/urlNotifications:publish HTTP/1.1
Host: indexing.googleapis.com
Content-length: 73
Content-type: application/json
Authorization: Bearer ya29.a0AfH6SMDWw9DRsmz_Gs6ZHCUrJPypU2LkvKDgK_7IF-TMGsBJkGsV9qVvtC0H_5IGC_NHulciqW3YXme47mKYI2I6-ml9ZvfS3wrSZUg6acW5dFKAAAZLdIA3dk1g-hw45o8Qbx7I-oHdqAldZRMhAFLWAGJ9U1E-pnY
{
  "url": "http://boatelectric.com/whats.htm",
  "type": "URL_UPDATED"
}

'''


#this works in oauthplaygroud for search console query 
'''
{
  "startDate": "2015-04-01",
  "endDate": "2020-09-09",
  "dimensions": ["country","device"]
}
'''

#https://www.googleapis.com/webmasters/v3/sites/https%3A%2F%2Fhealthtechnik.com%2F/searchAnalytics/query