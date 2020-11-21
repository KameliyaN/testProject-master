from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, EmailValidator

from accounts.models import Profile


#
# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password1')


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        validators=[MinLengthValidator(6)])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_first_name(self):

        first_name = self.cleaned_data['first_name']
        for char in first_name:
            if not char.isalpha():
                raise ValidationError('First name may only contain letters')
            if first_name:
                if not first_name[0].isupper():
                    raise ValidationError('First name must starts with uppercase letter')
        return first_name

    def clean_last_name(self):

        last_name = self.cleaned_data['last_name']
        for char in last_name:
            if not char.isalpha():
                raise ValidationError('Last name may only contain letters')
            if last_name:
                if not last_name[0].isupper():
                    raise ValidationError('Last name must starts with uppercase letter')
        return last_name


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

    fields = ('username', 'password1')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        validators=[MinLengthValidator(6)])
    email = forms.CharField(validators=[EmailValidator()])

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

    def clean_first_name(self):

        first_name = self.cleaned_data['first_name']
        for char in first_name:
            if not char.isalpha():
                raise ValidationError('First name may only contain letters')
            if first_name:
                if not first_name[0].isupper():
                    raise ValidationError('First name must starts with uppercase letter')
        return first_name

    def clean_last_name(self):

        last_name = self.cleaned_data['last_name']

        for char in last_name:
            if not char.isalpha():
                raise ValidationError('Last name may only contain letters')
            if last_name:
                if not last_name[0].isupper():
                    raise ValidationError('Last name must starts with uppercase letter')
        return last_name


class DisabledFormMixin:
    def __init__(self):
        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True


class DeleteProfileForm(ProfileForm, DisabledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DisabledFormMixin.__init__(self)
