import streamlit as st
import os
import google.generativeai as genai
import PyPDF2

text_file = r"E:\Work\workbackups\localdata\googleapi.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()
    
genai.configure(api_key=api_key)
model_2 = genai.GenerativeModel("gemini-pro")

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

def analyse_file(text_in_file):
    
    response_2 = model_2.generate_content("The text following is from OCR of an architectural drawing. Given its contents, what can the file be? What is the likely place of the file in the heirarchical structure of a normal project? Answer in json format, with the json object containing the fields filetype and heirarchy. Text: {}".format(text_in_file))

    return str(response_2.text).replace(r"```", "").replace("json", "")
    
def text_extract(dir_path, filepath):
    totaltext = ""
    
    pdf_file = open(r"{}\\".format(dir_path) + r"{}".format(filepath), "rb")

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
    st.write(finaltext)
    

def display_structure(path):
    """Displays the formatted directory structure."""
    directory_structure = get_directory_structure(path)
    st.text(directory_structure)

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

def save_files(uploaded_files, save_directory):
    """Saves uploaded files to the specified directory."""
    for file in uploaded_files:
        save_path = os.path.join(save_directory, file.name)
        with open(save_path, "wb") as out_file:
            out_file.write(file.getbuffer())
        text_extract(dir_path=save_directory, filepath=file.name)
    st.success(f"Files saved successfully to '{save_directory}'.")
    # analysis = analyse_file(dir_path=r"{}".format(save_directory))
    # st.write(analysis)
    
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
    
def main():
    st.title("Directory Manager & File Uploader")

    page_names = ["Directory Manager", "Manual Uploader", "Analyser"]
    page = st.sidebar.selectbox("Select Page", page_names)

    if page == "Directory Manager":
        page_directory_manager()
    elif page == "Manual Uploader":
        page_file_uploader()

if __name__ == "__main__":
    main()
