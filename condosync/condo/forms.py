from django import forms
from condo.models import *
from django.forms import BaseModelFormSet, ModelForm, modelformset_factory
from django.core.exceptions import ValidationError

import hashlib
# -----------USER-----------------------------------
class UserForm(forms.ModelForm):
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
    #                                     label="Confirm Password")
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
    def clean_phone(self):
        data = self.cleaned_data.get("phone")
        if not data.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password_hash")
    #     # confirm = cleaned_data.get("confirm_password")
    #     confirm = self.cleaned_data.get("confirm_password")
    #     if not password or not confirm:
    #         raise ValidationError("Both password and confirm password are required.")
    #     if password != confirm:
    #         raise ValidationError("Passwords do not match")

    #     # Hash the password before saving
    #     cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
    #     return cleaned_data

class PWForm(forms.ModelForm):
    # username = forms.CharField(label="Username or Email")
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
        password = cleaned_data.get("password_hash")
        confirm = self.cleaned_data.get("confirm_password")
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("Passwords do not match")
        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        return cleaned_data
    
class ChangePWForm(forms.ModelForm):
    password_old = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password_old'}),
                                        label="Old Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
                                        label="Confirm Password")
    class Meta:
        model = User
        fields = ['password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
        }
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old = cleaned_data.get("password_old")
        password = cleaned_data.get("password_hash")
        confirm = cleaned_data.get("confirm_password")
        if not old:
            raise ValidationError("Current password is required.")
        if self.user_instance.password_hash != hashlib.sha256(old.encode()).hexdigest():
            raise ValidationError("Current password is incorrect.")
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("New passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        # self.user = user
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
    
class CondoForm(forms.ModelForm):
    deed_number = forms.CharField(
        max_length=100, # กำหนด max_length ให้สอดคล้องกับ Model
        label="หมายเลขโฉนด",
        required=True # บังคับกรอก
    )
    class Meta:
        model = Condo
        fields = ['name', 'province', 'address', 'area_sqm', 'deed_picture', 'description']
        # ตัวอย่าง widgets
        widgets = {
            'province': forms.Select(),
            'area_sqm': forms.NumberInput(attrs={'min': '0'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'deed_picture': forms.FileInput(attrs={"class": "hidden"}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].empty_label = "--กรุณาเลือกจังหวัด--"


    def clean_area_sqm(self):
        data = self.cleaned_data.get("area_sqm")
        if data <= 0:
            raise ValidationError("พื้นที่ต้องมากกว่า 0 ตารางเมตร")
        return data
    def clean_deed_picture(self):
        data = self.cleaned_data.get("deed_picture")
        if not data:
            raise ValidationError("ต้องอัปโหลดรูปภาพสำเนาโฉนด")
        return data

class CondoListingForm(forms.ModelForm):
    class Meta:
        model = CondoListing
        fields = ['asking_price', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_asking_price(self):
        data = self.cleaned_data.get("asking_price")
        if data <= 0:
            raise ValidationError("ราคาที่ขอต้องมากกว่า 0 บาท")
        return data

class CondoImageForm(forms.ModelForm):
    # เราใช้ image_url ที่เป็น FileField ใน Model
    class Meta:
        model = CondoImage
        # image_name จะถูกกำหนดใน views.py จากชื่อไฟล์ที่อัปโหลด
        fields = ['image_url']

class AtLeastOneImageFormSet(BaseModelFormSet):
    def clean(self):
        super_clean = super().clean()
        # ถ้ามี error ของ form ย่อย ให้ปล่อยให้แสดง (จะไม่ซ้ำ)
        if any(self.errors):
            return super_clean

        filled = 0
        for form in self.forms:
            # form.cleaned_data อาจไม่มีถ้า form มี error ก่อนหน้านี้
            cd = getattr(form, 'cleaned_data', None)
            if not cd:
                continue
            # ข้ามฟอร์มที่ผู้ใช้ติ๊กลบ (ถ้าใช้ can_delete)
            if cd.get('DELETE'):
                continue
            # ถ้ามีไฟล์ใน image_url ให้ถือว่า filled
            if cd.get('image_url'):
                filled += 1

        if filled < 1:
            raise ValidationError("ต้องอัปโหลดอย่างน้อย 1 รูปภาพประกอบ")
        return super_clean

# Formset สำหรับจัดการหลายรูปภาพ
CondoImageFormSet = modelformset_factory(
    CondoImage, 
    form=CondoImageForm,
    formset=AtLeastOneImageFormSet,
    fields=['image_url'],
    extra= 3, # เริ่มต้นด้วยฟอร์มเปล่า 3 ฟอร์ม
    max_num=20, # อนุญาตสูงสุด 20 ไฟล์
)

# -----------Staff----------------------------
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'role']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
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
    def clean_phone(self):
        data = self.cleaned_data.get("phone")
        if not data.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return data

class StaffPWForm(forms.ModelForm):
    # username = forms.CharField(label="Username or Email")
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
    
class StaffChangePWForm(forms.ModelForm):
    password_old = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password_old'}),
                                        label="Old Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}),
                                        label="Confirm Password")
    class Meta:
        model = Staff
        fields = ['password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'id': 'password_hash'}),
        }
    def __init__(self, *args, **kwargs):
        self.staff_instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old = cleaned_data.get("password_old")
        password = cleaned_data.get("password_hash")
        confirm = cleaned_data.get("confirm_password")
        if not old:
            raise ValidationError("Current password is required.")
        if self.staff_instance.password_hash != hashlib.sha256(old.encode()).hexdigest():
            raise ValidationError("Current password is incorrect.")
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("New passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        # self.user = user
        return cleaned_data
