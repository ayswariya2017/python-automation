import smtplib
import pandas as pd
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# -----------------------------
# Load email config
# -----------------------------
with open("config.json", "r") as f:
    cfg = json.load(f)

sender_email = cfg["sender_email"]
sender_pass = cfg["sender_password"]
receiver_email = cfg["receiver_email"]
subject = cfg["subject"]

# -----------------------------
# Read & analyze the CSV
# -----------------------------
df = pd.read_csv("data.csv")

total_items = len(df)
total_quantity = df["quantity"].sum()
total_value = (df["quantity"] * df["price"]).sum()

summary = f"""
Daily Report Summary 📊

Total unique items: {total_items}
Total quantity sold: {total_quantity}
Total value: ₹{total_value}

Detailed table:
{df.to_string(index=False)}

"""

# -----------------------------
# Email sending setup
# -----------------------------
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(summary, "plain"))

# -----------------------------
# Send the email
# -----------------------------
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_pass)
    server.send_message(msg)
    server.quit()

    print("Email sent successfully! 🚀")

except Exception as e:
    print("Failed to send email:", e)