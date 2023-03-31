from django.shortcuts import render
from django.http import JsonResponse
from . import linkedinf
import traceback

import os
import sys
from linkedin import linkedin
import json
from django.http import JsonResponse
# from linkedin_api import Linkedin
from django.http import HttpResponse
from linkedin.exceptions import LinkedInError
from linkedin import exceptions as LinkedInExceptions
import requests
from django.shortcuts import redirect, render
# from linkedin.exceptions import HTTPError
from requests.exceptions import HTTPError
from linkedin_api.clients.restli.client import RestliClient
from . import post_and_comments_scraping 

def scrape_comments(request):
    post_and_comments_scraping.loginAndGetData()
    return render(request, 'scrape_comments.html')
#     print('request')
#     # print(request.GET['code'])
#     if request.method == 'GET' and 'code' in request.GET:
#         CLIENT_ID = '86c5ahzd57x714'
#         CLIENT_SECRET = 'yuZyzK5vpixUUWM6'
#         REDIRECT_URI = 'http://localhost:8000'

#         # Create the LinkedIn authentication object
#         authentication = linkedin.LinkedInAuthentication(
#             CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,linkedin.PERMISSIONS.enums.values()

#         )

#         # # # Get the authorization URL and print it out
#         # auth_url = authentication.authorization_url
#         # print(f'Please go to this URL to authorize the application: {auth_url}')

#         # # Get the authorization code from the user and exchange it for an access token
#         # authorization_code = input("enter the access code boss")
#         authentication.authorization_code = request.GET['code']

#         # access_token ="AQW0L8ry8l2b4da8_slAoDtvAU1IGLb6Kj5_QINBj17G5C3aNcYO2sEvSYqzz-Sm2lhGZ8al8W_BeBaoLjsGVseQHyfy0utE9reBn7QkKKD8YIkh9XuLWfRlV_KZ-E4MFsAZ4fiZxTASBvvOVHGAp90B5XkfIG06sx5gX0oM5PaiYIJuOFhbqv9WSjTJwtaobxomt13t_5B235y06OsQylcVDFlOPcMxhoR6ZdbPdUVVFSjybYmq30dXRaer8aWkAreDHbDG0BrAjp0NcZ8s6N5bO5PrraD_b_h3V20fV0aDCrQxT-51zfAoLocrOxeFcHCNxGTUSCTmDRFY1d4T1FK6Job-qw"
#         access_token = authentication.get_access_token().access_token
#         # access_token = "AQXoEIEW_Ze4RSgYYWfJEXfkt_5RAcme2cDq1tEL5l0mLzsKYh4ArR5Ja1EAliMtPt_WCiP1fCvOnDFcpfSI7eRUvbo30Kp4NbtfD9_pnzUIbeYooq4rWUYntpvATVvRmV5pNIXbvxEXmgXTqE7IG0w3kHPAl1YnEogVMelqDaYCoQKVtcjEyy4OypzbHMeTFu01SgaGp_ZzUSX4LGETC0X2qwFJXT7KCQe3JYsVxNfuaSc1W-yXMR0zo_gir_8TKXW-_YHmrpRgbpX9M24DQ0195SZTAGK3de64a63_loYxpbPMpOpGI38zyg0fuvn8tqK53JmlHiXaApcULmkkH-wcx5NsHA"
#         print('access')
#         print(access_token)

#         # Use access token to retrieve comments from a post
#         application = linkedin.LinkedInApplication(token=access_token)
#         # print(dir(application))
#         # post_id = '6908026548063215616'
#         post_id = "7046223315325091840"
#         # restli_client = RestliClient()

#         try:
#         #     print("ahhh")
#         #     posts = application.get_companies()
#             # print(posts)
#             restli_client = RestliClient()
#             # restli_client.access_token = access_token

#             # response = restli_client.get('/v2/ugcPosts?q=authors&authors=me&count=10')

#             resource_path = "/rest/posts"
#             query_params = {
#                 "owner": "urn:li:person:me",
#                 "count": 10,
#                 "sortOrder": "RECENT"
#             }

#             # Make the GET request to fetch the user's posts
#             response = restli_client.get(resource_path=resource_path,access_token=access_token,version_string="202303")
#             # response = restli_client.get(resource_path="/v2/posts", query_params={ "owner":"urn:li:person:me", "authors":'me',"count": 10 },access_token=access_token,version_string="202302")
# # path_keys = {'id':'emmanuel-audu-826051163'}
# # Make a GET request to the /organizationalEntityShareStatistics endpoint to retrieve the user's posts
#             # response = restli_client.get(
#             #     resource_path='organizationalEntityShareStatistics',
#             #     query_params={
#             #         'q': 'organizationalEntity',
#             #         'organizationalEntity': 'urn:li:organization:emmanuel-audu-82605116',
#             #         'timeIntervals.timeGranularityType': 'DAY',
#             #     },
#             #     access_token=access_token
#             # )
#             # for post in response.entity['elements']:
#             #     print(post)
#             print(response.entity)
#         except AttributeError as e:
#             traceback.print_exc()
#         except requests.exceptions.HTTPError as err:
#             print(err.response.text)
#         except Exception as e:
#             print(type(e))
#             print(e)
#             print("ahhahahah")
#         except Exception as e: 
#             print(e)
#         except LinkedInError as e:
#             print(f"LinkedInError: {e}")
#         except json.decoder.JSONDecodeError as e:
#             print(f"Error decoding JSON response: {e}")  
#         except requests.exceptions.RequestException as e:
#             print(f"Error making request: {e}")
#         return render(request, "scrape_comments_show.html", {})
#         # return HttpResponse(json.dumps(comments), content_type='application/json')

#     else:
#         CLIENT_ID = '86c5ahzd57x714'
#         CLIENT_SECRET = 'yuZyzK5vpixUUWM6'
#         REDIRECT_URI = 'http://localhost:8000'
#         SCOPE = ['r_liteprofile', 'r_emailaddress', 'w_member_social']

#         # Redirect user to LinkedIn authorization page
#         authentication = linkedin.LinkedInAuthentication(
#             CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,SCOPE
#         )
#         auth_url = authentication.authorization_url
#         print('auth url: ')
#         print(auth_url)
#         # return redirect(auth_url)
#         return render(request, "scrape_comments.html", {"auth_url": auth_url})


# def scrape_comments(request):
#     linkedinf.scrape_comments(request)
#     return render(request, 'scrape_comments.html')
#     return JsonResponse({'status': 'success'})