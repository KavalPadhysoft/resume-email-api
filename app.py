from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import base64

app = Flask(__name__)

# ==== CONFIGURE YOUR EMAIL ACCOUNT ====
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "yourmail@gmail.com"        # your email
SMTP_PASSWORD = "your-app-password"         # Gmail App Password (not normal password)

@app.route("/sendresume", methods=["POST"])
def send_resume():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    file_name = data.get("file_name")
    file_content_base64 = data.get("file_content")

    if not all([name, email, file_name, file_content_base64]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Decode file
    file_bytes = base64.b64decode(file_content_base64)

    # Create email message
    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = email
    msg["Subject"] = f"Resume Submission from {name}"

    # HTML template
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color:#f4f4f4; padding:20px; border-radius:8px;">
                <h2 style="color:#0073e6;">Resume Submission Received</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p>Thank you for submitting your resume. We will get back to you shortly.</p>
            </div>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    # Attach resume
    msg.add_attachment(file_bytes, maintype="application", subtype="octet-stream", filename=file_name)

    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"status": "success", "message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
