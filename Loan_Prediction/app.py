import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
cb = pickle.load(open('loan_c.pkl', 'rb'))
mms = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['Credit_History'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        
        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncomelog = np.log(ApplicantIncome)
        CoapplicantIncomelog = np.log(CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        credithistorylog = np.nan_to_num(credit)
        prediction = cb.predict([[credithistorylog, ApplicantIncomelog,LoanAmountlog,CoapplicantIncomelog, male, married_yes, not_graduate, employed_yes,semiurban, urban ]])

        # print(prediction)

        if(prediction=="N"):
            prediction="No"
        else:
            prediction="Yes"


        return render_template("prediction.html", prediction_text="loan status is {}".format(prediction))




    else:
        return render_template("prediction.html")



if __name__ == "__main__":
    app.run(debug=True)