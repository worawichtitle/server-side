from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
# from django.contrib.auth import authenticate, login

from condo.forms import *
from condo.models import *
from django.db.models import Q
from django.db import transaction

# Create your views here.
# -----------USER--------------------------------
class user_login(View):
    def get(self, request, **thisiserror):
        form = LoginForm()
        context = {
            'form': form
        }
        context.update(thisiserror)
        return render(request, 'user/login_user.html', context)
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session.flush()
            user = form.user
            request.session.set_expiry(21600)  # 6 hours in seconds
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return redirect("user-home")
        else:
            print("Form error:", form.errors)
            return render(request, 'user/login_user.html', {'form': form})

class user_home(View):
    def get(self, request):
        if not request.session.get("user_id"):
            return redirect("user-login")
        try:
            user_id = request.session.get("user_id")
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return redirect("user-login")
        context = {
            'user_id': user_id,
            'user': user
        }
        return render(request, 'user/home_user.html', context)

class user_regis(View):
    def get(self, request, **thisiserror):
        form = UserForm()
        pwform = PWForm()
        context = {
            'form': form,
            'pwform': pwform,
        }
        context.update(thisiserror)
        return render(request, 'user/regis_user.html', context)
    def post(self, request):
        form = UserForm(request.POST)
        pwform = PWForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid() and pwform.is_valid():
                    print('form pass')
                    form_instance = form.save(commit=False)
                    print('PWform pass', pwform.cleaned_data["password_hash"])
                    form_instance.password_hash = pwform.cleaned_data["password_hash"]
                    form_instance.save()
                    return redirect('user-login')
                else:
                    print('Transaction ERROR')
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("other error:", e)
                context = {
                    'form': form,
                    'pwform': pwform,
                }
                return render(request, 'user/regis_user.html', context)

class user_changepw(View):
    def get(self, request, user_id, **thisiserror):
        if not request.session.get("user_id"):
            return redirect("user-login")
        if request.session.get("user_id") != user_id:
            return redirect("user-home")
        user = User.objects.get(pk=user_id)
        form = ChangePWForm(instance=user)
        context = {
            'form': form,
            'user_id': user_id,
            'user': user,
        }
        context.update(thisiserror)
        return render(request, 'user/changepw_user.html', context)
    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = ChangePWForm(request.POST, instance=user)
        try:
            with transaction.atomic():
                if form.is_valid():
                    user.password_hash = form.cleaned_data["password_hash"]
                    user.save()
                    # print("form User:", user.id, user.username)
                    return redirect('user-profile', user_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                    'user_id': user_id,
                    'user': user
                }
                return render(request, 'user/changepw_user.html', context)
        
class user_profile(View):
    def get(self, request, user_id):
        if request.session.get("staff_id"):
            pass
        elif request.session.get("user_id") != user_id:
            if  not request.session.get("user_id"):
                return redirect("user-login")
            return redirect("user-home")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            if request.session.get("staff_id"):
                return redirect("staff-home")
            return redirect("user-login")
        context = {
            'user_id': user_id,
            'user': user
        }
        return render(request, 'user/profile_user.html', context)
    
class user_update(View):
    def get(self, request, user_id, **thisiserror):
        if not request.session.get("user_id"):
            return redirect("user-login")
        if request.session.get("user_id") != user_id:
            return redirect("user-home")
        user = User.objects.get(pk=user_id)
        print(user.id)
        form = UserForm(instance=user)
        context = {
            'form': form,
            'user_id': user_id,
            'user': user,
        }
        context.update(thisiserror)
        return render(request, 'user/update_user.html', context)
    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = UserForm(request.POST, instance=user)
        try:
            with transaction.atomic():
                if form.is_valid():
                    user = form.save()
                    return redirect('user-profile', user_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'user_id': user_id,
                    'user': user,
                }
                return render(request, 'user/update_user.html', context)
        
