import os
import zipfile

def zipdir(path, ziph):
    # ziph is the zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # Add each file to the ZIP archive
            ziph.write(file_path, os.path.relpath(file_path, path))

# Specify the directory you want to zip
directory_to_zip = r"E:\neov_ide\synergy\sy3nergy_SnA\dir1"

# Name for the output ZIP file
output_zip_filename = 'my_directory.zip'

# Create a new ZIP file
with zipfile.ZipFile(output_zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zipdir(directory_to_zip, zip_file)

print(f"Directory '{directory_to_zip}' has been zipped to '{output_zip_filename}'.")
