import streamlit as st
import pandas as pd
import numpy as np
import json
import requests


#with open("model.pkl", "rb") as file:
   # model = pickle.load(file)

endpoint = 'http://a4c410f3-a1fe-4747-9f79-c8eccd235851.westeurope.azurecontainer.io/score' #Replace with your endpoint
key = 'KdkeUAroJVT8NSpiEFhO07bSHjpUsMfB' #Replace with your key



@st.cache()
# defining the function which will make the prediction using the data which the user inputs 
def preprocess(Gender, Married, Dependents, Education, Self_Employed, Credit_History, Property_Area):
    # Pre-processing user's categorical input  
    if Gender == "Male":
        Gender = 0
    else:
        Gender = 1
 
    if Married == "Unmarried":
        Married = 0
    else:
        Married = 1
    
    if Dependents == "0":
        Dependents = 0
    elif Dependents == "1":
        Dependents = 1
    elif Dependents == "2":
        Dependents = 2
    else:
        Dependents = 3
    
    if Education == "Graduate":
        Education = 1
    else:
        Education = 0
    
    if Self_Employed == "No":
        Self_Employed = 0
    else:
        Self_Employed = 1

    if Credit_History == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1  
    
    if Property_Area == "Semiurban":
        Property_Area = 0
    elif Property_Area == "Urban":
        Property_Area = 1
    else:
        Property_Area = 2
    
    return Gender, Married, Dependents, Education, Self_Employed, Credit_History, Property_Area



"""
def prediction(Gender, Married, Dependents, Education, Self_Employed, Credit_History,
 Property_Area, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term):   
  
    
 
    # Making predictions 
    prediction = model.predict( 
        [[Gender, Married, Dependents, Education, Self_Employed, Credit_History,
 Property_Area, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term]])
     
    if prediction == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'
    return pred
"""

# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:cyan;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Bank Loan Default Prediction</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
    
    # following lines create boxes in which user can enter data required to make prediction 
    Gender = st.selectbox('Gender',("Male","Female"))
    Married = st.selectbox('Marital Status',("Unmarried","Married")) 
    Dependents = st.selectbox('Dependents', ("0", "1", "2", "3+"))
    Education = st.selectbox('Education', ("Graduate", "Not a Graduate"))
    Self_Employed = st.selectbox('Self Employed', ("Yes", "No"))
    Property_Area = st.selectbox('Property Area', ("Semiurban", "Urban", "Rural"))
    ApplicantIncome = st.number_input("Applicant's Monthly Income") 
    CoapplicantIncome = st.number_input("Coapplicant's Income")
    LoanAmount = st.number_input("Total loan amount")
    Loan_Amount_Term = st.number_input("Term of Loan")
    Credit_History = st.selectbox('Credit History', ("Unclear Debts", "No Unclear Debts"))
    result =""

    #preprocess categorical input
    #Gender, Married, Dependents, Education, Self_Employed, Credit_History, Property_Area = preprocess(Gender, Married, Dependents, Education, Self_Employed, Credit_History, Property_Area)
    

    #Features for a patient
    x = [{   
        "Gender": Gender, 
        "Married": Married, 
        "Dependents": Dependents, 
        "Education": Education, 
        "Self_Employed": Self_Employed, 
        "Credit_History": Credit_History,
        "Property_Area": Property_Area, 
        "ApplicantIncome": ApplicantIncome, 
        "CoapplicantIncome": CoapplicantIncome, 
        "LoanAmount": LoanAmount, 
        "Loan_Amount_Term": Loan_Amount_Term
        }]

    #Create a "data" JSON object
    input_json = json.dumps({"data": x})

    #Set the content type and authentication for the request
    headers = {"Content-Type":"application/json",
            "Authorization":"Bearer " + key}

    


    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        #Send the request
        response = requests.post(endpoint, input_json, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.json())
            if result["result"][0] == 0:
                pred = 'Rejected'
            else:
                pred = 'Approved'
            st.success('Your loan is {}'.format(pred))
            print(LoanAmount)
        else:
            print(response)
     
if __name__=='__main__': 
    main()
      