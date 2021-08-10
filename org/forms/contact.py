from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(label="Email*", widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control'}))


