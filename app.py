from flask import Flask, render_template, request
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load medical data from Excel
try:
    medical_df = pd.read_excel("medical_data.xlsx")
    medical_df['Common Symptoms'] = medical_df['Common Symptoms'].str.strip().str.lower()
except FileNotFoundError:
    print("Error: medical_data.xlsx not found. Using sample data.")
    medical_data = {
        'Common Symptoms': ['common cold', 'flu'],
        'Potential Treatments (Consult a Doctor)': ['Rest, fluids, OTC pain relievers', 'Rest, fluids, antiviral meds'],
        'Prevention Tips (General)': ['Handwashing', 'Flu vaccine'],
        'Notes': ['Usually resolves in a week', 'Can lead to complications']
    }
    medical_df = pd.DataFrame(medical_data)

@app.route("/", methods=['GET', 'POST'])
def index():
    selected_table_data = None

    if request.method == 'POST':
        if 'symptom_input1' in request.form and 'symptom_input2' in request.form:
            symptom_name1 = request.form['symptom_input1'].strip().lower()
            symptom_name2 = request.form['symptom_input2'].strip().lower()
            matching_rows = medical_df[
                (medical_df['Common Symptoms'].str.contains(symptom_name1)) &
                (medical_df['Common Symptoms'].str.contains(symptom_name2))
            ]
            if not matching_rows.empty:
                selected_table_data = matching_rows.to_html(index=False, classes='table table-bordered')
            else:
                selected_table_data = "Symptoms not found."

    return render_template('index.html', selected_table_data=selected_table_data)

if __name__ == '__main__':
    app.run(debug=True)