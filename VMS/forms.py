from django import forms

class Usersform(forms.Form):
    num1 = forms.CharField(label="Value 1")
    num2 = forms.CharField(label="Value 2")
    num3 = forms.CharField(label="Value 3")