import streamlit as st
import joblib

# Load the vectorizer and models
vectorizer = joblib.load('vectorizer.pkl')
nb_model = joblib.load('nb_model.pkl')
svm_model = joblib.load('svm_model.pkl')
logreg_model = joblib.load('logreg_model.pkl')
rf_model = joblib.load('rf_model.pkl')
xgb_model = joblib.load('xgb_model.pkl')

# Define the function to make predictions
def predict_spam_or_ham(sms_text):
    # Preprocess the email text
    sms_vector = vectorizer.transform([sms_text])
    
    # Predict with each model
    nb_prediction = nb_model.predict(sms_vector)
    svm_prediction = svm_model.predict(sms_vector)
    logreg_prediction = logreg_model.predict(sms_vector)
    rf_prediction = rf_model.predict(sms_vector)
    xgb_prediction = xgb_model.predict(sms_vector)
    
    # Convert numeric predictions to human-readable labels (assuming 1 = spam, 0 = ham)
    label_map = {1: 'Spam', 0: 'Ham'}
    results = {
        'Naive Bayes': label_map[nb_prediction[0]],
        'SVM': label_map[svm_prediction[0]],
        'Logistic Regression': label_map[logreg_prediction[0]],
        'Random Forest': label_map[rf_prediction[0]],
        'XGBoost': label_map[xgb_prediction[0]]
    }
    
    return results

# Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="SMS Spam Classification",
        page_icon="📧",
        layout="wide"
    )

    # Title and description
    st.title("SMS Spam Classification")
    st.markdown("""
    Welcome to the SMS Spam Classification dashboard! 
    Enter your SMS text below and see how different models classify it as Spam or Ham.
    """)

    # Input text area
    sms_text = st.text_area("Enter your SMS text here:", height=150)

    if st.button("Classify"):
        if sms_text:
            with st.spinner("Classifying..."):
                predictions = predict_spam_or_ham(sms_text)
                
                # Display results with better formatting
                st.markdown("### Prediction Results:")
                for model, prediction in predictions.items():
                    color = "red" if prediction == "Spam" else "green"
                    st.markdown(f"**{model}:** <span style='color:{color};'>{prediction}</span>", unsafe_allow_html=True)
        else:
            st.warning("Please enter an SMS text.")

    # Footer
    st.markdown("""
    ---
    **Disclaimer:** The results are based on the trained models and may not be perfect. 
    Use the results as a reference and not as the sole criterion for classification.
    """)

if __name__ == "__main__":
    main()
