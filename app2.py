import streamlit as st
import os

def get_directory_structure(path):
    """Recursively retrieves the directory structure and formats it as a string."""
    structure = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = "   " * level
        structure += f"{indent}{os.path.basename(root)}/\n"
        for filename in files:
            structure += f"{indent}  {filename}\n"
    return structure

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

def main():
    """Main function for the Streamlit app."""

    st.title("Directory Manager (Simulation)")

    current_directory = st.text_input("Directory to View", value=os.getcwd())

    action_selected = st.selectbox("Action", ["None", "Add Directory", "Remove Directory"])
    if action_selected != "None":
        handle_actions(action_selected, current_directory)
    
    if st.button("Refresh"):
        directory_structure = get_directory_structure(current_directory)
        st.text(directory_structure)
    else:
        st.write("Click the button to refresh the directory structure.")

if __name__ == "__main__":
    main()
