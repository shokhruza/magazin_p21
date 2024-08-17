from django.urls import path

from apps.views import ProductListView, RegisterView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list.html'),
    path('register', RegisterView.as_view(), name='register.html'),
    path('login', RegisterView.as_view(), name='login.html')
]
