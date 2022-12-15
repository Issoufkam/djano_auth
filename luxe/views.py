from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from imobilier import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request, 'home.html')


def registerF(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username):
            messages.error(request, 'user allexist')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, 'Email allexit')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'username is invalable')
            return redirect('register')
        if password != password1:
            messages.error(request, 'Les mots de passes ne correspondent pas')
            return redirect('register')
       # if not password.isalnum():
       #     messages.error(request, 'le mot de passe doit etre Alphanumerique')
       #     return redirect('register')
        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.save()

        # Message de bienvenu aux utilisateurs
        messages.success(request, 'Votre compte a été créer avec succès')
        subject = 'Mail de verification Alpha GT'
        message = 'Bonjour bievenue à votre compte'
        from_emil = settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject, message, from_emil, to_list, fail_silently=False)

        # Message de confirmation de la creation de compte
        current_site = get_current_site # recuperation du lien du site
        objet = 'Confirmation de creation de compte' # l'Objet de messagerie
        contenu = render_to_string("email.html", {
            'name': mon_utilisateur.first_name,
            'dommaine': current_site,
            'uid': urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            
        })
        return redirect('login')
        
    return render(request, 'connexion/register.html')

def loginF(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'home.html', {'firstname':firstname})
        else:
            messages.error(request, 'Username ou Mot de passe incorrect')
            return redirect('login')
    return render(request, 'connexion/login.html')

def logOut(request):
    logout(request)
    return redirect('home')