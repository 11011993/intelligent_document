from django.shortcuts import render, redirect
from .forms import DocumentForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import *
from django.http import FileResponse
from rest_framework import status
from pdf2image import convert_from_path
import pytesseract
import tempfile
import requests
import spacy

def upload_doc(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentForm()
    return render(request, 'upload_doc.html', {'form': form})

def upload_success(request):
    return render(request, 'success.html')

class GetDocument(APIView):
    def get(self,request):
        user_id = request.query_params.get('user_id')
        pdf_doc = UploadDocument.objects.filter(user_id = user_id).first()
        if not pdf_doc or not pdf_doc.pdf:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

        pdf_url = request.build_absolute_uri(pdf_doc.pdf.url)
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return Response({"error": "Failed to download PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf_path = temp_pdf.name

        try:
            images = convert_from_path(temp_pdf_path)
            extracted_text = ""
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                extracted_text += text
                print(f"Page {i+1} Text:\n{text}\n")

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(extracted_text)

            # Extract entities using spaCy
            entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
            print(f"Extracted Entities: {entities}")

            # You can also add other AI processing here (Text Classification, Sentiment Analysis, etc.)
            return Response({"pdf_url": pdf_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to process PDF: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # response = FileResponse(pdf_doc.pdf, content_type='application/pdf')
        # response['Content-Disposition'] = f'inline; filename="{pdf_doc.pdf.name}"'
        # return response