from django.urls import path, include

from accounts import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/',views.login_view,name='login'),
    path('profile/', views.profile, name='user-profile'),
    path('edit_profile/', views.profile_edit, name='edit-profile'),
    path('delete_profile/', views.profile_delete, name='delete-profile'),
    path('change_password/', views.change_password, name='password_change'),
    path('change_password/done/', views.change_password_done, name='password_change_done'),

]
