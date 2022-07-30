import datetime
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import os
import article
from .models import Article, TagsList, Products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm, NewArticle, ProfileForm
from .models import Profile
import time


# https://oauth.vk.com/authorize?client_id=7546586&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=app_widget+messages&response_type=code&v=5.131
# https://oauth.vk.com/access_token?client_id=7546586&client_secret=ZuuzrjpFNSQH5kmhJTBV&redirect_uri=https://oauth.vk.com/blank.html&code=f9c675957c432bbe8b

def how_much_comments(article_id) -> int:
    meth = "widgets.getComments"
    widget_api_id = "7546586"
    url = f"niktech.site/{article_id}/"
    page_id = ""
    order = "date"
    fields = ""
    offset = "0"
    count = "100"
    v = "5.131"
    access_token = "6dcf6d3a734c42082b4f274406297983502ae65404ecab0f46c09eedbb024d7492d0ad3e8bc5273a89957"

    response = requests.get(
        f"https://api.vk.com/method/{meth}?widget_api_id={widget_api_id}&url={url}&page_id={page_id}&order={order}&fields={fields}&offset={offset}&count={count}&v={v}&access_token={access_token}")

    data = response.json()
    try:
        count = data['response']["count"]
    except Exception as ex:
        return 0
    for post in data['response']['posts']:
        count += post['comments']['count']
    return count


def currentDay() -> str:
    day_text = ""
    try:
        file_days = open(r"days.txt", "r", encoding="utf-8")
    except FileNotFoundError:
        day_text = "¯\_(⊙_ʖ⊙)_/¯"
        return day_text
    for line in file_days:
        time_now = time.localtime()
        month_now = int(time_now[1])
        day_now = int(time_now[2])
        mon_in_txt = int(line[0] + line[1])
        day_in_txt = int(line[2] + line[3])
        if mon_in_txt == month_now and day_in_txt == day_now:
            day_text = ""
            for i in range(4, len(line)): day_text = day_text + line[i]
    file_days.close()
    return day_text


# done
def index(request):
    #   ----------------------------------------poisk----------------------------------------------------------
    search_query = request.GET.get('search', '')
    if search_query:
        latest_articles_list = Article.objects.filter(
            Q(article_title__icontains=search_query) | Q(article_small_text__icontains=search_query))
        meta_title = "Результат поиска"
        meta_description = "NikTech"
    #   -------------------------------------------список статей-----------------------------------------------
    else:
        latest_articles_list = Article.objects.order_by('-pub_date')
        meta_title = "home"
        meta_description = "Последние статьи на сайте NikTech. Программирование и IT"

    paginator = Paginator(latest_articles_list, 10)

    if 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    user_metadata = []  # аватарка и имя каждого пользователя
    admin_user = Profile.objects.get(user_id=25)
    for a in posts:
        try:
            curr_user = Profile.objects.get(user_id=a.author_id)
        except article.models.Profile.DoesNotExist:
            curr_user = admin_user
        user_metadata.append([curr_user.avatar.url, curr_user.user.username])

    #   ----------------------------------------paginator------------------------------------------------
    previous_page = posts.number - 3  # меньшая граница слева
    nex_page = posts.number + 2  # большая граница слева

    #   --------------------------------------------------days------------------------------------------------------
    day_text = currentDay()

    allTags = [(c.tag, c.count) for c in TagsList.objects.all().order_by('-count')[:7]]
    data = zip(posts, user_metadata, [x for x in range(len(posts))])
    if len(latest_articles_list) == 0:
        data = []

    return render(request, 'article/article.html',
                  {'posts': posts, 'previous_page': previous_page, 'nex_page': nex_page,
                   'meta_title': meta_title, 'meta_description': meta_description,
                   'day_text': day_text, 'allTags': allTags, 'css_params': 0,
                   'data': data})


