# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from django.template import RequestContext, loader, Context
import foursquare

# Authenticating the user here
def index(request):
	global client
	client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView/')
	
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

	#  Printing 10 checkins of the user between a given timeperiod.
	first10={}
	timeFilteredCheckins = {}
	print client.users.checkins(params={'beforeTimestamp':'1350311510','sort':'oldestfirst','limit':'6'})
	
	for i in range(0, 6):
		timeFilteredCheckins[i] = (client.users.checkins(params={'beforeTimestamp':'1350311510','afterTimestamp':'1318689110 ' ,'sort':'oldestfirst','limit':'6'})['checkins']['items'][i]['venue']['name'])

	
	print "The latest 6 checkins after 07/01/2011 and before 07/01/2012 are : \n"
	for key,something in timeFilteredCheckins.iteritems():
		print key,something
	print '\n\n'
	
	#Printing 10 checkins of the user	
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
		friends[i] = key['firstName']
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
	#print friendsCheckinsDict	
	friendsCheckins = {}
	for i in range(1,10):
               friendsCheckins[i] = friendsCheckinsDict['recent'][i]['venue']['name']
        print 'The latest 10 Checkins of users friends are : '
        for key,value in friendsCheckins.iteritems():
                print key,value


	return render_to_response('my_checkins.html',{'first10':first10, 'friends':friends})


def mapView(request):
    code = request.GET.get('code','')
    # Using access token and creating client object
    accessToken = request.session.get('accessToken')
    if not accessToken:
	accessToken = client.oauth.get_token(code)
	request.session['accessToken'] = accessToken
    client.set_access_token(accessToken)
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    print name
    


    template = loader.get_template('mapTemplate.html')
    context = Context({"Name":name})
    return HttpResponse(template.render(context))

def imageIndex(request):
    # TODO - I'd like to call a function here that returns all of the signed-in user's saved timeline images.
    client.set_access_token(request.session.get('accessToken'))

    imageList = []
    imageList.append({"src": "http://gadgetsteria.com/wp-content/uploads/2013/06/wpid-foursquare-time-top1.jpg", "title": "First Timeline"})
    imageList.append({"src": "http://wac.450f.edgecastcdn.net/80450F/lite987.com/files/2013/06/foursquare-time-machine-all-places-map.jpg", "title": "Another Timeline"})
    imageList.append({"src": "http://media.mediapost.com/dam/cropped/2013/06/13/san-francisco-map-b_2.jpg", "title": "Timeline 3"})
    imageList.append({"src": "http://images.itechpost.com/data/images/full/6964/foursquare-time-machine.jpg", "title": "Fourth"})
    imageList.append({"src": "http://monikarunstrom.com/blog/wp-content/uploads/2013/06/Screen-Shot-2013-06-13-at-9.20.57-AM.png", "title": ""})

    template = loader.get_template('imageIndexTemplate.html')
    context = Context({"imageList": imageList})
    return HttpResponse(template.render(context))

def friendIndex(request):
    # TODO - I'd like to call a function here that returns all of the signed-in user's friends.
    client.set_access_token(request.session.get('accessToken'))
    friends = []
    print 'All friends of user are :'
    print client.users.friends()
    for i,key in enumerate(client.users.friends()['friends']['items']):
	if 'photo' not in key:
		photo = " "
	else:
		photo = key['photo']

	if 'homeCity' not in key:
		homeCity = " "
	else:
		homeCity = key['homeCity']

	if 'lastName' not in key:
		lastName = " "
	else:
		lastName = key['lastName']
        friends.append([key['firstName'],lastName,photo,homeCity])
        #print i,key['firstName'] 

    template = loader.get_template('friendIndexTemplate.html')
    context = Context({"usernameList": friends})
    return HttpResponse(template.render(context))
