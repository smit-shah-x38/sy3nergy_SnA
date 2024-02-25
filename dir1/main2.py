import streamlit as st
import os
import google.generativeai as genai
import PyPDF2
import json
import zipfile
import os
from colorama import Fore, Back, Style
import fitz
import argparse
import logging
import shutil
import subprocess
import sys
import tempfile

DEFAULT_CHECK_COMMAND = "which"
WINDOWS_CHECK_COMMAND = "where"
TESSERACT_DATA_PATH_VAR = 'TESSDATA_PREFIX'

VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".gif", ".png", ".tga", ".tif", ".bmp"]


text_file = r"C:\Users\Atharva\OneDrive\Desktop\Atharva Rajmane\3rd Year\google_api_key.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()
    
genai.configure(api_key=api_key)
model_2 = genai.GenerativeModel("gemini-pro")

def analyse_file(text_in_file):
    
    response_2 = model_2.generate_content("The text following is from OCR of an architectural drawing. Given its contents, what can the file be? What would a brief summary of the file be? Answer in json format, with the json object containing the fields filetype and summary. Text: {}".format(text_in_file))

    return str(response_2.text).replace(r"```", "").replace("json", "").replace("JSON", "")
    
def text_extract(dir_path, filename):
    totaltext = ""
    
    pdf_file = open(r"{}\\".format(dir_path) + r"{}".format(filename), "rb")

  # Create a pdf reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Loop through each page
    for page in range(len(pdf_reader.pages)):
        # Get the page object
        pdf_page = pdf_reader.pages[page]
        # Extract the text
        page_text = pdf_page.extract_text()
        totaltext += page_text
    finaltext = analyse_file(text_in_file=totaltext)
    final_json = json.loads(finaltext)
    st.write(final_json)
    
    return final_json

