from django.urls import path
from correction import views

urlpatterns = [
    path('add_correction/toefl/create_integrated', views.CreateToeflIntegratedView.as_view(), name='create_toefl_integrated'),
    path('', views.ShowCorrectionsView, name='show_corrections'),
    path('<int:correction_id>', views.ShowCorrectionView, name='show_correction'),
]