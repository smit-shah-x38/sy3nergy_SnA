# Import PyPDF2
import PyPDF2
import os

# Get the directory path
dir_path = r"E:\Work\workbackups\localdata\PDFs"

# Get list of files
files = os.listdir(dir_path)
# Open the pdf file
for filepath in files[0:10]:
  pdf_file = open(r"{}\\".format(dir_path) + r"{}".format(filepath), "rb")

  # Create a pdf reader object
  pdf_reader = PyPDF2.PdfReader(pdf_file)

  # Loop through each page
  for page in range(len(pdf_reader.pages)):
    # Get the page object
    pdf_page = pdf_reader.pages[page]
    # Extract the text
    page_text = pdf_page.extract_text()
    # Print the text
    # print(str(page_text)[0:10])
    # print("-----------")
    
    with open(r"sample_outs\{}.txt".format(filepath), "w") as file_txt:
      file_txt.write(page_text)

  # Close the file
  pdf_file.close()
