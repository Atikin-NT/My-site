import datetime

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Article, TagsList
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm, NewArticle
from .models import Profile
import time


def index(request):
    param = request.resolver_match.url_name
    #   ----------------------------------------poisk----------------------------------------------------------
    search_query = request.GET.get('search', '')
    if search_query:
        latest_articles_list = Article.objects.filter(
            Q(article_title__icontains=search_query) | Q(article_small_text__icontains=search_query))
        titleurl = "Результат поиска"
        meta_title = "Результат поиска"
        meta_description = "NikTech"
    #   -------------------------------------------список статей-----------------------------------------------
    else:
        latest_articles_list = Article.objects.order_by('-pub_date')
        titleurl = "home"
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
    #   ----------------------------------------paginator------------------------------------------------
    flag1 = posts.number - 5  # меньшая граница слева
    flag2 = posts.number + 6  # большая граница слева
    flag3 = paginator.count - 5  # граница справа
    flagmin = paginator.count - 10  # граница справа
    arr_advert = []
    cout_of_advertisin = 0
    for a in posts:
        cout_of_advertisin = cout_of_advertisin + 1
        if cout_of_advertisin == 3:
            cout_of_advertisin = 0
            arr_advert.append(a.id)
    randomarticle = Article.objects.order_by('?')[:2]
    try:
        adver1 = arr_advert[0]
    except IndexError:
        adver1 = -1
    try:
        adver2 = arr_advert[1]
    except IndexError:
        adver2 = -1
    try:
        adver3 = arr_advert[2]
    except IndexError:
        adver3 = -1
    #   --------------------------------------------------days------------------------------------------------------
    day_text = currentDay()

    allTags = [c.tag for c in TagsList.objects.all()]

    return render(request, 'article/article.html',
                  {'posts': posts, 'flag1': flag1, 'flag2': flag2, 'flag3': flag3, 'flagmin': flagmin,
                   'adver1': adver1, 'adver2': adver2, 'adver3': adver3,
                   'randomarticle': randomarticle, 'titleurl': titleurl,
                   'meta_title': meta_title, 'meta_description': meta_description,
                   'day_text': day_text, 'allTags': allTags})


def tagPostShow(request, curr_tag):
    articles_list = Article.objects.filter(tagArticle__contains=curr_tag).all().order_by('-pub_date')
    allTags = [c.tag for c in TagsList.objects.all()]

    day_text = currentDay()

    paginator = Paginator(articles_list, 10)  # 10 posts in each page
    posts = paginator.page(paginator.num_pages)

    return render(request, 'article/article.html', {'posts': posts, 'meta_title': curr_tag, 'allTags': allTags,
                                                    'day_text': day_text})


def tagShow(request):
    return render(request, 'all_tags.html', {})


@csrf_exempt
def detail(request, article_id):
    print(request.method)
    article = Article.objects.get(id=article_id)
    allTags = [c.tag for c in TagsList.objects.all()]

    day_text = currentDay()

    if request.method == "POST":
        html = render(request, 'article/articledetail.html', {'article': article, 'allTags': allTags})
        print(request.COOKIES)
        if request.COOKIES.get(str(article_id)):
            pass
        else:
            if article_id == 16:
                html.set_cookie(str(article_id), '9 31 8 106 7 207 15', max_age=86400)
            else:
                html.set_cookie(str(article_id), 'Toad Sage', max_age=86400)
            article.likes += 1
            article.save()
        return html

    return render(request, 'article/articledetail.html', {'article': article, 'allTags': allTags,
                                                          'day_text': day_text, 'css_params': 1})


def articleById(request, user_id):
    articles_list = Article.objects.filter(Q(author_id=user_id)).all().order_by('-pub_date')
    paginator = Paginator(articles_list, 10)  # 10 posts in each page
    posts = paginator.page(paginator.num_pages)
    allTags = [c.tag for c in TagsList.objects.all()]

    curr_user = Profile.objects.filter(Q(user_id=user_id))

    return render(request, 'article/users_articles.html', {'posts': posts, 'curr': curr_user,
                                                           'allTags': allTags, 'css_params': 2})


def newArticle(request):
    current_user = request.user
    print("new line -------------")
    print(f"user = {current_user}")
    if request.method == "POST":
        form = NewArticle(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Article.objects.create(article_title=data['article_title'],
                                   article_small_text=data['article_small_text'],
                                   article_content_md=data['article_content_md'],
                                   pub_date=datetime.date.today(),
                                   author_id=request.user.id,
                                   article_picture=data['article_picture'],
                                   tagArticle=data['tagArticle'])
        return redirect(articleById, user_id=request.user.id)
    else:
        form = NewArticle()
    return render(request, 'article/new_article.html', {'css_params': 3, 'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def edit(request):
    current_user = request.user
    user_email = Profile.objects.filter(user_id=current_user.id)
    try:
        if user_email[0] is True:
            pass
    except IndexError:
        name1 = current_user.first_name
        name2 = current_user.last_name
        if name1 == "" or name2 == "":
            profile = Profile.objects.create(user=current_user)
        else:
            current_user.username = name1 + " " + name2
            current_user.save()
            profile = Profile.objects.create(user=current_user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})


def error404(request, exception):
    return render(request, 'error404.html')


def error500(request):
    return render(request, 'error500.html')


def currentDay() -> str:
    file_flag = 0
    day_text = ""
    try:
        file_days = open(r"days.txt", "r", encoding="utf-8")
        file_flag = 1
    except FileNotFoundError:
        day_text = "¯\_(⊙_ʖ⊙)_/¯"
    if file_flag == 1:
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
