from django.shortcuts import render

def homepage(request):
	#check for logout session variable to display message
	try:
		just_logged_out = request.session.get('logout_message', False)
	except:
		just_logged_out = False


	return render(request, 'lmn/home.html')