# done
def tagPostShow(request, curr_tag):
    articles_list = Article.objects.filter(tagArticle__contains=curr_tag).all().order_by('-pub_date')
    allTags = [c.tag for c in TagsList.objects.all()]

    day_text = currentDay()

    paginator = Paginator(articles_list, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    user_metadata = []  # аватарка и имя каждого пользователя
    admin_user = Profile.objects.get(user_id=25)
    for a in posts:
        try:
            curr_user = Profile.objects.get(user_id=a.author_id)
        except article.models.Profile.DoesNotExist:
            curr_user = admin_user
        user_metadata.append([curr_user.avatar.url, curr_user.user.username])

    data = zip(posts, user_metadata, [x for x in range(len(posts))])
    if len(articles_list) == 0:
        data = []
    return render(request, 'article/article.html', {'meta_title': curr_tag, 'allTags': allTags,
                                                    'day_text': day_text, 'css_params': 0, 'data': data})


# done
def tagShow(request):
    return render(request, 'all_tags.html', {})


@csrf_exempt
def detail(request, article_id):
    # print(request.method)
    try:
        article = Article.objects.get(id=article_id)
    except Exception as ex:
        return redirect(index)
    allTags = [c.tag for c in TagsList.objects.all()]

    day_text = currentDay()

    count_of_comments = how_much_comments(article_id)
    if count_of_comments > article.comments:
        article.comments = count_of_comments
        article.save()

    if request.method == "POST":
        html = render(request, 'article/articledetail.html', {'article': article, 'allTags': allTags,
                                                              'day_text': day_text, 'css_params': 1})
        # print(request.COOKIES)
        if request.COOKIES.get(str(article_id)):
            pass
        else:
            article.likes += 1
            article.save(update_fields=['likes'])
            html = render(request, 'article/articledetail.html', {'article': article, 'allTags': allTags,
                                                                  'day_text': day_text, 'css_params': 1})
            if article_id == 1:
                html.set_cookie(str(article_id), '9 31 8 106 7 207 15', max_age=172800)
            else:
                html.set_cookie(str(article_id), 'Toad Sage', max_age=172800)
        return html

    return render(request, 'article/articledetail.html', {'article': article, 'allTags': allTags,
                                                          'day_text': day_text, 'css_params': 1})


def product(request):
    latest_articles_list = Products.objects.order_by('-pub_date')
    meta_title = "home"
    meta_description = "Последние статьи на сайте NikTech. Программирование и IT"

    paginator = Paginator(latest_articles_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    previous_page = posts.number - 3  # меньшая граница слева
    nex_page = posts.number + 2  # большая граница слева
    day_text = currentDay()
    allTags = [c.tag for c in TagsList.objects.all()]

    return render(request, 'article/article.html',
                  {'posts': posts, 'previous_page': previous_page, 'nex_page': nex_page,
                   'meta_title': meta_title, 'meta_description': meta_description,
                   'day_text': day_text, 'allTags': allTags, 'css_params': 0})


# done
def articleById(request, user_id):
    try:
        curr_user = Profile.objects.get(user_id=user_id)
    except article.models.Profile.DoesNotExist:
        return redirect(index)

    admin_flag = 0
    if request.user.is_authenticated and (request.user.is_superuser or request.user.id == user_id):
        admin_flag = 1

    articles_list = Article.objects.filter(author_id=user_id).order_by('-pub_date')
    paginator = Paginator(articles_list, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    previous_page = posts.number - 3  # меньшая граница слева
    nex_page = posts.number + 2  # большая граница слева

    return render(request, 'article/users_articles.html', {'posts': posts, 'curr': curr_user, 'css_params': 2,
                                                           'count_of_all_posts': len(articles_list),
                                                           'previous_page': previous_page, 'nex_page': nex_page,
                                                           'admin_flag': admin_flag})


# done
def newArticle(request):
    if not request.user.is_authenticated:
        return redirect(register)

    if request.method == "POST":
        form = NewArticle(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)

            new_article.pub_date = datetime.date.today()
            new_article.author_id = request.user.id

            new_article.save(new=True)
            return redirect(articleById, user_id=request.user.id)

    else:
        form = NewArticle(initial={'article_picture': 'default.jpg'})
    return render(request, 'article/new_article.html', {'css_params': 3, 'form': form, 'new_or_old': 1,
                                                        'meta_title': 'Новая статья', 'meta_description': 'Новая статья'})


# done
def editArticle(request, article_id):
    try:
        curr_article = Article.objects.get(id=article_id)
    except article.models.Article.DoesNotExist:
        return redirect(index)

    if (not request.user.is_authenticated) or (request.user.id != curr_article.author_id and (not request.user.is_superuser)):
        return redirect('article:detail', article_id=article_id)

    if request.method == "POST":
        form = NewArticle(data=request.POST, files=request.FILES, instance=curr_article)
        if form.is_valid() and form.has_changed():
            form.save()
            return redirect(articleById, user_id=request.user.id)
    else:
        form = NewArticle(initial={'article_title': curr_article.article_title,
                                   'article_small_text': curr_article.article_small_text,
                                   'article_content_md': curr_article.article_content_md,
                                   'article_picture': curr_article.article_picture,
                                   'tagArticle': curr_article.tagArticle})
    return render(request, 'article/new_article.html',
                  {'css_params': 3, 'form': form, 'new_or_old': 0, 'article': curr_article})


def deleteArticle(request, article_id):
    article = Article.objects.filter(Q(id=article_id))[0]
    for curr_tag in article.tagArticle:
        TagsList.objects.get(tag=curr_tag).remove()
    article.delete()
    return redirect(articleById, user_id=request.user.id)


# done
def register(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            profile_data = profile_form.cleaned_data
            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            Profile.objects.create(user=new_user,
                                   avatar=profile_data['avatar'],
                                   description=profile_data['description'],
                                   where_you_leave=profile_data['where_you_leave'],
                                   date_of_birth=profile_data['date_of_birth'])
            return render(request, 'registration/register_done.html', {'new_user': new_user, 'meta_title': 'ヾ(⌐■_■)ノ♪',
                                                                       'meta_description': 'ヾ(⌐■_■)ノ♪'})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                          'profile_flag_edit': 0, 'css_params': 4,
                                                          'meta_title': 'Регистрация', 'meta_description': 'Регистрация'})


# done
def edit(request):
    current_user = request.user
    if (not request.user.is_authenticated) or (request.user.id != current_user.id and request.user.id != 25):
        return redirect('article:index')
    curr_profile = Profile.objects.filter(user_id=current_user.id)[0]
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=current_user)
        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=curr_profile)
        if user_form.is_valid() and profile_form.is_valid():
            if user_form.has_changed():
                user_form.save()
            if profile_form.has_changed():
                profile_form.save()
            return redirect(articleById, user_id=request.user.id)
    else:
        user_form = UserEditForm(initial={'username': current_user.username,
                                          'email': current_user.email})
        profile_form = ProfileForm(initial={'avatar': curr_profile.avatar,
                                            'date_of_birth': curr_profile.date_of_birth,
                                            'description': curr_profile.description,
                                            'where_you_leave': curr_profile.where_you_leave})
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                          'profile_flag_edit': 1, 'css_params': 4,
                                                          'meta_title': 'Настройки', 'meta_description': 'Настройки'})


def error404(request, exception):
    return render(request, 'errorPage.html', {"error": "404"})


def error500(request):
    return render(request, 'errorPage.html', {"error": "500"})
