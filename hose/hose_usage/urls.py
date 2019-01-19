from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'h'
urlpatterns = [
    path('home/', login_required(views.HomeView.as_view()), name='home'),
    path('hoses/', login_required(views.LinkedHosesView.as_view()), name='see_hoses'),
    path('browse-hosers/', login_required(views.browser_hosers), name='browse_hosers'),
    # path('browse-content/', views., name='browse_content'),
    path('hoser/<int:hoser_id>/', login_required(views.show_hoser), name='show_hoser'),
    # path('demands/', views., name='see_demands'),
    path('hoser/<int:hoser_id>/ask', login_required(views.ask_for_hose_creation), name='hoser_ask'),
    # path('hoser/<int:hoser-pk>/confirm', views., name='hoser_confirm'),
    path('hose/<int:hose_id>/', login_required(views.show_hose), name='show_hose'),
    # path('hose/<int:hose-pk>/<int:content-pk>', views., name='show_content'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
