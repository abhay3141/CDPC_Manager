from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateHpc(ModelForm):
    class Meta:
        model = headplacementcoordinator
        fields = '__all__'
        exclude = ['my_user']

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyUserForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude  = ['name','Spoc']

class CompanyManagerForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude  = ['name','Manager']

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CreateCoordinatorForm(ModelForm):
    class Meta:
        model = Coordinator
        field = '__all__'
        exclude = ['my_user']

class CreateManagerForm(ModelForm):
    class Meta:
        model = Manager
        field = '__all__'
        exclude = ['my_user']

