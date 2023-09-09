from django.urls import path,include
from home import views
urlpatterns = [
    path('', views.index,name='index' ),
    path('contact', views.contact,name='contact' ),
    path('about', views.about,name='about' ),
    path('search', views.search,name='search' ),
    path('signup', views.handleSignup,name='handleSignup' ),
    path('login', views.handleLogin,name='handleLogin' ),
    path('logout', views.handleLogout,name='handleLogout' ),
]