class condo_create(View):
    # กำหนด Formset ภายใน View เพื่อให้ง่ายต่อการเรียกใช้ (ถ้าไม่ได้กำหนดใน forms.py)
    # แต่เนื่องจากเรากำหนดแล้วใน forms.py ให้ใช้ที่ import มา

    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("user-login")
        user = User.objects.get(pk=user_id)
        condo_form = CondoForm()
        listing_form = CondoListingForm()
        image_formset = CondoImageFormSet(queryset=CondoImage.objects.none()) 
        
        context = {
            'condo_form': condo_form,
            'listing_form': listing_form,
            'image_formset': image_formset,
            'user_id': user_id,
            'user': user,
        }
        return render(request, 'user/create_condo.html', context)

    def post(self, request):
        user_id = request.session.get("user_id")
        user = User.objects.get(pk=user_id)
        condo_form = CondoForm(request.POST, request.FILES)
        listing_form = CondoListingForm(request.POST)
        image_formset = CondoImageFormSet(request.POST, request.FILES, queryset=CondoImage.objects.none())
        
        
        # ตรวจสอบความถูกต้องของทุกฟอร์ม
        if condo_form.is_valid() and listing_form.is_valid() and image_formset.is_valid():
            try:
                with transaction.atomic():
                    deed_num = condo_form.cleaned_data['deed_number']
                    if Condo.objects.filter(deed_number=deed_num).exists():
                        condo = Condo.objects.get(deed_number=deed_num)
                        new_listing = listing_form.save(commit=False)
                        new_listing.condo = condo
                        new_listing.user = user # กำหนด Foreign Key ไปที่ผู้ใช้ที่ล็อกอินอยู่
                        new_listing.save()
                        return redirect('condo-list')
                    print('Condo form valid')
                    # 1. บันทึก Condo หลัก
                    new_condo = condo_form.save()
                    new_condo.deed_number = deed_num
                    new_condo.save()
                    print('New condo created:', new_condo.id, new_condo.name)
                    # 2. บันทึก CondoListing (ต้องเชื่อมโยงกับ user และ condo)
                    print('Listing form valid')
                    new_listing = listing_form.save(commit=False)
                    new_listing.condo = new_condo
                    new_listing.user = user # กำหนด Foreign Key ไปที่ผู้ใช้ที่ล็อกอินอยู่
                    new_listing.save()
                    print('New listing created:', new_listing.id, new_listing.condo.name, new_listing.user.username)
                    # 3. บันทึก CondoImage Formset
                    print('Image formset valid')
                    for form in image_formset:
                        # ตรวจสอบว่ามีการอัปโหลดไฟล์ในช่องนั้นๆ จริงหรือไม่
                        if form.cleaned_data and form.cleaned_data.get('image_url'):
                            condo_image = form.save(commit=False)
                            condo_image.condo = new_condo  # เชื่อมโยงกับ Condo ที่สร้างใหม่
                            
                            # กำหนด image_name จากชื่อไฟล์ที่อัปโหลด
                            uploaded_file = form.cleaned_data.get('image_url')
                            condo_image.image_name = uploaded_file.name 
                            
                            condo_image.save()
                    return redirect('condo-list')

            except Exception as e:
                # จัดการข้อผิดพลาด
                print(f"Error during save: {e}")
                # อาจจะเพิ่มข้อความ error ให้ผู้ใช้เห็น
                context = {
                    'condo_form': condo_form,
                    'listing_form': listing_form,
                    'image_formset': image_formset,
                    'user_id': user_id,
                    'user': user,
                }
                return render(request, 'user/create_condo.html', context)
        else:
            print("Form errors:")
            print("Condo form errors:", condo_form.errors)
            print("Listing form errors:", listing_form.errors)
            print("Image formset errors:", image_formset.errors)
            print("Image formset non-field errors:", image_formset.non_form_errors())
            # หากมีข้อผิดพลาดในการตรวจสอบความถูกต้อง
            context = {
                'condo_form': condo_form,
                'listing_form': listing_form,
                'image_formset': image_formset,
                'user_id': user_id,
                'user': user,
            }
            return render(request, 'user/create_condo.html', context)
        
class condo_update(View):
    def get(self, request, deed_number):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("user-login")
        user = User.objects.get(pk=user_id)
        condo = Condo.objects.get(deed_number=deed_number)
        listing = CondoListing.objects.filter(condo=condo, user=user).select_related('user').first()
        if not listing:
            return redirect("condo-list")
        
        condo_form = EditCondoForm(instance=condo)
        
        context = {
            'condo_form': condo_form,
            'condo': condo,
            'user': user,
        }
        return render(request, 'user/update_condo.html', context)

    def post(self, request, deed_number):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("user-login")
        user = User.objects.get(pk=user_id)
        condo = Condo.objects.get(deed_number=deed_number)

        condo_form = EditCondoForm(request.POST, request.FILES, instance=condo)
        if condo.deed_picture:
            condo_form.fields['deed_picture'].required = False

        
        print("before")
        if condo_form.is_valid():
            try:
                with transaction.atomic():
                    print("form valid")
                    updated_condo = condo_form.save(commit=False)
                    updated_condo.update_at = timezone.now()
                    updated_condo.save()


                return redirect('condo-detail', condo.deed_number)
            
            except Exception as e:
                print(f"Error during update: {e}")
                context = {
                    'condo_form': condo_form,
                    'condo': condo,
                    'user': user
                }
                return render(request, 'user/update_condo.html', context)
        print("form invalid")
        context = {
            'condo_form': condo_form,
            'condo': condo,
            'user': user
        }
        return render(request, 'user/update_condo.html', context)

