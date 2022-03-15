from django import forms
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from .models import Profile, Article
from markdownx.fields import MarkdownxFormField
from django.core.exceptions import MultipleObjectsReturned
from captcha.fields import CaptchaField
from captcha.helpers import math_challenge
from django.core import validators


class MyImageWidget(ClearableFileInput):
    template_name = "clearable_file_input.html"  # clearable_file_input


class NewArticle(forms.ModelForm):
    article_title = forms.CharField(required=True, label='Заголовок', max_length=200)
    article_content_md = MarkdownxFormField(required=True)  # myfield
    article_picture = forms.ImageField(label='Картинка', validators=[validators.FileExtensionValidator(
                                       allowed_extensions=('gif', 'jpg', 'png'))],
                                       error_messages={'invalid_extension': 'этот формат не поддерживается'},
                                       required=False, widget=MyImageWidget)
    article_small_text = forms.CharField(required=True, widget=forms.Textarea, label='Краткое описание')
    tagArticle = forms.SelectMultiple()

    class Meta:
        model = Article
        fields = ('article_title', 'article_picture', 'article_small_text', 'tagArticle', 'article_content_md')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    email = forms.CharField(label='Email', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password']) < 5:
            raise forms.ValidationError('Пароль слишком короткий')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            get_email = User.objects.get(email=email)
            raise forms.ValidationError('Такая почта уже есть в нашей базе')
        except User.DoesNotExist:
            return email
        except MultipleObjectsReturned:
            raise forms.ValidationError('Такая почта уже есть в нашей базе')


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    where_you_leave = forms.CharField(widget=forms.TextInput, required=False, initial='Эльдия')
    description = forms.CharField(widget=forms.Textarea, required=False, initial='Клевый чел:)')
    avatar = forms.ImageField(label="Аватар", validators=[validators.FileExtensionValidator(
                              allowed_extensions=('gif', 'jpg', 'png'))],
                              error_messages={'invalid_extension': 'этот формат не поддерживается'},
                              required=False, widget=MyImageWidget)

    class Meta:
        model = Profile
        fields = ('avatar', 'date_of_birth', 'description', 'where_you_leave')


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
