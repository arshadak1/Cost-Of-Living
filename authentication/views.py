from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.views.decorators.cache import cache_control, never_cache



account_creation = {'created': False}
# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def login(request):
    login_context_var = {"userError": False,
                         "passwordError": False, "user_or_email": ""}
    if request.method == 'POST':

        email_or_username = request.POST['email']
        email_or_username = str(email_or_username).strip()
        password1 = request.POST['password']

        # checking whether the user exist in the database or not
        user = authenticate(username=email_or_username, password=password1)
        if user is None and User.objects.filter(email=email_or_username).exists():
            username = User.objects.get(email__exact=str(email_or_username))
            user = authenticate(username=username, password=password1)
        # user = User.objects.get(email__exact='usermail@example.com')

        if user is not None:
            # logging in the user by using an imported method
            log(request, user)
            return redirect('dashboard')

        else:
            login_context_var['user_or_email'] = str(email_or_username)
            login_context_var['passwordError'] = True
            if User.objects.filter(username=email_or_username).exists() or User.objects.filter(email=email_or_username).exists():
                return render(request, "authentication/login.html", login_context_var)
            else:
                login_context_var['userError'] = True
                return render(request, "authentication/login.html", login_context_var)

    return render(request, "authentication/login.html")


def signup(request):
    context_var = {'emailExists': False, 'password': False,
                   'username': '', 'emailStr': '', 'userExists': False}

    if request.method == 'POST':
        username = str(request.POST.get('username')).strip()
        email = str(request.POST.get('email')).strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        

        if User.objects.filter(username=username):
            context_var['userExists'] = True
            context_var['emailStr'] = str(email)
            context_var['username'] = str(username)

            return render(request, "authentication/signup.html", context_var)
        elif User.objects.filter(email=email).exists():
            context_var['emailExists'] = True
            context_var['emailStr'] = str(email)
            context_var['username'] = str(username)

            return render(request, "authentication/signup.html", context_var)
        if password != confirm_password:
            context_var['password'] = True
            context_var['email'] = True
            context_var['emailStr'] = str(email)
            context_var['username'] = str(username)
            return render(request, "authentication/signup.html", context_var)

        
        newUser = User.objects.create_user(username, email, password)
        
        newUser.is_active = False
        newUser.save()
        messages.success(
            request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # confirmation mail
        current_site = get_current_site(request)
        subject = "Confirm your email - COL"
        message = render_to_string('email_confirm.html', {
            'name': newUser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
            'token': generate_token.make_token(newUser),
        })

        email_msg = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [newUser.email],
        )

        email_msg.fail_silently = True
        email_msg.send()

        account_creation['created'] = True
        return render(request, "authentication/login.html", account_creation)

    return render(request, "authentication/signup.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        newUser = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        newUser = None

    if newUser is not None and generate_token.check_token(newUser, token):
        newUser.is_active = True
        newUser.save()
        log(request, newUser)
        account_creation['created'] = False
        return redirect('home')
    else:
        return render(request, 'activation_error.html')
