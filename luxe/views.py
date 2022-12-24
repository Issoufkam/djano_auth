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
from .models import Product
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    product_objects = Product.objects.all() # recuperation de tous les produits dans la base de donnée
    product_id = request.GET.get('product_id')
    if product_id != '' and product_id is not None:
        product_objects = Product.objects.filter(title__icontains=product_id)
    paginator = Paginator(product_objects, 20)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    return render(request, 'home.html', {'product_objects': product_objects})


def registerF(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username):
            messages.error(request, 'user allexist')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, 'Email exist')
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
        mon_utilisateur = User.objects.create_user(username=username, email=email, last_name=last_name, first_name=first_name, password=password)
        mon_utilisateur.save()

        # Message de bienvenu aux utilisateurs
        messages.success(request, 'Votre compte a été créer avec succès')
        subject = 'Mail de verification Alpha GT'
        message = 'Bonjour bievenue à votre compte'
        from_emil = settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject, message, from_emil, to_list, fail_silently=False)

        # Message de confirmation de la creation de compte
        #current_site = get_current_site # recuperation du lien du site
        #objet = 'Confirmation de creation de compte' # l'Objet de messagerie
        #contenu = render_to_string("email.html", {
         #   'name': mon_utilisateur.first_name,
          #  'dommaine': current_site,
           # 'uid': urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            
       # })
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

def detail(request, myid):
    product_objects = Product.objects.get(id=myid)
    category = product_objects.category # affichage des articles similaire et qui appartiennent la meme categorie
    similar_pro = Product.objects.filter(category=category)
    return render(request, 'product/detail.html', {'produit': product_objects, 'similar_pro': similar_pro})

def panier(request):
    return render(request, 'product/panier.html')

#sms function
#def sms(request):
 #   message = request.GET['body']
 #   message_splited = message.split("-")
  #  title = message_splited[0]
   # desc = message_splited[1]

#    agri_category = Category.objects.get(id=2)
 #   product = Product(title=title,category=agri_category)
  #  return render