from django.shortcuts import render

def home_screen(request):
    return render(request, 'personal/home.html', {'username': request.user.username})
