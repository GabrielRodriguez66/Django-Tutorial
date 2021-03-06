from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.home, name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/edit/', views.edit, name='edit'),
    path('add_question/', views.add_question, name='add_question'),
    path('<int:question_id>/delete/', views.delete_question, name='delete'),
    path('export/', views.ExportPDFView.as_view(), name='export')
]
