from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.views import LoginView, LogoutView

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in immediately if you want:
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')  # update to your home url name
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

class AppLoginView(LoginView):
    template_name = 'blog/login.html'

class AppLogoutView(LogoutView):
    template_name = 'blog/logged_out.html'  # optional

@login_required
def profile_view(request):
    return render(request, 'blog/profile.html')

@login_required
def profile_edit_view(request):
    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        pform = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile_edit.html', {'pform': pform})
