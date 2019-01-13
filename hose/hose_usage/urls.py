from django.urls import path

from . import views

app_name = 'h'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/list', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/songs', views.ResultsView.as_view(), name='results'),
    path('<int:hose_id>/listen', views.listen_content, name='listen'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
