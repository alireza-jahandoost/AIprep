from django.urls import path
from correction import views

urlpatterns = [
    path('add_correction/toefl/create_integrated', views.CreateToeflIntegratedView.as_view(), name='create_toefl_integrated'),
    path('add_correction/toefl/create_independent', views.CreateToeflIndependentView.as_view(), name='create_toefl_independent'),
    path('', views.ShowCorrectionsView, name='show_corrections'),
    path('<int:correction_id>', views.ShowCorrectionView, name='show_correction'),
]