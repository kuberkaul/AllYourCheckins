# Create your views here.

#importing dependencies for the project
from django.http import HttpResponse
from django.shortcuts import redirect,render_to_response
from django.template import Context, loader, RequestContext
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import forms
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from foursquare_app.models import savedTimelines
import base64, datetime, mimetypes, foursquare 

# Authenticating the user here using oauth2
def index(request):
	try:
		del request.session['accessToken']
	except KeyError:
		pass
	client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
	auth_uri = client.oauth.auth_url()
	return redirect(auth_uri)

# Saving the image(base64 string) on AWS-S3 here with key as firstname, lastname
def mapView(request):
    # Checking for authentication again
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    code = request.GET.get('code','')
    friendid = request.GET.get('userid','')
    friendname = request.GET.get('firstName','')
    accessToken = request.session.get('accessToken')

    # Checking for access token for further authentication
    if not accessToken:
	accessToken = client.oauth.get_token(code)
	request.session['accessToken'] = accessToken

    client.set_access_token(accessToken)
    client.set_access_token(request.session.get('accessToken'))
    currentUser = client.users()['user']['firstName']+" "+client.users()['user']['lastName']

    if friendid:
        name = friendname
        id = friendid
    else:
        name= currentUser 
        id = '' 
    imageString = request.POST.get('imageString','')
    
    # Saving the image to S3 here using BOTO
    if imageString:
    	conn = S3Connection(settings.ACCESS_KEY, settings.SECRET_ACCESS_KEY)
    	b = conn.create_bucket("allyourcheckinsimages"+client.users()['user']['id'])
    	k = Key(b)
    	k.key = client.users()['user']['id']+"_"+unicode(datetime.datetime.now()) 
    	k.set_contents_from_string(imageString)
    else:
	"Error no string"

    template = loader.get_template('mapTemplate.html')
    context = RequestContext(request,{"CurrentUser":currentUser,"Name":name,"Id":id})
    return HttpResponse(template.render(context))

# Displaying all the images in the image index tab from AWS-S3 for download.
def imageIndex(request):
    # Checking for authentication of the user
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    currentId = client.users()['user']['id']   
    imageList = []
    
    # Connecting to S3 using BOTO
    try:
    	conn = S3Connection(settings.ACCESS_KEY, settings.SECRET_ACCESS_KEY)
    	b = conn.get_bucket("allyourcheckinsimages"+client.users()['user']['id'])
    	for k in b.list():
		l=k.key.split("_")
		if l[0]==client.users()['user']['id']:
    	    		src=k.get_contents_as_string()
	    		imageList.append({"src": src,"title": "First Timeline"})
    	template = loader.get_template('imageIndexTemplate.html')
    	context = RequestContext(request,{"imageList": imageList,"Name":name})
	print "reached end of imageindex"
    	return HttpResponse(template.render(context))
    except:
	template = loader.get_template('imageIndexTemplate.html')
        context = RequestContext(request,{"imageList": imageList,"Name":name})
        return HttpResponse(template.render(context))

# Displaying all friends of the user in the friends tab
def friendIndex(request):
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    client.set_access_token(request.session.get('accessToken'))
    name=client.users()['user']['firstName']+" "+client.users()['user']['lastName']

    friends = []
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
        friends.append([key['id'],key['firstName'],lastName,photo,homeCity])

    template = loader.get_template('friendIndexTemplate.html')
    context = RequestContext(request,{"usernameList": friends,"Name":name})
    return HttpResponse(template.render(context))

