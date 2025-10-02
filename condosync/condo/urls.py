from django.urls import path

from . import views
from condo.views import *

urlpatterns = [
    # ex: /condo/login/  or  {% url 'user-login' %}
    path("login/", views.user_login.as_view(), name="user-login"),
    # ex: /condo/regis/  or  {% url 'user-regis' %}
    path("regis/", views.user_regis.as_view(), name="user-regis"),
    # ex: /condo/forgetpw/  or  {% url 'user-forgetpw' %}
    path("forgetpw/", views.user_forgetpw.as_view(), name="user-forgetpw"),
    # ex: /condo/home/  or  {% url 'user-login' %}
    path("home/", views.user_home.as_view(), name="user-home"),
     # ex: /condo/profile_user/1/  or  {% url 'user-profile' user_id %}
    path("profile_user/<int:user_id>/", views.user_profile.as_view(), name="user-profile"),
    # ex: /condo/update_user/1/  or  {% url 'user-update' user_id %}
    path("update_user/<int:user_id>/", views.user_update.as_view(), name="user-update"),
    

    # ------STAFF----------------
    # ex: /condo/login_staff/  or  {% url 'staff-login' %}
    path("login_staff/", views.staff_login.as_view(), name="staff-login"),
    # ex: /condo/home_staff/  or  {% url 'staff-login' %}
    path("home_staff/", views.staff_home.as_view(), name="staff-home"),
    # ex: /condo/regis_staff/  or  {% url 'staff-regis' %}
    path("regis_staff/", views.staff_regis.as_view(), name="staff-regis"),
    # ex: /condo/forgetpw_staff/  or  {% url 'staff-forgetpw' %}
    path("forgetpw_staff/", views.staff_forgetpw.as_view(), name="staff-forgetpw"),
    # ex: /condo/profile_staff/1/  or  {% url 'staff-profile' staff_id %}
    path("profile_staff/<int:staff_id>/", views.staff_profile.as_view(), name="staff-profile"),
    # ex: /condo/update_staff/1/  or  {% url 'staff-update' staff_id %}
    path("update_staff/<int:staff_id>/", views.staff_update.as_view(), name="staff-update"),


    # # ex: /registration/professor/
    # path("professor/", views.professor_list.as_view(), name="professor-list"),
    # # ex: /registration/faculty/
    # path("faculty/", views.faculty_list.as_view(), name="faculty-list"),
    # # ex: /registration/course/
    # path("course/", views.course_list.as_view(), name="course-list"),
    # # ex: /registration/create_student/
    # path("create_student/", views.create_student.as_view(), name="create-student"),
    # # ex: {% url 'update-student' student.student_id %}
    # path("update_student/<int:student_id>/", views.update_student.as_view(), name="update-student"),
    # # ex: /registration/create_course/
    # path("create_course/", views.create_course.as_view(), name="create-course"),
    # # ex: {% url 'update-course' course.course_code %}
    # path("update_course/<course_code>/", views.update_course.as_view(), name="update-course"),
]