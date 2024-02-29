# from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
#
# User = get_user_model()
#
# class AgentModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'password'
#             'first_name',
#             'last_name',
#           'status',
#           'sex',
#           'oborduvania'
#         )


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import  UserProfile

User = get_user_model()

class AgentModelForm(forms.ModelForm):
    status = forms.ChoiceField(choices=(('admin', 'Admin'), ('analyst', 'Analyst')))
    sex = forms.CharField(max_length=20)
    oboruduvania = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'status', 'sex', 'oboruduvania', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organisor = False
        user.is_agent = True
        if commit:
            user.save()
            UserProfile.objects.create(user=user, status=self.cleaned_data['status'], sex=self.cleaned_data['sex'], oboruduvania=self.cleaned_data['oboruduvania'])
        return user
