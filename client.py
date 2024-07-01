import PyPDF2
import pandas as pd
import numpy as np
import os
import time
import json
import requests

api = 'http://localhost:5000'


# text extarction from pdf
def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file.

    Args:
        pdf_file: The path to the PDF file.

    Returns:
        A string containing the extracted text.
    """

    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for i in range(num_pages):
            page_object = pdf_reader.pages[i]
            text += page_object.extract_text()
    return text



#job_description=input("enter job description here :- \n\n") #user input failing on terminal due to limitation of next line in terminal add it in script 

job_description= '''-JOB DESCRIPTION HERE-'''
print("------ Processing------")
pdf_file='''Resume here'''

resume=extract_text_from_pdf(pdf_file)

data = {
    'job_description': job_description,
    'resume': resume
}

# Send data to the server
response = requests.post(api + '/process', json=data)

if response.status_code == 200:
    print("Data Processed Successfully")
    processed_data = response.json()
    # Processed data received from the server
    # You can handle/process it as per your requirement
    #print(type(processed_data))
    print('Candidate Name :-  ',processed_data["candidate_name"])
    print('\n')
    print('Resume Score :- ',processed_data["resume_score"])
    print('\n')
    print('Overall Exp. :- ',processed_data["overall_experience"])
    print('\n')
    print('Relevant Exp. :- ',processed_data["relevant_experience"])
    print('\n')
    print('Phone no. :- ',processed_data["phone_number"])
    print('\n')
    print('Email Id. :- ',processed_data["email_id"])
    print('\n')
    print('Why We Should Hire This Candidate :- ',processed_data["why_hire"])
    print('\n')
    print("Why We Shouldn't Hire This Candidate :- ",processed_data["why_not_hire"])
    print('\n')
    print('Overall Assesment :- ',processed_data["overall_assessment"])
    
else:
    print("Error:", response.text)