from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Registernew_Form(UserCreationForm):
	email=forms.EmailField(max_length=50,widget=forms.TextInput(
		attrs={
			'class':"formy",'placeholder':'Email'
		}
		))
	username=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"formy",'placeholder':'Username'
		}
		))
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(
		attrs={
			'class':"formy",'placeholder':'Password'
		}
		))

	password2=forms.CharField(label="Password-confirmation",widget=forms.PasswordInput(
		attrs={
			'class':"formy",'placeholder':'Repeat Your Password'
		}
		))

	HR=forms.BooleanField(required=False,widget=forms.CheckboxInput(
		attrs={
			'class':"agree-term",'id':'agree-term','name':'agree-term'
		}
		))
	class Meta:
		model=User
		fields=("username","email","password1","password2","HR")