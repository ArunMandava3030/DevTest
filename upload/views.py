from django.shortcuts import render

# Create your views here.
import pandas as pd
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from django.conf import settings

def handle_uploaded_file(file):
    data = pd.read_excel(file)
    summary = data.describe().to_string()
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            summary = handle_uploaded_file(uploaded_file.file.path)

            # Send email
            send_mail(
                subject=f'Python Assignment - {request.user.get_full_name()}',
                message=summary,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['recipient@example.com'],  # Replace with the desired email IDs
            )

            return render(request, 'upload/success.html')
    else:
        form = FileUploadForm()

    return render(request, 'upload/upload.html', {'form': form})
