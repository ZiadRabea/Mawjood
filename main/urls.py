from django.urls import path
from.views import *
urlpatterns = [
    path('', show_grades),
    path('manage/', create_grades),
    path('<int:id>/delete', delete_grade),
    path('<int:id>/classrooms', show_classrooms),
    path('<int:id>/classrooms/<int:cid>/delete', delete_classroom),
    path('<int:id>/classrooms/manage', create_classrooms),
    path('<int:id>/classrooms/<int:cid>/students', students),
]