class condo_list(View):
    def get(self, request):
        if not request.session.get("user_id") and not request.session.get("staff_id"):
            return redirect("user-login")
        search = request.GET.get("search", "")
        s_filter = request.GET.get("filter", "")
        list_all = CondoListing.objects.all().select_related('condo', 'condo__province').prefetch_related('condo__images').order_by('-condo__update_at')
        if not request.session.get("staff_id"):
            user = User.objects.get(pk=request.session.get("user_id"))
            list_all = list_all.filter(user=user)
        else:
            user = Staff.objects.get(pk=request.session.get("staff_id"))
        if search:
            if s_filter == "name":
                condo_list = list_all.filter(condo__name__icontains=search)
            elif s_filter == "status":
                condo_list = list_all.filter(
                Q(condo__status__icontains=search) | 
                Q(condo__status__in=[value for value, label in Condo.CondoStatus.choices if search in label])
            )
            elif s_filter == "user" and request.session.get("staff_id"):
                condo_list = list_all.filter(
                Q(user__username__icontains=search) | 
                Q(user__first_name__icontains=search) | 
                Q(user__last_name__icontains=search)
            )
            else:
                condo_list = list_all.filter(condo__deed_number__icontains=search)
        else:
            condo_list = list_all
        total = condo_list.count()
        return render(request, 'condo_list.html', context={
            "user": user,
            "condo_list": condo_list,
            "total": total,
            "search": search,
            "filter": s_filter
        })
    
class condo_detail(View):
    def get(self, request, deed_number):
        if not request.session.get("user_id"):
            return redirect("user-login")
        else:
            if not CondoListing.objects.filter(condo__deed_number=deed_number, user__id=request.session.get("user_id")).exists():
                return redirect("condo-list")
            user = User.objects.get(pk=request.session.get("user_id"))

        listing = CondoListing.objects.filter(condo__deed_number=deed_number, user=user).select_related(
            'condo', 'condo__province', 'user').prefetch_related('condo__images').first()
        
        condo = listing.condo # อ้างอิงถึง Condo ที่เชื่อมโยงกับ Listing นั้น

        context = {
            'listing': listing,
            'condo': condo,
            'user': user,
        }
        return render(request, 'user/detail_condo.html', context)
    
class condolist_edit(View):
    def get(self, request, list_id):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("user-login")
        listing = CondoListing.objects.get(pk=list_id)
        if listing.user.id != user_id:
            return redirect("user-home")
        form = CondoListingForm(instance=listing)
        context = {
            'form': form,
            'listing': listing,
            'condo_name': listing.condo.name,
            'user': listing.user
        }
        return render(request, 'user/update_list.html', context)

    def post(self, request, list_id):
        listing = CondoListing.objects.get(pk=list_id)
        form = CondoListingForm(request.POST, instance=listing)
        print("get form")

        if form.is_valid():
            print("form valid")
            listing.listed_at = timezone.now()
            form.save()
            return redirect("condo-detail", deed_number=listing.condo.deed_number)
        context = {
            'form': form,
            'listing': listing,
            'condo_name': listing.condo.name,
        }
        return render(request, 'listing_update.html', context)
    
