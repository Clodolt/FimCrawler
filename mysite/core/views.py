from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import  messages
from .models import Journal
from mysite.core.forms import RegistrationForm, UserUpdateForm, JournalSelectionForm


def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

def journal_list(request):
    queryset = Journal.objects.all()

    context = {
        "object_list": queryset
    }

    return render(request, "list.html", context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance =request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }
    return render(request, 'registration/profile.html', context)

@login_required
def journals(request):
    if request.method == 'POST':
        form = JournalSelectionForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Journals have been updated!')
            return redirect('home')
    else:
        j_form = JournalSelectionForm(request.POST, instance=request.user.profile)
    context = {
        'j_form': j_form
    }
    return render(request, 'registration/journals.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crawls(request):
    if request.method == 'POST':
        import os
        os.system('cd crawler/postscrape/postscrape && scrapy crawl combined')


        # return user to required page
    return render(request, 'crawls.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def mails(request):
    if request.method == 'POST':
        import mysqlCmd, sendMail, FIM_newsletter, crawler_dictionaries
        FIM_newsletter.mail()


        # return user to required page
    return render(request, 'mails.html')