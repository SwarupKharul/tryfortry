from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .Forms import UserAdminCreationForm, AuthenticationForm
from django.http.response import StreamingHttpResponse
from .models import MyUser
from home.camera import VideoCamera
from django.contrib.auth.decorators import login_required
from django.template import loader, Context

camera = VideoCamera()

def gen():
	global camera
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(),
					content_type='multipart/x-mixed-replace; boundary=frame')


def home(request):
    return render(request, 'home.html')

def dumbmode(request):
    return render(request, 'dumb.html')

def blindmode(request):
    return render(request, 'blind.html')

def deafmode(request):
    return render(request, 'deaf.html')

@login_required
def profile(request):
    #details = User.objects.filter(user=request.user)
    return render(request, 'profile.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserAdminCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = MyUser.objects.create_user(password=request.POST['password1'], email=request.POST['email'], mob=request.POST['mob'])
                user.save()
                login(request, user)
                return redirect('profile')


            except IntegrityError:
                return render(request, 'signup.html',
                              {'error': 'This email id has already been registered. Please try to login or use different email id'})
            except ValueError:
                return render(request, 'signup.html',
                              {'error': 'Please enter valid email'})
        else:
            # tell the user the password didn't match
            return render(request, 'signup.html', {'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'User password did not match'})
        else:
            login(request, user)
            return redirect('profile')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
