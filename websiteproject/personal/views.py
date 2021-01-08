from django.shortcuts import render

# view the home screen
def home_screen(request):
    return render(request, 'personal/home.html', {'username': request.user.username})
