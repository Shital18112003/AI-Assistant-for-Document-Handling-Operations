from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
import os
from pdf2docx import Converter
from django.shortcuts import render

# Conversion view in the documents app
def conversion_view(request):
    return render(request, 'conversion/documento.html')

def pdf_to_word(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        pdf_file = request.FILES.get('file')
        print("pdf_file:", pdf_file)

        if not pdf_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        # Define the path for the output directory
        output_dir = os.path.join(settings.MEDIA_ROOT, 'converted')  # Use MEDIA_ROOT
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

        try:
            # Save the uploaded PDF temporarily in the default storage (typically /media)
            file_path = default_storage.save(f'temp/{pdf_file.name}', pdf_file)
            file_path = default_storage.path(file_path)  # Full path to the file

            output_file_name = f"{os.path.splitext(pdf_file.name)[0]}.docx"
            output_file_path = os.path.join(output_dir, output_file_name)  # Full path for the output file

            print("Processing file:", file_path)
            print("Output will be saved to:", output_file_path)

            # Convert PDF to Word using pdf2docx
            converter = Converter(file_path)
            converter.convert(output_file_path, start=0, end=None)  # Convert entire PDF
            converter.close()

            print("Conversion successful, output saved to:", output_file_path)

            # Return the path to the converted Word file
            return JsonResponse({'word_file': f'media/converted/{output_file_name}'})

        except Exception as e:
            print("Error during conversion:", str(e))  # Print error to console for debugging
            return JsonResponse({'error': 'Conversion failed: ' + str(e)}, status=500)

        finally:
            # Clean up the uploaded file after conversion
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except PermissionError:
                print(f"Cannot remove the file {file_path}. It may still be in use.")

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
