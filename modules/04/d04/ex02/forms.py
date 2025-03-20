from django import forms


class TextInputForm(forms.Form):
    text = forms.CharField(label="Input Text", max_length=200)
