from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User

from bootcamp2.feeds.models import Feed
from bootcamp2.articles.models import Article
from bootcamp2.questions.models import Question


# icontains 不区分大小写 Q 复合查询
def search(request):
    if 'q' not in request.GET:
        return render(request, 'search/search.html', {'hide_search': True})

    querystring = request.GET.get('q').strip()
    search_type = request.GET.get('type')

    if len(querystring) == 0:
        return redirect('/search')

    if search_type not in ['feed', 'articles', 'questions', 'users']:
        search_type = 'feed'

    results = {
        'feed': Feed.objects.filter(post__icontains=querystring),
        'articles': Article.objects.filter(
            Q(title__icontains=querystring) |
            Q(content__icontains=querystring)),
        'questions': Question.objects.filter(
            Q(title__icontains=querystring) |
            Q(description__icontains=querystring)),
        'users': User.objects.filter(
            Q(username__icontains=querystring) |
            Q(first_name__icontains=querystring) |
            Q(last_name__icontains=querystring))
    }
    count = {
        'feed': results['feed'].count(),
        'users': results['users'].count(),
        'articles': results['articles'].count(),
        'questions': results['questions'].count()
    }
    context = {
        'hide_search': True,
        'querystring': querystring,
        'active': search_type,
        'count': count,
        'results': results[search_type]
    }
    return render(request, 'search/results.html', context)
