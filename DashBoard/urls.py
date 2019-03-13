# noinspection SpellCheckingInspection
"""BackyardSale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('', views.dashboard.as_view(), name='dashboard'),
    path('create/', views.createItem.as_view(), name='create'),
    path('ajax/load-subCats/', views.getSubCategories, name='ajax_load_subCats'),
    path('delete/<slug:slug>/<int:pk>', views.deleteItems.as_view(), name='deleteItems'),
    path('update/<slug:slug>/<int:pk>', views.updateItems.as_view(), name='updateItems'),
    path('approve/', views.approveView.as_view(), name='approve'),
]
