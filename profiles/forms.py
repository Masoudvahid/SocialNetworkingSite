from django import forms

from login.models import User


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email",
                  "phone",
                  "bio",
                  "first_name",
                  "last_name",
                  ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            user = User.objects.exclude(username=self.instance.username).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def save(self, commit=True):
        profile = super(AccountUpdateForm, self).save(commit=False)
        profile.email = self.cleaned_data["email"].lower()
        profile.phone = self.cleaned_data["phone"]
        profile.bio = self.cleaned_data["bio"]
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]
        if commit:
            profile.save()
        return profile
