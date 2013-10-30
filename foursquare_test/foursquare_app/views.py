# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from django.template import RequestContext, loader, Context
import foursquare, datetime
from django.contrib.auth import logout

#from sets import set

# Authenticating the user here
def index(request):
	try:
		del request.session['accessToken']
	except KeyError:
		pass
	client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
	
	auth_uri = client.oauth.auth_url()
	return redirect(auth_uri)

def mapView(request):
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    code = request.GET.get('code','')
    # Using access token and creating client object
    accessToken = request.session.get('accessToken')
    if not accessToken:
	accessToken = client.oauth.get_token(code)
	request.session['accessToken'] = accessToken
    client.set_access_token(accessToken)
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    #print name


    template = loader.get_template('mapTemplate.html')
    context = Context({"Name":name})
    return HttpResponse(template.render(context))

def imageIndex(request):
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    # TODO - I'd like to call a function here that returns all of the signed-in user's saved timeline images.
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']

    imageList = []
    imageList.append({"src": "http://gadgetsteria.com/wp-content/uploads/2013/06/wpid-foursquare-time-top1.jpg", "title": "First Timeline"})
    imageList.append({"src": "http://wac.450f.edgecastcdn.net/80450F/lite987.com/files/2013/06/foursquare-time-machine-all-places-map.jpg", "title": "Another Timeline"})
    imageList.append({"src": "http://media.mediapost.com/dam/cropped/2013/06/13/san-francisco-map-b_2.jpg", "title": "Timeline 3"})
    imageList.append({"src": "http://images.itechpost.com/data/images/full/6964/foursquare-time-machine.jpg", "title": "Fourth"})
    imageList.append({"src": "http://monikarunstrom.com/blog/wp-content/uploads/2013/06/Screen-Shot-2013-06-13-at-9.20.57-AM.png", "title": ""})

    template = loader.get_template('imageIndexTemplate.html')
    context = Context({"imageList": imageList,"Name":name})
    return HttpResponse(template.render(context))

def friendIndex(request):
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    # TODO - I'd like to call a function here that returns all of the signed-in user's friends.
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']

    friends = []
    #print 'All friends of user are :'
    #print client.users.friends()
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
    context = Context({"usernameList": friends,"Name":name})
    return HttpResponse(template.render(context))

def search(request):
    print "hello world"
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    timeFilteredCheckinsBefore = {}
    timeFilteredCheckinsAfter = {}
    venueNamesBefore = []
    venueNamesAfter = []
    commonSet = []
    putToMap = dict() 
    timeFilteredCheckinsBefore.clear()
    timeFilteredCheckinsAfter.clear()

    if 'user' in request.GET:
        message = request.GET['user']
    if 'query' in request.GET:
        message1 = request.GET['query']
    if 'startDate' in request.GET:
        message2 = request.GET['startDate']
        message2 = message2.split('-')
	print message2
    if 'endDate' in request.GET:
	message3 = request.GET['endDate']
	message3 = message3.split('-')
	print message3

    if (request.GET['startDate'] == "" and request.GET['endDate'] != ""):
        finalDate = (datetime.datetime(int(message3[0]),int(message3[1]),int(message3[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
        finalDate = int(finalDate)
        for i,key in enumerate(client.users.checkins(params={'beforeTimestamp':finalDate})['checkins']['items']):
        	timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
        	venueNamesBefore.append(key['venue']['name'])
        return HttpResponse(venueNamesBefore)

    elif (request.GET['endDate'] == "" and request.GET['startDate'] != ""):
	startDate = (datetime.datetime(int(message2[0]),int(message2[1]),int(message2[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
	startDate = int(startDate)
	for i,key in enumerate(client.users.checkins(params={'afterTimestamp':startDate})['checkins']['items']):
        	timeFilteredCheckinsAfter[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
        	venueNamesAfter.append(key['venue']['name'])
	return HttpResponse(venueNamesAfter)
    
    elif (request.GET['endDate'] == "" and request.GET['startDate'] == ""):
	for i,key in enumerate(client.users.checkins()['checkins']['items']):
	        timeFilteredCheckinsAfter[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
        	venueNamesAfter.append(key['venue']['name'])
	return HttpResponse(venueNamesAfter)
    startDate = (datetime.datetime(int(message2[2]),int(message2[1]),int(message2[0]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    finalDate = (datetime.datetime(int(message3[2]),int(message3[1]),int(message3[0]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    startDate = int(startDate)
    finalDate = int(finalDate)

    for i,key in enumerate(client.users.checkins(params={'beforeTimestamp':finalDate})['checkins']['items']):
	
        timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
        venueNamesBefore.append(key['venue']['name'])

    for i,key in enumerate(client.users.checkins(params={'afterTimestamp':startDate})['checkins']['items']):
        timeFilteredCheckinsAfter[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
        venueNamesAfter.append(key['venue']['name'])

    for before in venueNamesBefore:
	for after in venueNamesAfter:
            if(before == after):
                commonSet.append(before)
    intersectionNames = set(commonSet)
    for something in intersectionNames:
	if something in timeFilteredCheckinsBefore.keys():
		print something , timeFilteredCheckinsBefore[something]
		putToMap[something] = timeFilteredCheckinsBefore[something]
	else:
		putToMap[something] = timeFilteredCheckinsBefore[something]
		print something, timeFilteredCheckinsAfter[something]
    for i in putToMap:
	print i ,putToMap[i]
    print putToMap   
    return HttpResponse(putToMap)


def login(request):
    if request.session['accessToken']:
        del request.session['accessToken']
    template = loader.get_template('login.html')
    context = Context()
    return HttpResponse(template.render(context))
def logoutuser(request):
    return redirect("https://foursquare.com/oauth2/authorize?client_id=AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR&response_type=code&redirect_uri=http://localhost:8000/foursquare_app/mapView")
def loginError(request):
    template = loader.get_template('login.html')
    context = Context({"errorMessage": "The username or password you entered is incorrect"})
    return HttpResponse(template.render(context))

