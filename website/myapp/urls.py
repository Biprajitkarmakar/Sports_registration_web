from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/students/', views.student_list, name='student_list'),
    path('admin/student/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('admin/student/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('', views.register, name='registerpage'),
    path('get-sports/', views.get_sports_by_group, name='get_sports_by_group'),
    path('confirm/', views.confirm, name='confirmpage'),
    path('thankyou/', views.submit, name='thankyoupage'),
    path('download-pdf/<str:student_id>/', views.download_pdf, name='download_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
