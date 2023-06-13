from django import forms
from django.contrib.auth.models import User


class LoginFrom(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


    # Метод clean_<fieladname>() можно предоставлять любому полю
    # формы, чтобы очищать значение или вызывать ошибку валидации формы
    # для конкретного поля.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match')
        return cd['password2']
