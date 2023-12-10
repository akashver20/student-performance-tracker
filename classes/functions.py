import os

def handle_uploaded_file(f):
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class_files_path = os.path.join(base_dir, 'static', 'class_files')

    os.makedirs(class_files_path, exist_ok=True)

    file_path = os.path.join(class_files_path, f.name)

    # Open the file and write the uploaded content
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path 