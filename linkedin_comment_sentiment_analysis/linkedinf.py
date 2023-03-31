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



def scrape_comments(request):
    if request.method == 'GET' and 'code' in request.GET:
        CLIENT_ID = '86c5ahzd57x714'
        CLIENT_SECRET = 'yuZyzK5vpixUUWM6'
        REDIRECT_URI = 'http://localhost:8000'
        SCOPE = ['r_liteprofile', 'r_emailaddress', 'w_member_social']

        # Create the LinkedIn authentication object
        authentication = linkedin.LinkedInAuthentication(
            CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,SCOPE
        )

        # # # Get the authorization URL and print it out
        # auth_url = authentication.authorization_url
        # print(f'Please go to this URL to authorize the application: {auth_url}')

        # # Get the authorization code from the user and exchange it for an access token
        # authorization_code = input("enter the access code boss")
        authentication.authorization_code = request.GET['code']

        # access_token ="AQW0L8ry8l2b4da8_slAoDtvAU1IGLb6Kj5_QINBj17G5C3aNcYO2sEvSYqzz-Sm2lhGZ8al8W_BeBaoLjsGVseQHyfy0utE9reBn7QkKKD8YIkh9XuLWfRlV_KZ-E4MFsAZ4fiZxTASBvvOVHGAp90B5XkfIG06sx5gX0oM5PaiYIJuOFhbqv9WSjTJwtaobxomt13t_5B235y06OsQylcVDFlOPcMxhoR6ZdbPdUVVFSjybYmq30dXRaer8aWkAreDHbDG0BrAjp0NcZ8s6N5bO5PrraD_b_h3V20fV0aDCrQxT-51zfAoLocrOxeFcHCNxGTUSCTmDRFY1d4T1FK6Job-qw"
        access_token = authentication.get_access_token().access_token
        print('access')
        print(access_token)

        # Use access token to retrieve comments from a post
        application = linkedin.LinkedInApplication(token=access_token)
        # print(dir(application))
        post_id =  '6980927128733188096'
        try:
            comments = application.get_post_comments(post_id)
            print(comments)
        except requests.exceptions.HTTPError as e:
            print(f"An HTTP error occurred: {e.response.text}")
        
        return HttpResponse(json.dumps(comments), content_type='application/json')
    else:
        CLIENT_ID = '86c5ahzd57x714'
        CLIENT_SECRET = 'yuZyzK5vpixUUWM6'
        REDIRECT_URI = 'http://localhost:8000'
        SCOPE = ['r_liteprofile', 'r_emailaddress', 'w_member_social']

        # Redirect user to LinkedIn authorization page
        authentication = linkedin.LinkedInAuthentication(
            CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,SCOPE
        )
        auth_url = authentication.authorization_url
        print('auth url: ')
        print(auth_url)
        # return redirect(auth_url)
        return render(request, "scrape_comments.html", {"auth_url": auth_url})

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if the user provided the --scrape-comments flag
    if len(sys.argv) > 1 and sys.argv[1] == '--scrape-comments':
        scrape_comments()
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
