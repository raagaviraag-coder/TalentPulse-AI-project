from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
import resend


# ==============================
# LOAD ENVIRONMENT VARIABLES
# ==============================

load_dotenv()

# Resend API key
resend.api_key = os.getenv("RESEND_API_KEY")


# ==============================
# FLASK APP
# ==============================

app = Flask(__name__)


# ==============================
# LOAD MACHINE LEARNING MODEL
# ==============================

model = joblib.load("talentpulse_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# EMPLOYEE ATTRITION PREDICTION
# ==============================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Create input dictionary
        input_data = {}

        for feature in feature_columns:
            input_data[feature] = 0

        # Read values from HTML form
        for feature in feature_columns:

            if feature in request.form:

                value = request.form.get(feature)

                if value == "":
                    value = 0

                input_data[feature] = float(value)

        # Convert input into DataFrame
        input_df = pd.DataFrame([input_data])

        # Prediction
        prediction = model.predict(input_df)[0]

        # Probability
        probability = model.predict_proba(input_df)[0][1] * 100

        # Prediction message
        if prediction == 1:

            prediction_text = (
                "⚠ Employee is likely to leave the company."
            )

        else:

            prediction_text = (
                "✅ Employee is likely to stay in the company."
            )

        # Display result
        return render_template(
            "index.html",
            prediction_text=prediction_text,
            probability=round(probability, 2)
        )

    except Exception as e:

        return render_template(
            "index.html",
            prediction_text=f"Error : {str(e)}",
            probability=0
        )


# ==============================
# CONTACT / SEND EMAIL
# ==============================

@app.route("/contact", methods=["POST"])
def contact():

    # Get form values
    name = request.form.get("name", "").strip()
    recipient_email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    # Check empty fields
    if not name or not recipient_email or not message:

        return render_template(
            "index.html",
            contact_error="Please fill all the details."
        )

    try:

        # Email details
        params = {
            "from": "TalentPulse AI <onboarding@resend.dev>",

            # Email entered in Contact form
            "to": [recipient_email],

            "subject": "Message from TalentPulse AI",

            "html": f"""
                <h3>Hello {name},</h3>

                <p>{message}</p>

                <br>

                <p>
                    Regards,<br>
                    <strong>TalentPulse AI</strong>
                </p>
            """
        }

        # Send email using Resend
        response = resend.Emails.send(params)

        # Show Resend response in terminal
        print("RESEND RESPONSE:", response)

        # Success message
        return render_template(
            "index.html",
            contact_success="Message sent successfully!"
        )

    except Exception as e:

        # Show error in terminal
        print("RESEND ERROR:", e)

        return render_template(
            "index.html",
            contact_error=f"Email could not be sent: {str(e)}"
        )


# ==============================
# RUN FLASK APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=True)