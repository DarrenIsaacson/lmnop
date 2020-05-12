from django.shortcuts import render

<<<<<<< HEAD


def homepage(request):
	#check for logout session variable to display message
	try:
		just_logged_out = request.session.get('just_logged_out', False)
	except:
		ust_logged_out = False
=======
def homepage(request):
	#check for logout session variable to display message
	try:
		just_logged_out = request.session.get('logout_message', False)
	except:
		just_logged_out = False

>>>>>>> 6fe25741f364a256478dd03a891a2000cdba654a

	return render(request, 'lmn/home.html')

