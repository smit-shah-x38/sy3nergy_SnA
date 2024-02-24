import os
import google.generativeai as genai

text_file = r"E:\Work\workbackups\localdata\googleapi.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()
    
genai.configure(api_key=api_key)

# Get the directory path
dir_path = r"E:\neov_ide\synergy\sy3nergy_SnA\sample_outs"

# Get list of files
files = os.listdir(dir_path)

model_2 = genai.GenerativeModel('gemini-pro')
for file in files:
    with open(r"{}\\".format(dir_path) + r"{}".format(file), "r") as f:
        text_in_file = f.read().strip()
    
    response_2 = model_2.generate_content("The text following is from OCR of an architectural drawing. Given its contents, what can the file be? What is the likely place of the file in the heirarchical structure of a normal project? Answer in json format, with the json object containing the fields filetype and heirarchy. Text: {}".format(text_in_file))

    print(str(response_2.text).replace(r"```", "").replace("json", ""))
    print("---------------")