import PIL.Image
import google.generativeai as genai

text_file = r"E:\Work\sem5backups\localdata\google_apikey.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()
    
genai.configure(api_key=api_key)

img = PIL.Image.open(r"C:\Users\Smit\Downloads\imageofdeath.jpg")
model = genai.GenerativeModel('gemini-pro-vision')
response = model.generate_content(img)
print(response.text)
print("---------------------------------")

rtext = response.text

model_2 = genai.GenerativeModel('gemini-pro')
response_2 = model_2.generate_content("Using the text following, What does this image contain, and what field of STEM does this belong to? What are the different parts of this image, and what do each of them represent? Answer in json format. Text: {}".format(rtext))

print(str(response_2.text).replace(r"```", ""))