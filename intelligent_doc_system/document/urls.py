from django.urls import path
from .views import upload_doc, upload_success
from document import views

urlpatterns = [
    path('upload/', upload_doc, name='upload_pdf'),
    path('success/', upload_success, name='success'),
    path('pdf_doc/', views.GetDocument.as_view()),
]
