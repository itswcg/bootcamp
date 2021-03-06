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
from bootcamp2.follow.models import Follow

from .forms import PorfileForm, ChangePasswordForm, SavePictureForm

cloudinary.config(
    cloud_name = "itswcg",
    api_key = '',
    api_secret = '',
)

def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PATES)
    feeds = paginator.page(1)
    user = request.user

    from_feed = -1

    if feeds:
        from_feed = feeds[0].id

    if Follow.objects.filter(follower=user, followed=page_user).first():
        is_follow = True
    else:
        is_follow = False
    context = {
    'page_user': page_user, 'feeds': feeds,
    'from_feed': from_feed, 'page': 1,
    'is_follow': is_follow
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


@login_required
def send(request, username):
    if request.method == 'POST':
        message = request.POST.get('message')
        to_user = get_object_or_404(User, username=username)
        from_user = request.user

        if from_user != to_user:
            Message.send_message(from_user, to_user, message)

        return redirect(f'/messages/{to_user}/')

    conversations = Message.get_conversations(user=request.user)
    context = {'conversations': conversations}
    return render(request, 'messages/new.html', context)


@login_required
def follow(request, username):
    to_user = get_object_or_404(User, username=username)
    from_user = request.user

    Follow.follow(from_user, to_user)
    from_user.profile.notify_follow(to_user)
    return redirect(f'/{to_user}/')

@login_required
def unfollow(request, username):
    to_user = get_object_or_404(User, username=username)
    from_user = request.user

    Follow.unfollow(from_user, to_user)
    return redirect(f'/{to_user}/')