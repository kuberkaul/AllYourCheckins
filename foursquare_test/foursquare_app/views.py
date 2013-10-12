# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from django.template import RequestContext
import foursquare

# Authenticating the user here
def index(request):
	client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/welcome/')
	
	auth_uri = client.oauth.auth_url()
	return redirect(auth_uri)

# Welocming user with the data extracted. 
def welcome(request):
	code = request.GET.get('code','')
	client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/welcome/')
	
	# Using access token and creating client object
	accessToken = client.oauth.get_token(code)
	client.set_access_token(accessToken)
	all_checkins = client.users.checkins()

	#  Printing 10 checkins of the user
	first10={}
	for i in range(1,10):
		first10[i] = all_checkins['checkins']['items'][i]['venue']['name']
	print 'The latest 10 Checkins of user are : '
	for key,value in first10.iteritems():
		print key,value 
	print '\n\n\n\n\n\n'

	#  Printing 10 names of friends user has
	friends = {}
	print 'All friends of user are :'
	for i,key in enumerate(client.users.friends()['friends']['items']):
		friends[i] = key['lastName']
		print i,key['firstName'] 
	print '\n\n\n\n\n\n'
	

	# Returns a list of venues near the current location, optionally matching a search term. 
	venueSearch = client.venues.search(params={'query': 'coffee', 'near': 'Manhattan, NY'})
	#print venueSearch
	filterCheckins = {}
	for i in range (1, 10):
		filterCheckins[i] = venueSearch['venues'][i]['name']
	print ' 10 filtered location for coffee in Manhattan, Ny are :'
	for key, value in filterCheckins.iteritems():
		print key, value 
	print '\n\n\n\n'


	# Returns a list of recent checkins from friends.
	friendsCheckinsDict =  client.checkins.recent(params={'id':'5134447'})
	print friendsCheckinsDict	
	friendsCheckins = {}
	for i in range(1,10):
               friendsCheckins[i] = friendsCheckinsDict['recent'][i]['venue']['name']
        print 'The latest 10 Checkins of users friends are : '
        for key,value in friendsCheckins.iteritems():
                print key,value
	return render_to_response('my_checkins.html',{'first10':first10, 'friends':friends})
