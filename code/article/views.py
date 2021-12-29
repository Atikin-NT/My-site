import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Article, TagsList, Products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm, NewArticle, ProfileForm
from .models import Profile
import time


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
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    user_metadata = []  # аватарка и имя каждого пользователя
    for a in posts:
        curr_user = Profile.objects.filter(Q(user_id=a.author_id))[0]
        user_metadata.append([curr_user.avatar.url, curr_user.user.username])

    #   ----------------------------------------paginator------------------------------------------------
    previous_page = posts.number - 3  # меньшая граница слева
    nex_page = posts.number + 2  # большая граница слева
    arr_advert = []
    cout_of_advertisin = 0
    for a in posts:
        cout_of_advertisin = cout_of_advertisin + 1
        if cout_of_advertisin == 3:
            cout_of_advertisin = 0
            arr_advert.append(a.id)
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
    data = zip(posts, user_metadata)
    if len(latest_articles_list) == 0: data = []

    return render(request, 'article/article.html',
                  {'posts': posts, 'previous_page': previous_page, 'nex_page': nex_page,
                   'adver1': adver1, 'adver2': adver2, 'adver3': adver3,
                   'meta_title': meta_title, 'meta_description': meta_description,
                   'day_text': day_text, 'allTags': allTags, 'css_params': 0,
                   'data': data})


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
    for a in posts:
        curr_user = Profile.objects.filter(Q(user_id=a.author_id))[0]
        user_metadata.append([curr_user.avatar.url, curr_user.user.username])

    data = zip(posts, user_metadata)
    if len(articles_list) == 0: data = []
    return render(request, 'article/article.html', {'meta_title': curr_tag, 'allTags': allTags,
                                                    'day_text': day_text, 'css_params': 0, 'data': data})


def tagShow(request):
    return render(request, 'all_tags.html', {})


@csrf_exempt
def detail(request, article_id):
    # print(request.method)
    article = Article.objects.get(id=article_id)
    allTags = [c.tag for c in TagsList.objects.all()]

    day_text = currentDay()

    if request.method == "POST":
        html = render(request, 'article/articledetail.html', {'article': article, 'allTags': allTags,
                                                              'day_text': day_text, 'css_params': 1})
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


def articleById(request, user_id):
    articles_list = Article.objects.filter(Q(author_id=user_id)).all().order_by('-pub_date')
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

    curr_user = Profile.objects.filter(Q(user_id=user_id))[0]

    return render(request, 'article/users_articles.html', {'posts': posts, 'curr': curr_user, 'css_params': 2,
                                                           'count_of_all_posts': len(articles_list),
                                                           'previous_page': previous_page, 'nex_page': nex_page})


def newArticle(request):
    if request.method == "POST":
        form = NewArticle(data=request.POST, files=request.FILES)
        article = Article.objects.create()
        article.article_title = form['article_title'].value()
        article.article_small_text = form['article_small_text'].value()
        article.article_content_md = form['myfield'].value()
        article.pub_date = datetime.date.today()
        article.author_id = request.user.id
        if form['article_picture'].value(): article.article_picture = form['article_picture'].value()
        article.tagArticle = form['tagArticle'].value()
        article.save()
        # Article.objects.create(article_title=data['article_title'],
        #                            article_small_text=data['article_small_text'],
        #                            article_content_md=data['myfield'],
        #                            pub_date=datetime.date.today(),
        #                            author_id=request.user.id,
        #                            article_picture=data['article_picture'],
        #                            tagArticle=data['tagArticle'])
        return redirect(articleById, user_id=request.user.id)
    else:
        form = NewArticle()
    return render(request, 'article/new_article.html', {'css_params': 3, 'form': form, 'new_or_old': 1})


def editArticle(request, article_id):
    article = Article.objects.filter(Q(id=article_id))[0]
    if request.method == "POST":
        form = NewArticle(data=request.POST, files=request.FILES)

        article.article_title = form['article_title'].value()
        article.article_small_text = form['article_small_text'].value()
        article.article_content_md = form['myfield'].value()
        if form['article_picture'].value(): article.article_picture = form['article_picture'].value()
        article.tagArticle = form['tagArticle'].value()
        article.save()
        return redirect(articleById, user_id=request.user.id)
    else:
        form = NewArticle(initial={'article_title': article.article_title,
                                   'article_small_text': article.article_small_text,
                                   'myfield': article.article_content_md,
                                   'article_picture': article.article_picture,
                                   'tagArticle': article.tagArticle})
    return render(request, 'article/new_article.html',
                  {'css_params': 3, 'form': form, 'new_or_old': 0, 'article': article})


def deleteArticle(request, article_id):
    article = Article.objects.filter(Q(id=article_id))[0]
    article.delete()
    return redirect(articleById, user_id=request.user.id)


def register(request):
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Create a new user object but avoid saving it yet
            profile_data = profile_form.cleaned_data
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user,
                                   avatar=profile_data['avatar'],
                                   description=profile_data['description'],
                                   where_you_leave=profile_data['where_you_leave'],
                                   date_of_birth=profile_data['date_of_birth'])
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                          'profile_flag_edit': 0})


def edit(request):
    current_user = request.user
    curr_profile = Profile.objects.filter(user_id=current_user.id)[0]
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)

        current_user.username = user_form['username'].value()
        current_user.email = user_form['email'].value()
        current_user.save()

        if profile_form['avatar'].value(): curr_profile.avatar = profile_form['avatar'].value()
        if profile_form['date_of_birth'].value(): curr_profile.date_of_birth = profile_form['date_of_birth'].value()
        if profile_form['description'].value(): curr_profile.description = profile_form['description'].value()
        curr_profile.where_you_leave = profile_form['where_you_leave'].value()
        curr_profile.save()

        return redirect(articleById, user_id=request.user.id)
    else:
        user_form = UserRegistrationForm(initial={'username': current_user.username,
                                                  'email': current_user.email})
        profile_form = ProfileForm(initial={'avatar': curr_profile.avatar,
                                            'date_of_birth': curr_profile.date_of_birth,
                                            'description': curr_profile.description,
                                            'where_you_leave': curr_profile.where_you_leave})
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                              'profile_flag_edit': 1, 'css_params': 4})


def error404(request, exception):
    return render(request, 'error404.html')


def error500(request):
    return render(request, 'error500.html')
