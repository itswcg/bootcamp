import cloudinary.uploader

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bootcamp2.feeds.models import Feed
from bootcamp2.feeds.views import FEEDS_NUM_PATES
from bootcamp2.messenger.models import Message

from .forms import PorfileForm, ChangePasswordForm, SavePictureForm

cloudinary.config(
    cloud_name = "itswcg",
    api_key = '734238578483371',
    api_secret = 'ikxZuYWZxDB4D1eVAlmOT8-VW_I',
)

def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PATES)
    feeds = paginator.page(1)

    from_feed = -1

    if feeds:
        from_feed = feeds[0].id

    context = {
        'page_user': page_user, 'feeds': feeds,
        'from_feed': from_feed, 'page': 1
    }
    return render(request, 'core/profile.html', context)


@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = PorfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.save()

            message = _('Your profile were successfully edited.')
            messages.add_message(request, messages.SUCCESS, message)

    else:
        initial = {
            'job_title': user.profile.job_title,
            'url': user.profile.url,
            'location': user.profile.location
        }
        form = PorfileForm(instance=user, initial=initial)

    return render(request, 'core/settings.html', {'form': form})


@login_required
def password(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()

            message = _('Your password were successfully changed.')
            messages.add_message(request, messages.SUCCESS, message)

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form})


@login_required
def picture(request):
    uploaded_picture = False
    picture_url = None

    username = request.user.username

    if request.GET.get('upload_picture') == 'uploaded':
        uploaded_picture = True
        result = cloudinary.uploader.explicit(username, type='upload')
        picture_url = result['secure_url']

    context = {
        'uploaded_picture': uploaded_picture,
        'picture_url': picture_url,
    }
    return render(request, 'core/picture.html', context)


@login_required
def upload_picture(request):
    username = request.user.username

    cloudinary.uploader.upload(
        request.FILES['picture'], public_id=username, width=400, crop='limit')

    return redirect('/settings/picture/?upload_picture=uploaded')


@login_required
def save_uploaded_picture(request):
    form = SavePictureForm(request.POST)
    user = request.user

    if form.is_valid():
        form.cleaned_data.update(crop='crop')
        result = cloudinary.uploader.explicit(
            user.username, type='upload', eager=form.cleaned_data)

        user.profile.picture_url = result['eager'][0]['secure_url']
        user.save()

        return redirect('/settings/picture/')

