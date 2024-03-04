# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
#
# from leads.models import UserProfile
#
# User = get_user_model()
#
# class AgentModelForm(UserCreationForm):
#     STATUS_CHOICES = [
#         ('admin', 'Admin'),
#         ('analyst', 'Analyst'),
#         ('master', 'Master'),
#         ('slave', 'Slave'),
#     ]
#     status = forms.ChoiceField(choices=STATUS_CHOICES)
#     sex = forms.CharField(max_length=20)
#     oboruduvania = forms.CharField(max_length=20)
#     uchastok = forms.CharField(max_length=20)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'status', 'sex', 'oboruduvania', 'uchastok', 'password1', 'password2')
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.save()
#         # Assuming you have a UserProfile model to handle the additional fields
#         # This part of the code should create a UserProfile instance for the user
#         # with the extra fields like 'status', 'sex', 'oboruduvania', and 'uchastok'.
#         # Make sure you have these fields defined in your UserProfile model.
#         user_profile = UserProfile(user=user, status=self.cleaned_data['status'],
#                                    sex=self.cleaned_data['sex'],
#                                    oboruduvania=self.cleaned_data['oboruduvania'],
#                                    uchastok=self.cleaned_data['uchastok'])
#         user_profile.save()
#         return user
