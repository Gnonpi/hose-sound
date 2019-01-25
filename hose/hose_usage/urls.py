from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'h'
urlpatterns = [
    ## User objects
    path('home/', login_required(views.HomeView.as_view()), name='home'),
    path('demands/', login_required(views.see_hose_demands), name='see_demands'),
    path('hoses/', login_required(views.LinkedHosesView.as_view()), name='see_hoses'),
    path('signup/', views.SignUp.as_view(), name='signup'),

    ## Browse objects
    path('browse-hosers/', login_required(views.browser_hosers), name='browse_hosers'),
    # path('browse-content/', views., name='browse_content'),

    ## Show object detail
    path('hose/<int:hose_id>/', login_required(views.show_hose), name='show_hose'),
    path('hoser/<int:hoser_id>/', login_required(views.show_hoser), name='show_hoser'),

    ## Hose creation
    path('hoser/<int:hoser_id>/ask', login_required(views.ask_for_hose_creation), name='hoser_ask'),
    path('hoser/<int:demand_id>/confirm', login_required(views.confirm_hose_creation), name='hoser_confirm'),
    path('hoser/<int:hoser_id>/cancel', login_required(views.cancel_hose_creation), name='hoser_cancel'),
    # path('hose/<int:hose-pk>/<int:content-pk>', views., name='show_content'),
    path('hose/<int:hose_id>/upload', login_required(views.upload_song), name='upload_song'),

    ## REST url
    path('rest/hosers', views.HoseUserList.as_view(), name='rest_hose_users_list'),
    path('rest/hoser/<int:pk>', views.HoseUserDetail.as_view(), name='rest_hose_user_detail'),
    path('rest/hose/<int:pk>', views.HoseAssociationDetail.as_view(), name='rest_hose_detail'),
    path('rest/songs', views.HoseContentList.as_view(), name='rest_songs_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)