from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django.forms.models import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class AccountForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name","email", "bio","image", "intro","github_link", "twitter_link","website_link"]
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude =['owner']
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject','body']
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})