# The main function of the backend, which processes the inputs from the frontend and then processes that as parameter for the Foursquare API using M-Lewis library and then sends the xml data back to the front end for display.
def search(request):
    # Checking authentication for the user again 
    client = foursquare.Foursquare(client_id='AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR', client_secret='4TISHB1NWZUHLBRPXDT0ULL0EUBEREKRVHGR1QPZKTM3ILKP', redirect_uri='http://localhost:8000/foursquare_app/mapView')
    client.set_access_token(request.session.get('accessToken'))
    currentUser = client.users()['user']['firstName']+" "+client.users()['user']['lastName']
    timeFilteredCheckinsBefore = {}
    timeFilteredCheckinsAfter = {}
    venueNamesBefore = []
    venueNamesAfter = []
    commonSet = []
    putToMap = dict() 
    timeFilteredCheckinsBefore.clear()
    timeFilteredCheckinsAfter.clear()
    template = loader.get_template('mapTemplate.html')

    
    if 'startDate' not in request.GET:
        startDate = ""

    if 'username' in request.GET:
        username = request.GET['username']
	print "username is : " + username
    else:
	print "current user"

    if 'userid' in request.GET:
 	userid = request.GET['userid']
	print "userid is : " + userid
	friends_checkins = client.checkins.recent()
    else:
	print "current userid"

    if 'query' in request.GET:
        message1 = request.GET['query']
    if 'startDate' in request.GET:
        message2 = request.GET['startDate']
        message2 = message2.split('-')
    if 'startDate' in request.GET:
    	if request.GET['startDate'] != "":
		startDate = (datetime.datetime(int(message2[0]),int(message2[1]),int(message2[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    		startDate = int(startDate)
    		friends_checkins_timestamp = client.checkins.recent(params={'afterTimestamp':startDate})
    if 'endDate' in request.GET:
	message3 = request.GET['endDate']
	message3 = message3.split('-')

    if (request.GET['startDate'] == "" and request.GET['endDate'] != ""):
        finalDate = (datetime.datetime(int(message3[0]),int(message3[1]),int(message3[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
        finalDate = int(finalDate)

     	if 'userid' in request.GET:
	   	for i,key in enumerate(friends_checkins['recent']):  
			if friends_checkins['recent'][i]['user']['id']  == userid:			      			      	    timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
	 		else:
				pass
	else:
		for i,key in enumerate(client.users.checkins(params={'beforeTimestamp':finalDate})['checkins']['items']):
     			timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
	context = RequestContext(request,{"CurrentUser":currentUser,"Name":username,"mapCheckins": timeFilteredCheckinsBefore})
    	return HttpResponse(template.render(context))



    elif (request.GET['endDate'] == "" and request.GET['startDate'] != ""):
	#Checking for input conditions where end date is blank
	startDate = (datetime.datetime(int(message2[0]),int(message2[1]),int(message2[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
	startDate = int(startDate)
	if 'userid' in request.GET:
		for i,key in enumerate(friends_checkins_timestamp['recent']):	
			if friends_checkins_timestamp['recent'][i]['user']['id']  == userid:                         		      timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']	
			else:
				pass	
	else:
		for i,key in enumerate(client.users.checkins(params={'afterTimestamp':startDate})['checkins']['items']):
        		timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
	context = RequestContext(request, {"CurrentUser":currentUser,"Name":username,"mapCheckins": timeFilteredCheckinsBefore})
        return HttpResponse(template.render(context))



    
    elif (request.GET['endDate'] == "" and request.GET['startDate'] == ""):
	#Checking for input conditions where both the dates are blank
	if 'username' not in request.GET:
		useranme = "Kuber Kaul"
	if 'userid' in request.GET:
		for i,key in enumerate(friends_checkins['recent']):
                        if friends_checkins['recent'][i]['user']['id']  == userid:
                                timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
	else:
		for i,key in enumerate(client.users.checkins()['checkins']['items']):
                        timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
 	context = RequestContext( request, {"CurrentUser":currentUser,"mapCheckins": timeFilteredCheckinsBefore})
    	return HttpResponse(template.render(context))
    


    else:
	# Processing inputs as parameters
	startDate = (datetime.datetime(int(message2[0]),int(message2[1]),int(message2[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
        startDate = int(startDate)
        if 'userid' in request.GET:
                for i,key in enumerate(friends_checkins_timestamp['recent']):
                        if client.checkins.recent(params={'afterTimestamp':startDate})['recent'][i]['user']['id']  == userid:
                                timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
		context = RequestContext(request, {"CurrentUser":currentUser,"Name":username,"mapCheckins": timeFilteredCheckinsBefore})
        	return HttpResponse(template.render(context))
	else:
    		startDate = (datetime.datetime(int(message2[0]),int(message2[1]),int(message2[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    		finalDate = (datetime.datetime(int(message3[0]),int(message3[1]),int(message3[2]),0,0) - datetime.datetime(1970,1,1)).total_seconds()
    		startDate = int(startDate)
    		finalDate = int(finalDate)

    		for i,key in enumerate(client.users.checkins(params={'beforeTimestamp':finalDate})['checkins']['items']):
			timeFilteredCheckinsBefore[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
        		venueNamesBefore.append(key['venue']['name'])

		
                for i,key in enumerate(client.users.checkins(params={'afterTimestamp':startDate})['checkins']['items']):
                        timeFilteredCheckinsAfter[key['venue']['name']] = key['venue']['location']['lat'] , key['venue']['location']['lng']
                        venueNamesAfter.append(key['venue']['name'])

    #Collecting common chekins
    for before in venueNamesBefore:
	for after in venueNamesAfter:
            if(before == after):
                commonSet.append(before)
    intersectionNames = set(commonSet)
    for something in intersectionNames:
        if something in timeFilteredCheckinsBefore.keys():
		putToMap[something] = timeFilteredCheckinsBefore[something]
	else:
		putToMap[something] = timeFilteredCheckinsBefore[something]
    context = RequestContext(request, {"CurrentUser":currentUser,"Name":username,"mapCheckins": putToMap})
    return HttpResponse(template.render(context))

# Logging in to the application
def login(request):
    if request.session['accessToken']:
        del request.session['accessToken']
    template = loader.get_template('login.html')
    context = RequestContext()
    return HttpResponse(template.render(context))

# Logging out of application
def logoutuser(request):
    try:
        del request.session['accessToken']
    except KeyError:
        pass
    return redirect("https://foursquare.com/oauth2/authorize?client_id=AWIKUN01EPJQ3BOCDC4HJPJ1LE52JAW03DJ0M5PWT5SO1ZCR&response_type=code&redirect_uri=http://localhost:8000/foursquare_app/mapView")

def loginError(request):
    template = loader.get_template('login.html')
    context = RequestContext(request,{"errorMessage": "The username or password you entered is incorrect"})
    return HttpResponse(template.render(context))


