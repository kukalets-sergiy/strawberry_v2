from django import forms
from django.contrib.auth.models import User
from strawberry_app.models import PlantImage
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirmation = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirmation = cleaned_data.get("confirmation")

        if password and confirmation and password != confirmation:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        return user


class PlantImageForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = PlantImage
        fields = ("image", "video", "delete")
