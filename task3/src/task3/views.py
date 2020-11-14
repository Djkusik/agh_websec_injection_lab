from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings


def index(request):
    if 'why' in request.GET and request.GET['why'] == 'why You love AGH':
        user = auth.authenticate(username='young_Padawan', password='None')
        if user:
            request.user = user
            auth.login(request, user)
        else:
            return HttpResponse('Login with young_Padawan:None at /admin')
        return redirect('/admin')

    output = '''
<!DOCTYPE html>
<html>
<head>
    <title>-={ AGH web sec | Guons the Lazy }=-</title>
    <style>
    body {
        background-image: url("/static/images/stars.jpg");
        margin: 0 auto;
    }
    #content {
        width: 500px;
        margin: 0 auto;
        color: white;
        margin-top: 15%;
    }
    h2 {
        margin-bottom: 5px;
    }
    </style>
</head>
<body>
    <div id="content">
    <h2>Say why You love AGH and enter</h2> ~Guons the Lazy
    <form method="GET">
    <input type="text" name="why" />
    <input type="submit" value="Say" />
    </form>
    </div>
</body>
</html>'''
    return HttpResponse(output)