from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm
from django.views.generic import CreateView
from .models import Profile
from .forms import EditProfileForm, EditUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.
class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'
    failed_message = "User was not added. Please try again."
    success_url = 'profile'

    def form_valid(self, form):
        super().form_valid(form)   
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user:
            login(self.request, user)           
            return redirect('profile')

    
@login_required()    
def profile(request):
    if request.method == "GET":
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        return render(request, 'registration/profile.html', {'user_form':user_form, 'profile_form': profile_form})

    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile changes have been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'The changes were not updated to your profile.')
            return redirect('profile')


@login_required()    
def delete_user(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    messages.success(request, 'Profile successfully disabled.')
    return redirect('welcome')

@login_required()    
def admin_delete_user(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        subject = f'Your account has been deactivated.'
        message = f'{user}, your account has been deactivated by admin.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [user.email,]
        send_mail( subject, message, email_from, recipient_list) 
        messages.success(request, f"{user}'s profile successfully disabled.")
        return redirect('welcome')
    else:
        messages.warning(request, f"You do not have permission to delete this account.")
        return redirect('welcome')


    
