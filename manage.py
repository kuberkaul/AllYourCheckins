#!/usr/bin/env python
import os, foursquare
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AllYourCheckins.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

# Construct the client object
client = foursquare.Foursquare(client_id='RTWQIPCAGNSS0OAQJJ1RQSTULBFSOWXL3Q0PG3HXJOODCMH4', client_secret='JV22GECYYP30YKVXVL0PPUBBTJM2RPGCOJTYGUOBIO33KC5O', redirect_uri='http://localhost/redirect_uri')

# Build the authorization url for your app
auth_uri = client.oauth.auth_url()

# Interrogate foursquare's servers to get the user's access_token
access_token = client.oauth.get_token('XX_CODE_RETURNED_IN_REDIRECT_XX')

# Apply the returned access token to the client
client.set_access_token(access_token)

# Get the user's data
user = client.users()
