from django import forms
from condo.models import *
from django.forms import BaseModelFormSet, ModelForm, modelformset_factory
from django.core.exceptions import ValidationError

import hashlib
# -----------USER-----------------------------------
class UserForm(forms.ModelForm):
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
            raise ValidationError("ชื่อนี้มีคนใช้แล้ว")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("อีเมลนี้มีคนใช้แล้ว")
        return data
    def clean_phone(self):
        data = self.cleaned_data.get("phone")
        if not data.isdigit():
            raise ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        return data

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
            raise ValidationError("ต้องใส่ทั้งรหัสผ่านและยืนยันรหัสผ่าน")
        if password != confirm:
            raise ValidationError("รหัสผ่านไม่ตรงกัน")
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
            raise ValidationError("ต้องใส่รหัสปัจจุบัน")
        if self.user_instance.password_hash != hashlib.sha256(old.encode()).hexdigest():
            raise ValidationError("รหัสปัจจุบันไม่ถูกต้อง")
        if not password or not confirm:
            raise ValidationError("ต้องใส่ทั้งรหัสผ่านและยืนยันรหัสผ่าน")
        if password != confirm:
            raise ValidationError("รหัสผ่านไม่ตรงกัน")

        
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
            raise ValidationError("ไม่พบข้อมูล")
        password_input_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_input_hash != user.password_hash:
            raise ValidationError("ชื่อผู้ใช้หรือรหัสผ่านผิด")
        self.user = user
        return cleaned_data
    
class CondoForm(forms.ModelForm):
    deed_number = forms.CharField(
        max_length=100,
        label="หมายเลขโฉนด",
        required=True
    )
    class Meta:
        model = Condo
        fields = ['name', 'province', 'address', 'area_sqm', 'deed_picture', 'description']
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
        
class EditCondoForm(forms.ModelForm):
    class Meta:
        model = Condo
        fields = ['name', 'province', 'address', 'area_sqm', 'deed_picture', 'description']
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
    class Meta:
        model = CondoImage
        # image_name อยู่ใน view
        fields = ['image_url']

class AtLeastOneImageFormSet(BaseModelFormSet):
    def clean(self):
        super_clean = super().clean()
        if any(self.errors):
            return super_clean

        filled = 0
        for form in self.forms:
            cd = getattr(form, 'cleaned_data', None)
            if not cd:
                continue
            if cd.get('DELETE'):
                continue
            if cd.get('image_url'):
                filled += 1

        if filled < 1:
            raise ValidationError("ต้องอัปโหลดอย่างน้อย 1 รูปภาพประกอบ")
        return super_clean


CondoImageFormSet = modelformset_factory(
    CondoImage, 
    form=CondoImageForm,
    formset=AtLeastOneImageFormSet,
    fields=['image_url'],
    extra= 3, # เริ่มต้น 3
    max_num=20, # สูงสุด 20
    can_delete=True,
)

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Condo
        fields = ['status']
        widgets = {
                'status': forms.Select(attrs={
                        'class': 'block w-full rounded-md shadow-sm m-1 py-2 px-3'
                    }),
            }

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
            raise ValidationError("ชื่อนี้มีคนใช้แล้ว")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if Staff.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("อีเมลนี้มีคนใช้แล้ว")
        return data
    def clean_phone(self):
        data = self.cleaned_data.get("phone")
        if not data.isdigit():
            raise ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
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
            raise ValidationError("ต้องใส่ทั้งรหัสผ่านและยืนยันรหัสผ่าน")
        if password != confirm:
            raise ValidationError("รหัสผ่านไม่ตรงกัน")
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
            raise ValidationError("ไม่พบชื่อผู้ใช้")
        password_input_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_input_hash != staff.password_hash:
            raise ValidationError("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
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
            raise ValidationError("ต้องใส่รหัสปัจจุบัน")
        if self.staff_instance.password_hash != hashlib.sha256(old.encode()).hexdigest():
            raise ValidationError("รหัสปัจจุบันไม่ถูกต้อง")
        if not password or not confirm:
            raise ValidationError("ต้องใส่ทั้งรหัสผ่านและยืนยันรหัสผ่าน")
        if password != confirm:
            raise ValidationError("รหัสผ่านไม่ตรงกัน")

        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        # self.user = user
        return cleaned_data
    
class StaffReportForm(forms.ModelForm):
    class Meta:
        model = CondoReport
        fields = ['report']
        widgets = {
            'report': forms.Textarea(attrs={'rows': 4}),
        }