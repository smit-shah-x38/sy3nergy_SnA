# # The following code sample demonstrates how to specify the specific layout of a DWG file to export as a PDF document in Python.
# import aspose.cad as cad

# # Load an existing DWG file
# image = cad.Image.load(r"C:\Users\Atharva\Downloads\0ne-wellington-street-st-kilda\Addendum 02\2. Architectural T02\DWG A0099 [T02] BASEMENT 01.dwg")


# # Initialize and specify CAD options
# rasterizationOptions = cad.imageoptions.CadRasterizationOptions()
# # rasterizationOptions.page_width = 1200
# rasterizationOptions.page_width = float(1200)
# # rasterizationOptions.page_height = 1200
# rasterizationOptions.page_height = float(1200)
# rasterizationOptions.layouts = ["Layout1"]

# # Specify PDF Options
# pdfOptions = cad.imageoptions.PdfOptions()
# pdfOptions.vector_rasterization_options = rasterizationOptions

# # Save as PDF

# image.save(r"C:\Users\Atharva\Downloads\output2.pdf", pdfOptions)
import aspose.cad as cad

try:
    # Load an existing DWG file
    image = cad.Image.load(r"C:\Users\Atharva\Downloads\0ne-wellington-street-st-kilda\Addendum 02\2. Architectural T02\DWG A0097 [T02] BASEMENT 03.dwg")

    # Initialize and specify CAD options
    rasterizationOptions = cad.imageoptions.CadRasterizationOptions()
    rasterizationOptions.page_width = float(1200)
    rasterizationOptions.page_height = float(1200)
    rasterizationOptions.layouts = ["Layout1"]

    # Specify PDF Options
    pdfOptions = cad.imageoptions.PdfOptions()
    pdfOptions.vector_rasterization_options = rasterizationOptions

    # Save as PDF
    image.save(r"C:\Users\Atharva\Downloads\output.pdf", pdfOptions)

    print("PDF successfully generated.")
except Exception as e:
    print("An error occurred:", e)
