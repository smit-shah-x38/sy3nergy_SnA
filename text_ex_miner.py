# Import PyPDF2
import PyPDF2

# Open the pdf file
pdf_file = open(r"C:\Users\Smit\Downloads\BDA_EXP1.pdf", "rb")

# Create a pdf reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Loop through each page
for page in range(len(pdf_reader.pages)):
  # Get the page object
  pdf_page = pdf_reader.pages[page]
  # Extract the text
  page_text = pdf_page.extract_text()
  # Print the text
  print(page_text)

# Close the file
pdf_file.close()
