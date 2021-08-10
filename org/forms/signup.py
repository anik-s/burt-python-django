from django import forms


class SignupForm(forms.Form):
    email = forms.EmailField(label='Email*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8,
                               label="Password*",
                               strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
                               )
    confirm_password = forms.CharField(min_length=8,
                                       label="Confirm Password*",
                                       strip=False,
                                       widget=forms.PasswordInput(
                                           attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
                                       )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("position")
        confirm_password = cleaned_data.get("title")
        if password != confirm_password:
            self.add_error('password', 'Passwords don\'t match')
