from django.shortcuts import redirect, reverse
from django.views import generic
from django.contrib.auth import logout, login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .tasks import create_email
from . decorators import login_forbidden
from .forms import  UserForm,AuthForm
   
 
 
 
class SignUpView(generic.FormView):
 
    template_name = "registration/sign_up.html"
    form_class = UserForm
    success_url = "/account/"
 
    def form_valid(self, form):
        obj = form.save()
        login(self.request, obj)
        #this is a celery task
        create_email.delay(
            user_id = obj.id, #user ID - this must be added
            email_account = "do not reply",#the email account being used
            subject = 'Thanks for signing up',
            email = obj.username,#who to email
            cc = [],
            template = "hello.html",#template to be used
            )
        return super().form_valid(form)
   
    @method_decorator(login_forbidden)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 
 
 
 


class SignInView(generic.FormView):
    template_name = "registration/sign_in.html"
    form_class = AuthForm
    success_url = "/account/"
 
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(SignInView, self).form_valid(form)
        else:
            return self.form_invalid(form)


    @method_decorator(login_forbidden)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


 
def sign_out(request):
    logout(request)
    return redirect(reverse('sign-in'))
 
 
 
class AccountView(generic.TemplateView):
    template_name = "registration/account.html"
 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)