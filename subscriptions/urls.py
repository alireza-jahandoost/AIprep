from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.show_plans, name='subscription_plans'),
    path('order/<int:plan_id>', views.order, name='subscription_order'),
    path('verify/<int:plan_id>', views.verify, name='verify'),
]