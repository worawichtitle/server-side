from django.urls import path

from . import views
from condo.views import *

urlpatterns = [
    # ex: /condo/login/  or  {% url 'user-login' %}
    path("login/", views.user_login.as_view(), name="user-login"),
    # ex: /condo/regis/  or  {% url 'user-regis' %}
    path("regis/", views.user_regis.as_view(), name="user-regis"),
    # ex: /condo/home/  or  {% url 'user-login' %}
    path("home/", views.user_home.as_view(), name="user-home"),
    

    # ------STAFF----------------
    # ex: /condo/login/  or  {% url 'user-login' %}
    path("login_staff/", views.staff_login.as_view(), name="staff-login"),
    # ex: /condo/home/  or  {% url 'user-login' %}
    path("home_staff/", views.staff_home.as_view(), name="staff-home"),
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