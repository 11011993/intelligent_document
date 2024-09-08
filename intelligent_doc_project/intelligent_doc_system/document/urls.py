from django.urls import path
from .views import upload_doc, UploadSuccess
from document import views

urlpatterns = [
    path('upload/', upload_doc, name='upload_pdf'),
    path('success/', UploadSuccess.as_view(), name='success'),
    path('pdf_doc/', views.GetDocument.as_view()),
]