def create_directory(path):
    """
    Create directory at given path if directory does not exist
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def check_path(path):
    """
    Check if file path exists or not
    :param path:
    :return: boolean
    """
    return bool(os.path.exists(path))


def get_command():
    """
    Check OS and return command to identify if tesseract is installed or not
    :return:
    """
    if sys.platform.startswith('win'):
        return WINDOWS_CHECK_COMMAND
    return DEFAULT_CHECK_COMMAND


def run_tesseract(filename, output_path, image_file_name):
    # Run tesseract
    filename_without_extension = os.path.splitext(filename)[0]
    # If no output path is provided
    if not output_path:
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, filename_without_extension)
        subprocess.run(['tesseract', image_file_name, temp_file],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        with open('{}.txt'.format(temp_file), 'r', encoding="utf8") as f:
            text = f.read()
        shutil.rmtree(temp_dir)
        return text
    text_file_path = os.path.join(output_path, filename_without_extension)
    subprocess.run(['tesseract', image_file_name, text_file_path],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
    return


def check_pre_requisites_tesseract():
    """
    Check if the pre-requisites required for running the tesseract application are satisfied or not
    :param : NA
    :return: boolean
    """
    check_command = get_command()
    logging.debug("Running `{}` to check if tesseract is installed or not.".format(check_command))

    result = subprocess.run([check_command, 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("tesseract-ocr missing, install `tesseract` to resolve. Refer to README for more instructions.")
        return False
    logging.debug("Tesseract correctly installed!\n")

    if sys.platform.startswith('win'):
        environment_variables = os.environ
        logging.debug(
            "Checking if the Tesseract Data path is set correctly or not.\n")
        if TESSERACT_DATA_PATH_VAR in environment_variables:
            if environment_variables[TESSERACT_DATA_PATH_VAR]:
                path = environment_variables[TESSERACT_DATA_PATH_VAR]
                logging.debug("Checking if the path configured for Tesseract Data Environment variable `{}` \
                as `{}` is valid or not.".format(TESSERACT_DATA_PATH_VAR, path))
                if os.path.isdir(path) and os.access(path, os.R_OK):
                    logging.debug("All set to go!")
                    return True
                else:
                    logging.error(
                        "Configured path for Tesseract data is not accessible!")
                    return False
            else:
                logging.error("Tesseract Data path Environment variable '{}' configured to an empty string!\
                ".format(TESSERACT_DATA_PATH_VAR))
                return False
        else:
            logging.error("Tesseract Data path Environment variable '{}' needs to be configured to point to\
            the tessdata!".format(TESSERACT_DATA_PATH_VAR))
            return False
    else:
        return True


def img_extract(dir_path,filename):
    pdffile =  r"{}\\".format(dir_path) + r"{}".format(filename)
    namefile = f"random_{filename}"
    
    zoom = 2
    

    # Setting default saving path
    if ":" not in namefile:
        save = rf"dir1\temp2\\{namefile}\\"  # change the path to your desktop
    else:
        save = rf"{namefile}\\"
    os.makedirs(save)

    doc = fitz.open(pdffile)
    i = 0
    mat = fitz.Matrix(zoom, zoom)

    # Loop through all pages
    for page in doc:  # Total number of pages
        pix = page.get_pixmap(matrix=mat)
        output = f"{save}{namefile}_{page.number}.png"  # Name and path of your saving folder
        pix.save(output)
        # print(f"Finish converting page {page.number}")
        # i += 1

    outpath = rf"C:\Users\Atharva\OneDrive\Desktop\Atharva Rajmane\3rd Year\Synergy\sy3nergy_SnA\dir1\temp3\random_{filename}"
    tes_run(input_path=rf"C:\Users\Atharva\OneDrive\Desktop\Atharva Rajmane\3rd Year\Synergy\sy3nergy_SnA\dir1\dir1\temp2\random_{filename}",
            output_path=outpath)

    output_file = rf"{filename}_explained.txt"

    with open(output_file, "w") as outfile:
        for filename in os.listdir(outpath):
            if filename.endswith(".txt"):
                with open(os.path.join(outpath, filename), "r+", encoding='utf-8') as infile:
                    outfile.write(infile.read())

    with open(output_file, "r") as f:
        totaltext = f.read().strip()

    finaltext = analyse_file(text_in_file=totaltext)
    final_json = json.loads(finaltext)
    st.write(final_json)

    return final_json
    # print(f"{Fore.GREEN}Finish converting{Fore.BLUE} {i} {Style.RESET_ALL}{Fore.GREEN}pages{Style.RESET_ALL}")
        
def tes_run(input_path, output_path):
    # Check if tesseract is installed or not
    if not check_pre_requisites_tesseract():
        return

    # Check if a valid input directory is given or not
    if not check_path(input_path):
        logging.error("Nothing found at `{}`".format(input_path))
        return

    # Create output directory
    if output_path:
        create_directory(output_path)
        logging.debug("Creating Output Path {}".format(output_path))

    # Check if input_path is directory or file
    if os.path.isdir(input_path):
        logging.debug("The Input Path is a directory.")
        # Check if input directory is empty or not
        total_file_count = len(os.listdir(input_path))
        if total_file_count == 0:
            logging.error("No files found at your input location")
            return

        # Iterate over all images in the input directory
        # and get text from each image
        other_files = 0
        successful_files = 0
        logging.info("Found total {} file(s)\n".format(total_file_count))
        for ctr, filename in enumerate(os.listdir(input_path)):
            logging.debug("Parsing {}".format(filename))
            extension = os.path.splitext(filename)[1]

            if extension.lower() not in VALID_IMAGE_EXTENSIONS:
                other_files += 1
                continue

            image_file_name = os.path.join(input_path, filename)
            print(run_tesseract(filename, output_path, image_file_name))
            successful_files += 1

        logging.info("Parsing Completed!\n")
        if successful_files == 0:
            logging.error("No valid image file found.")
            logging.error("Supported formats: [{}]".format(
                ", ".join(VALID_IMAGE_EXTENSIONS)))
        else:
            logging.info(
                "Successfully parsed images: {}".format(successful_files))
            logging.info(
                "Files with unsupported file extensions: {}".format(other_files))

    else:
        filename = os.path.basename(input_path)
        logging.debug("The Input Path is a file {}".format(filename))
        print(run_tesseract(filename, output_path, input_path))



def get_directory_structure(path):
    """Recursively retrieves the directory structure and formats it as a string."""
    structure = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = "      " * level
        structure += f"{indent}{os.path.basename(root)}/\n"
        for filename in files:
            structure += f"{indent}  {filename}\n"
    return structure

def display_structure(path):
    """Displays the formatted directory structure."""
    directory_structure = get_directory_structure(path)
    st.text(directory_structure)

def save_files(uploaded_files, save_directory):
    """Saves uploaded files to the specified directory."""
    for file in uploaded_files:
        if save_directory:
            try:
                os.makedirs(save_directory)
                st.success(f"Directory '{save_directory}' created successfully.")
            except FileExistsError:
                st.error(f"Directory '{save_directory}' already exists.")
        save_path = os.path.join(save_directory, file.name)
        with open(save_path, "wb") as out_file:
            out_file.write(file.getbuffer())
    st.success(f"Files saved successfully to '{save_directory}'.")

def handle_actions(action, directory):
    """Simulates directory actions based on user input."""
    if action == "Add Directory":
        new_dir_name = st.text_input("Enter directory name:")
        if new_dir_name:
            try:
                os.makedirs(os.path.join(directory, new_dir_name))
                st.success(f"Directory '{new_dir_name}' created successfully.")
            except FileExistsError:
                st.error(f"Directory '{new_dir_name}' already exists.")
    elif action == "Remove Directory":
        remove_dir_name = st.text_input("Enter directory name to remove:")
        if remove_dir_name:
            try:
                os.rmdir(os.path.join(directory, remove_dir_name))
                st.success(f"Directory '{remove_dir_name}' removed successfully.")
            except (FileNotFoundError, PermissionError) as e:
                st.error(f"Error removing directory: {str(e)}")

def page_directory_manager():
    current_directory = st.text_input("Directory to View", value=os.getcwd())

    action_selected = st.selectbox("Action", ["None", "Add Directory", "Remove Directory"])
    if action_selected != "None":
        handle_actions(action_selected, current_directory)
    
    if st.button("Refresh"):
        directory_structure = get_directory_structure(current_directory)
        st.text(directory_structure)
    else:
        st.write("Click the button to refresh the directory structure.")                

def page_file_uploader():
    """Allows uploading files and specifying a save directory."""
    st.subheader("File Uploader")

    uploaded_files = st.file_uploader("Upload Files", type=["pdf", "jpg", "txt"], accept_multiple_files=True)
    
    current_directory = os.getcwd()
    
    # folders = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
    # selected_directory_level1 = st.selectbox("Root Directory", folders)

    # # Simulate subdirectories within the chosen root directory
    # if selected_directory_level1:
    #     subdirectories = os.listdir(os.path.join(os.getcwd(), selected_directory_level1))
    #     selected_directory_level2 = st.selectbox("Subdirectory", ["None"] + subdirectories)
    #     if selected_directory_level2 != "None":
    #         save_directory = os.path.join(os.getcwd(), selected_directory_level1, selected_directory_level2)
    #     else:
    #         save_directory = os.path.join(os.getcwd(), selected_directory_level1)
    # else:
    #     save_directory = None
    
    save_directory = current_directory + "\\temp"

    if uploaded_files and save_directory:
        save_files(uploaded_files, save_directory)
        
        for uploaded_file in uploaded_files:    
            choice = st.selectbox("Images or Text", ["Text", "Image"])
            if choice == "Text":
                jsonobj = text_extract(save_directory, uploaded_file.name)
            else:
                jsonobj = img_extract(save_directory, uploaded_file.name)
        
        if jsonobj:
            if jsonobj["filetype"]:
                save_files(uploaded_files=uploaded_files, save_directory=jsonobj["filetype"])

def zipdir(path, ziph):
    # ziph is the zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # Add each file to the ZIP archive
            ziph.write(file_path, os.path.relpath(file_path, path))

def page_file_uploader_2():
    """Allows uploading files and specifying a save directory."""
    st.subheader("File Uploader")

    uploaded_files = st.file_uploader("Upload Files", type=["pdf", "jpg", "txt"], accept_multiple_files=True)
    
    current_directory = os.getcwd()
    
    folders = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
    selected_directory_level1 = st.selectbox("Root Directory", folders)

    # Simulate subdirectories within the chosen root directory
    if selected_directory_level1:
        subdirectories = os.listdir(os.path.join(os.getcwd(), selected_directory_level1))
        selected_directory_level2 = st.selectbox("Subdirectory", ["None"] + subdirectories)
        if selected_directory_level2 != "None":
            save_directory = os.path.join(os.getcwd(), selected_directory_level1, selected_directory_level2)
        else:
            save_directory = os.path.join(os.getcwd(), selected_directory_level1)
    else:
        save_directory = None
    
    save_directory = current_directory + "\\temp"

    if uploaded_files and save_directory:
        save_files(uploaded_files, save_directory)

# Function to get list of files in a directory
def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), directory))
    return file_list

# Function to delete a file
def delete_file(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"File '{filename}' deleted successfully.")
    else:
        st.error(f"File '{filename}' does not exist.")

def file_deleter():
    directory = os.getcwd()
    st.header("List of Files")
    files = list_files(directory)
    selected_file = st.selectbox("Select a file to delete:", files)

    # Delete selected file
    if st.button("Delete File"):
        delete_file(directory, selected_file)
    
    # Display the list of files
    st.write("Files in directory:", files)



def zipper():
    st.subheader("Zip Downloader")
    # Specify the directory you want to zip
    directory_to_zip = r"C:\Users\Atharva\OneDrive\Desktop\Atharva Rajmane\3rd Year\Synergy\sy3nergy_SnA\dir1"

    # Name for the output ZIP file
    output_zip_filename = r'my_directory.zip'

    # Create a new ZIP file
    with zipfile.ZipFile(output_zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zipdir(directory_to_zip, zip_file)
        
    with open("my_directory.zip", "rb") as fp:
        st.download_button(label="Download ZIP", data=fp, file_name="my_directory.zip", mime="application/zip")
    
def main():
    st.title("Directory Manager & File Sorter")

    page_names = ["Directory Manager", "Uploader", "Zipper", "Manual Delete", "Manual Upload"]
    page = st.sidebar.selectbox("Select Page", page_names)

    if page == "Directory Manager":
        page_directory_manager()
    elif page == "Uploader":
        page_file_uploader()
    elif page == "Zipper":
        zipper()
    elif page == "Manual Delete":
        file_deleter()
    elif page == "Manual Upload":
        page_file_uploader_2()
                
if __name__ == "__main__":
    main() 