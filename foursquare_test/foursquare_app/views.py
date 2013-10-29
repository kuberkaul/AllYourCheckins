# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from django.template import RequestContext, loader, Context
import foursquare, datetime

# Authenticating the user here
def index(request):
	client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView/')
	
	auth_uri = client.oauth.auth_url()
	return redirect(auth_uri)

def mapView(request):
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView/')
    code = request.GET.get('code','')
    # Using access token and creating client object
    accessToken = request.session.get('accessToken')
    if not accessToken:
	accessToken = client.oauth.get_token(code)
	request.session['accessToken'] = accessToken
    client.set_access_token(accessToken)
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    #print name
    


    template = loader.get_template('mapTemplate.html')
    context = Context({"Name":name})
    return HttpResponse(template.render(context))

def imageIndex(request):
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView/')
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
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView/')
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
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView/')
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    print name
    print "hello from search"
    if 'username' in request.GET:
        message = request.GET['username']
    if 'query' in request.GET:
        message1 = request.GET['query']
    if 'startDate' in request.GET:
        message2 = request.GET['startDate']
        message2 = message2.split('/')
   	print message2
    if 'endDate' in request.GET:
	message3 = request.GET['endDate']
	message3 = message3.split('/')
    print client.users.friends()
    print message2
    print "after message2"
    # Time format yyyy/mm/dd/h/s --> epoch conversion
    startDate = (datetime.datetime(int(message2[0]),int(message2[1]),int(message2[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    finalDate = (datetime.datetime(int(message3[0]),int(message3[1]),int(message3[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    
    count = 10
    for i in range(0, count):
        timeFilteredCheckins[i] = (client.users.checkins(params={'beforeTimestamp':startDate,'afterTimestamp':finalDate ,'sort':'oldestfirst','limit':'100'})['checkins']['items'][i]['venue']['name'])
        print "The time filtered checkins are : \n"
        for key,something in timeFilteredCheckins.iteritems():
            print key,something
        print '\n\n'

    return HttpResponse("hello")

