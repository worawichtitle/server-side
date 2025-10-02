from django import forms
from condo.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError

import hashlib
# -----------USER-----------------------------------
class UserForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
                                        label="Confirm Password")
    class Meta:
        model = User
        fields = ['username', 'password_hash', 'first_name', 'last_name',
                  'email', 'phone', 'main_contact', 'address']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError("This username is already in use")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use")
        return data
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        # confirm = cleaned_data.get("confirm_password")
        confirm = self.cleaned_data.get("confirm_password")
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("Passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password_hash = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password_hash'}),
        label="Password"
    )
    def clean(self):
        cleaned_data = super().clean()
        userinput = cleaned_data.get("username")
        password = cleaned_data.get("password_hash")
        user = User.objects.filter(username=userinput).first()
        if not user:
            user = User.objects.filter(email=userinput).first()
        if not user:
            raise ValidationError("User not found.")
        password_input_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_input_hash != user.password_hash:
            raise ValidationError("Incorrect username or password.")
        self.user = user
        return cleaned_data

class ForgetPWForm(ModelForm):
    username = forms.CharField(label="Username or Email")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
                                        label="Confirm Password")
    class Meta:
        model = User
        fields = ['password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        userinput = cleaned_data.get("username")
        password = cleaned_data.get("password_hash")
        confirm = self.cleaned_data.get("confirm_password")
        user = User.objects.filter(username=userinput).first()
        if not user:
            user = User.objects.filter(email=userinput).first()
        if not user:
            raise ValidationError("User not found.")
        
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("Passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        self.user = user
        return cleaned_data
    
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'main_contact', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already in use")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use")
        return data

# -----------Staff----------------------------
class StaffForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
                                        label="Confirm Password")
    class Meta:
        model = Staff
        fields = ['username', 'password_hash', 'first_name', 'last_name',
                  'email', 'phone', 'role']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
            'role': forms.Select(),
        }
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError("This username is already in use")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use")
        return data
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm = self.cleaned_data.get("confirm_password")
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("Passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        return cleaned_data
    
class StaffLoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password_hash = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password_hash'}),
        label="Password"
    )
    def clean(self):
        cleaned_data = super().clean()
        staffinput = cleaned_data.get("username")
        password = cleaned_data.get("password_hash")
        staff = Staff.objects.filter(username=staffinput).first()
        if not staff:
            staff = Staff.objects.filter(email=staffinput).first()
        if not staff:
            raise ValidationError("User not found.")
        password_input_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_input_hash != staff.password_hash:
            raise ValidationError("Incorrect username or password.")
        self.staff = staff
        return cleaned_data
    
class StaffForgetPWForm(ModelForm):
    username = forms.CharField(label="Username or Email")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
                                        label="Confirm Password")
    class Meta:
        model = Staff
        fields = ['password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        userinput = cleaned_data.get("username")
        password = cleaned_data.get("password_hash")
        confirm = self.cleaned_data.get("confirm_password")
        user = Staff.objects.filter(username=userinput).first()
        if not user:
            user = Staff.objects.filter(email=userinput).first()
        if not user:
            raise ValidationError("User not found.")
        
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("Passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        self.user = user
        return cleaned_data
    
class StaffUpdateForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'role']
        widgets = {
            'role': forms.Select(),
        }
    def clean_username(self):
        data = self.cleaned_data["username"]
        if Staff.objects.filter(username=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already in use")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if Staff.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use")
        return data