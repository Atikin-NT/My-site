from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from .models import Profile, Article, TagsList
from markdownx.fields import MarkdownxFormField


class MyImageWidget(ClearableFileInput):
    template_name = "clearable_file_input.html"  # clearable_file_input


class NewArticle(forms.ModelForm):
    article_title = forms.CharField(required=True, label='Заголовок', max_length=200)
    article_content_md = MarkdownxFormField(required=True)  # myfield
    article_picture = forms.ImageField(required=False, widget=MyImageWidget)
    article_small_text = forms.CharField(required=True, widget=forms.Textarea, label='Краткое описание')
    tagArticle = forms.SelectMultiple()

    class Meta:
        model = Article
        fields = ('article_title', 'article_picture', 'article_small_text', 'tagArticle', 'article_content_md')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    where_you_leave = forms.CharField(widget=forms.TextInput, required=False, initial='Эльдия')
    description = forms.CharField(widget=forms.Textarea, required=False, initial='Клевый чел:)')
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'date_of_birth', 'description', 'where_you_leave')
        widgets = {
            'avatar': forms.FileInput(attrs={'onchange': 'previewFile()'}),
            'date_of_birth': DateInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'avatar')