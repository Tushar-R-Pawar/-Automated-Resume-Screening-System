import PyPDF2
import io
import re
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import time
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/process', methods=['POST'])

def process_data():
    data = request.get_json()
    job_description = data.get('job_description')
    resume = data.get('resume')



    genai.configure(api_key='-------------')  #-------------- USE YOUR GEMINI API KEY
    # Set up the model
    generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)


    name_pattern=r'(candidate name:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    resume_score_pattern=r'(resume score:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    overall_experience_pattern=r'(overall experience:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    relevant_experience_pattern=r'(relevant experience:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    phone_number_pattern=r'(phone number:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    email_pattern=r'(email id:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    why_hire_pattern=r'(why hire:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    why_not_hire_pattern=r'(why not hire:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'

    overall_assessment_pattern=r'(overall assessment:)(.*?)(overall experience:|overall assessment:|candidate name:|relevant experience:|phone number:|email id:|why hire:|why not hire:|resume score:|")'


    info_dict={"resume_score":"",
    "candidate_name":"",
    "overall_experience":"",
    "relevant_experience":"",
    "phone_number":"",
    "email_id":"",
    "why_hire":"",
    "why_not_hire":"",
    "overall_assessment":""}

    expected_format='candidate name:extracted name of candidatate,resume score:extracted resume score,overall experience:extracted overall experience,relevant experience:extracted relevant experience,phone number:extracted phone number,email id:extracted email id,why hire:extracted why hire,why not hire:extracted why not hire,overall assessment:extracted overall assessment'

    prompt_parts = [f"analyze this resume {resume} and give summary in 5 points whether this candidate is suitable or not for the given job description{job_description} also calculate the resume score out of 100 based on the skill required for the this position which are given in job description and roles and responsibilities also extact information such as name of candidate , overall experience - this should be consist of his all work experience , relevant experience, phone no., email id, why we should hire this candidate, why we should not hire not this candidate and overall assesment and store all this information in below this format {expected_format} "]



    response = model.generate_content(prompt_parts)
    gen_ai_op=response.text
    gen_ai_op=gen_ai_op.replace('*','').replace('\n',' ').replace('Resume Analysis','')
    gen_ai_op=json.dumps(gen_ai_op)
    gen_ai_op_lower = gen_ai_op.lower()
    print(gen_ai_op)

    info_dict["candidate_name"] = re.search(name_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["resume_score"] = re.search(resume_score_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["overall_experience"] = re.search(overall_experience_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["relevant_experience"] = re.search(relevant_experience_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["phone_number"] = re.search(phone_number_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["email_id"] = re.search(email_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["why_hire"] = re.search(why_hire_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["why_not_hire"] = re.search(why_not_hire_pattern, gen_ai_op_lower).group(2).strip()
    info_dict["overall_assessment"] = re.search(overall_assessment_pattern, gen_ai_op_lower).group(2).strip()

    #print(info_dict)
    print("Sent back to client after processing")


    return jsonify(info_dict)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app