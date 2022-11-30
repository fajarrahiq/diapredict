import numpy as np
import pickle
import streamlit as st

st.markdown('''
  <h1 class="title">Diabetes Prediction</h1>
  <hr class="new5"
  <div>
    <p>Silahkan masukan data pasien pada form berikut ini</p>          
  </div>
''',unsafe_allow_html=True)

model = pickle.load(open('xgb_model.pkl','rb'))
scaler = pickle.load(open('scaler.pkl','rb'))

@st.cache()

def predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,	BMI, DiabetesPedigreeFunction, Age, Weight_Category_Obesity, Weight_Category_Overweight, Weight_Category_Underweight, Insulin_Category_Normal, Glucose_Category_Hipoglikemia, Glucose_Category_Normal, Glucose_Category_Pradiabetes):
  input_df = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,	BMI, DiabetesPedigreeFunction, Age, Weight_Category_Obesity, Weight_Category_Overweight, Weight_Category_Underweight, Insulin_Category_Normal, Glucose_Category_Hipoglikemia, Glucose_Category_Normal, Glucose_Category_Pradiabetes]]).astype(np.float64)
  input_dfscal = scaler.transform(input_df)
  prediction = model.predict(input_dfscal)
  return float(prediction)

def main():
  Pregnancies = st.number_input('Pregnancies',format = '%f')
  Glucose = st.number_input('Glucose',format = '%f')
  BloodPressure = st.number_input('BloodPressure',format = '%f')
  SkinThickness = st.number_input('SkinThickness',format = '%f')
  Insulin = st.number_input('Insulin',format = '%f')
  BMI = st.number_input('BMI',format = '%f')
  DiabetesPedigreeFunction = st.number_input('DiabetesPedigreeFunction',format = '%f')
  Age = st.number_input('Age',format = '%f')

  #Weight_Category
  if (BMI < 18.5):
    Weight_Category_Obesity = 0
    Weight_Category_Overweight = 0
    Weight_Category_Underweight = 1
  elif (BMI >= 25 and BMI <= 29.9):
    Weight_Category_Obesity = 0
    Weight_Category_Overweight = 1
    Weight_Category_Underweight = 0
  elif (BMI > 30):
    Weight_Category_Obesity = 1
    Weight_Category_Overweight = 0
    Weight_Category_Underweight = 0
  else:
    Weight_Category_Obesity = 0
    Weight_Category_Overweight = 0
    Weight_Category_Underweight = 0         

  #Insulin_Category
  if (Insulin >= 16 and Insulin <= 166):
    Insulin_Category_Normal = 1
  else:
    Insulin_Category_Normal = 0

  #Glucose_Category
  if (Glucose < 70):
    Glucose_Category_Hipoglikemia = 1
    Glucose_Category_Normal = 0
    Glucose_Category_Pradiabetes = 0
  elif (Glucose >= 70 and Glucose <= 140):
    Glucose_Category_Hipoglikemia = 0
    Glucose_Category_Normal = 1
    Glucose_Category_Pradiabetes = 0
  elif (Glucose > 140 and Glucose <= 199):
    Glucose_Category_Hipoglikemia = 0
    Glucose_Category_Normal = 0
    Glucose_Category_Pradiabetes = 1
  else:
    Glucose_Category_Hipoglikemia = 0
    Glucose_Category_Normal = 0
    Glucose_Category_Pradiabetes = 0

  safe_html="""  
  <div style="background-color:#F4D03F;padding:10px >
  <h2 style="color:white;text-align:center;">Pasien Tidak Terkena Diabetes</h2>
  </div>
  """
  danger_html="""  
  <div style="background-color:#F08080;padding:10px >
  <h2 style="color:black ;text-align:center;">Pasien Menderita Diabetes</h2>
  </div>
  """

  if st.button("Prediksi Diabetes"):
    output=predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,	BMI, DiabetesPedigreeFunction, Age, Weight_Category_Obesity, Weight_Category_Overweight, Weight_Category_Underweight, Insulin_Category_Normal, Glucose_Category_Hipoglikemia, Glucose_Category_Normal, Glucose_Category_Pradiabetes)
    st.success('Presdiksi dari pasien adalah {}'.format(output))

    if output == 0:
      st.markdown(safe_html,unsafe_allow_html=True)
    else:
      st.markdown(danger_html,unsafe_allow_html=True)

if __name__ == "__main__":
  main()