class status_edit(View):
    def get(self, request, deed_number, **thisiserror):
        if request.session.get("staff_id") or CondoListing.objects.filter(condo__deed_number=deed_number, user__id=request.session.get("user_id")).exists():
            condo = Condo.objects.get(deed_number=deed_number)
            if request.path.endswith('/cancel/'):
                try:
                    with transaction.atomic():
                        condo.status = 'CAL'
                        condo.save()
                    return redirect('condo-detail', deed_number)
                except Exception as e:
                    print("Cancel error:", e)
                    return redirect('user-home')

            print(deed_number)
            form = StatusUpdateForm(instance=condo)
            context = {
                'form': form,
                'deed_number': deed_number,
                'condo': condo,
            }
            context.update(thisiserror)
            return render(request, 'status_update.html', context)
        else:
            return redirect('user-home')
    def post(self, request, deed_number):
        condo = Condo.objects.get(deed_number=deed_number)
        form = StatusUpdateForm(request.POST, instance=condo)
        try:
            with transaction.atomic():
                if form.is_valid():
                    condo.status = form.cleaned_data['status']
                    condo.save()
                    return redirect('condo-list')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'deed_number': deed_number,
                    'condo': condo,
                }
                return render(request, 'status_update.html', context)

class logout(View):
    def get(self, request):
        # Clear session keys
        staff = False
        if request.session.get('staff_id'):
            staff = True
        request.session.flush()  # Clears all session data
        if staff:
            return redirect('staff-login') 
        return redirect('user-login') 

# -----------STAFF------------------------------------------------
class staff_login(View):
    def get(self, request, **thisiserror):
        form = StaffLoginForm()
        context = {
            'form': form
        }
        context.update(thisiserror)
        return render(request, 'staff/login_staff.html', context)
    def post(self, request):
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            request.session.flush()
            staff = form.staff
            request.session.set_expiry(21600)  # 6 hours in seconds
            request.session["staff_id"] = staff.id
            request.session["username"] = staff.username
            return redirect("staff-home")
        else:
            print("Form error:", form.errors)
            return render(request, 'staff/login_staff.html', {'form': form})

class staff_home(View):
    def get(self, request):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        try:
            staff_id = request.session.get("staff_id")
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return redirect("staff-login")
        context = {
            'staff_id': staff_id,
            'staff': staff
        }
        return render(request, 'staff/home_staff.html', context)
    
class staff_regis(View):
    def get(self, request, **thisiserror):
        form = StaffForm()
        pwform = StaffPWForm()
        context = {
            'form': form,
            'pwform': pwform,
        }
        context.update(thisiserror)
        return render(request, 'staff/regis_staff.html', context)
    def post(self, request):
        form = StaffForm(request.POST)
        pwform = StaffPWForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid() and pwform.is_valid():
                    form_instance = form.save(commit=False)
                    print('PWform pass', pwform.cleaned_data["password_hash"])
                    form_instance.password_hash = pwform.cleaned_data["password_hash"]
                    form_instance.save()
                    return redirect('staff-login')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'pwform': pwform,
                }
                return render(request, 'staff/regis_staff.html', context)
        
class staff_changepw(View):
    def get(self, request, staff_id, **thisiserror):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        staff = Staff.objects.get(pk=staff_id)
        form = StaffChangePWForm(instance=staff)
        context = {
            'form': form,
            'staff_id': staff_id,
            'staff': staff,
        }
        context.update(thisiserror)
        return render(request, 'staff/changepw_staff.html', context)
    def post(self, request, staff_id):
        staff = Staff.objects.get(pk=staff_id)
        form = StaffChangePWForm(request.POST, instance=staff)
        try:
            with transaction.atomic():
                if form.is_valid():
                    staff.password_hash = form.cleaned_data["password_hash"]
                    staff.save()
                    # print("form User:", staff.id, staff.staffname)
                    return redirect('staff-profile', staff_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                    'staff_id': staff_id,
                    'staff': staff
                }
                return render(request, 'staff/changepw_staff.html', context)
        
class staff_profile(View):
    def get(self, request, staff_id):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return redirect("staff-login")
        context = {
            'staff_id': staff_id,
            'staff': staff
        }
        return render(request, 'staff/profile_staff.html', context)

class staff_update(View):
    def get(self, request, staff_id, **thisiserror):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        staff = Staff.objects.get(pk=staff_id)
        print(staff.id)
        form = StaffForm(instance=staff)
        context = {
            'form': form,
            'staff_id': staff_id,
            'staff': staff,
        }
        context.update(thisiserror)
        return render(request, 'staff/update_staff.html', context)
    def post(self, request, staff_id):
        staff = Staff.objects.get(pk=staff_id)
        form = StaffForm(request.POST, instance=staff)
        try:
            with transaction.atomic():
                if form.is_valid():
                    staff = form.save()
                    return redirect('staff-profile', staff_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'staff_id': staff_id,
                    'staff': staff,
                }
                return render(request, 'staff/update_staff.html', context)

