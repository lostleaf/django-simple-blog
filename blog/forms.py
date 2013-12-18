from django import forms

class BlogForm(forms.Form):
    """docstring for BlogForm"""
    caption = forms.CharField(label='title', max_length=100)
    content = forms.CharField(widget=forms.Textarea)

class TagForm(forms.Form):
  """docstring for TagForm"""
  tag_name = forms.CharField()

class LoginForm(forms.Form):
  username=forms.CharField(label="username",max_length=30,
    widget=forms.TextInput(attrs={'size': 20,}))
  password=forms.CharField(label="password",max_length=30,
    widget=forms.PasswordInput(attrs={'size': 20,}))