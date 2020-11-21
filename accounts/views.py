from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import render, redirect

from accounts.forms import SignUpForm, ProfileForm, UserForm, DeleteProfileForm, LoginForm


def get_redirect_url(params):
    redirect_url = params.get('return_url')
    print(redirect_url)
    return redirect_url if redirect_url else 'home'


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        return_url = get_redirect_url(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(return_url)

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('home')
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile = request.user.profile

    context = {'profile': profile}

    return render(request, 'accounts/user_profile.html', context)


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            return redirect('user-profile')

    context = {'form': form,
               }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def profile_delete(request):
    user = request.user
    profile = user.profile
    form = DeleteProfileForm(instance=profile)

    if request.method == 'POST':
        profile.delete()
        user.delete()
        return redirect('home')
    context = {'form': form,
               }
    return render(request, 'accounts/delete_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('password_change_done')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form})


@login_required
def change_password_done(request):
    return render(request, 'accounts/change_password_done.html', {})
