from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password' ]
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        # user = super(RegistrationForm, self).save(commit=False)
        user = User.objects.create_user(self.cleaned_data["email"], self.cleaned_data["password"])

        # user.username = User.objects.get_username(self.cleaned_data["email"])
        # user.set_password(self.cleaned_data["password"])
        # print user.email, user.username, user.password

        if commit:
            user.save()
        return user
