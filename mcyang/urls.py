from django.urls import path
from .views import *

urlpatterns = [
    # FIXME: API先資料庫在事件！
    path('api/StudentLogin/', student_login),
    path('api/CourseList/', course_list),
    path('api/CourseSignList/', course_sign_list),
    path('api/CourseSignup/', course_signup),
    path('api/TeacherLogin/', teacher_login),

    # path('api/studentLogin/', student_login),
    # path('api/showCourse/', show_course),
    # path('api/courseSigned/', course_sign),
    # path('api/listSignCourse/', show_sign_course),

    # FIXME: 後臺網頁
    # path('', views.login, name="login"),
    # path('user_login/', views.user_login, name="user_login"),

]
