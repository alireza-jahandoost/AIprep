# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import path, include, reverse  # add this
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    # path('customers/', include("customers.urls")),  # Django customers route
    path('correction/', include('correction.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path("", include("app.urls")),  # UI Kits Html files
    path("", include("authentication.urls")),  # Auth routes - login / register
    path("", RedirectView.as_view(url="login", permanent=True), name="home"),
]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
