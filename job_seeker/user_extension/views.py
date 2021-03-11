from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User

#for verification
from django.urls import reverse
from django.core.mail import EmailMessage
from .utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
import threading

#Models
from .forms import Registernew_Form
from .models import UserType

class EmailThread(threading.Thread):    #threading

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=False)


# Create your views here.
def landing_page(request):
    
    return render(request,"landing.html",{})


def login_view(request): #For HR
    error=""
    user=request.user
    print("hello")
    if user.is_authenticated:
        return redirect("landing")
    if request.POST:
        email=request.POST.get('email')
        print(email)
        try:
            username=User.objects.get(email=email)
            print(username)
            password=request.POST.get('pass')
            print(password)
            user=authenticate(username=username,password=password)
            print("true")
            if user:
                login(request,user)
                print("True")
                return redirect("landing")
            else:
                error="Invalid Credentials"
        except:
            error="Email Does Not exist"

    context={'error':error}
    return render(request,'login.html',context)

def new_registration(request): #For HR
    context={}
    if request.POST:
        utype=request.POST.get('HR')
        print(utype)
        if utype=="on":
            utype=True
        print("###################################")
        form=Registernew_Form(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            usertype=UserType.objects.get(user=user)
            usertype.selected=True
            if utype==True:
                usertype.HR=True
            usertype.save()
                

                
            #domain,relative url,token,uid
            user=user
            domain=get_current_site(request).domain
            uidb64=urlsafe_base64_encode(force_bytes(user.id))
            token= account_activation_token.make_token(user)
            link=reverse('user_extension:activate',kwargs={'uidb64':uidb64,'token':token})
            activate_url="https://"+domain+link

            subject="Email verification"
            message="Hi "+str(user.username)+"\n"+str(activate_url)+"\nIgnore(if not used arsenalG)"
            to_list=[user.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
            )
            EmailThread(email).start()
            #send_mail(subject,message,"gauravshinde696969@gmail",to_list,fail_silently=True)
            return redirect('user_extension:wait')
        else:
            context={'registeration_form':form}
    else:

        form=Registernew_Form()
        context["registeration_form"]=form
    return render(request,'Register.html',context)


def Wait(request):
    return render(request,"waiting.html",{})

def verification(request,uidb64,token):

    id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=id)
    if not account_activation_token.check_token(user, token):
        return redirect('landing')
    if user.is_active:
        return redirect('landing')
    user.is_active = True
    user.save()
    return redirect('landing')
		