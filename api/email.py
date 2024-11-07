import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
import os
from decouple import config

ADMIN_EMAIL = config('ADMIN_EMAIL')
FROM_EMAIL=config('FROM_EMAIL')
EMAIL_PASSWORD=config('EMAIL_PASSWORD')
EMAIL_SMTP_SERVER=config('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT= int(config('EMAIL_SMTP_PORT'))

logo_file = os.path.join(settings.BASE_DIR, "static", "images", "firstoriginallogo.png")


def send_beautiful_html_email_create_user(
    bank_id, 
    account_details, 
    to_email, 
):
    print(logo_file)
    # Email subject
    subject = "Welcome to Our Bank"
    
    # Create the HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="cid:logo" alt="Bank Logo" style="width: 150px; height: auto;"/>
            </div>
            <h2 style="color: #4CAF50; text-align: center;">Welcome to Our Bank!</h2>
            <p style="font-size: 16px; line-height: 1.6;">
                Dear customer,
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                Your bank ID is: <strong>{bank_id}</strong>
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                Your account details are: <strong>{account_details}</strong>
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                We're thrilled to have you with us. If you have any questions, feel free to reach out to our customer service team.
            </p>
            <p style="text-align: center; font-size: 14px; color: #777; margin-top: 30px;">
                © 2024 Our Bank. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = ADMIN_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Add logo image as an attachment with Content-ID
    with open(logo_file, 'rb') as img_file:
        logo_image = MIMEImage(img_file.read())
        logo_image.add_header('Content-ID', '<logo>')  # This ID should match the src in the HTML
        logo_image.add_header('Content-Disposition', 'inline', filename="logo.png")
        msg.attach(logo_image)

    try:
        # Set up the SMTP server connection
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
        
        # Send the email
        server.sendmail(ADMIN_EMAIL, to_email, msg.as_string())
        
        # Close the SMTP server connection
        server.quit()
        
        print("HTML email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_beautiful_html_email_create_account(
    account_name, 
    account_details, 
    to_email, 
):
    print(logo_file)
    # Email subject
    subject = "Welcome to Our Bank"
    
    # Create the HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="cid:logo" alt="Bank Logo" style="width: 150px; height: auto;"/>
            </div>
            <h2 style="color: #4CAF50; text-align: center;">Welcome to Our Bank!</h2>
            <p style="font-size: 16px; line-height: 1.6;">
                Dear customer,
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                Your bank ID is: <strong>{bank_id}</strong>
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                Your account details are: <strong>{account_details}</strong>
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                We're thrilled to have you with us. If you have any questions, feel free to reach out to our customer service team.
            </p>
            <p style="text-align: center; font-size: 14px; color: #777; margin-top: 30px;">
                © 2024 FirstCitizen Bank. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = ADMIN_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Add logo image as an attachment with Content-ID
    with open(logo_file, 'rb') as img_file:
        logo_image = MIMEImage(img_file.read())
        logo_image.add_header('Content-ID', '<logo>')  # This ID should match the src in the HTML
        logo_image.add_header('Content-Disposition', 'inline', filename="logo.png")
        msg.attach(logo_image)

    try:
        # Set up the SMTP server connection
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
        
        # Send the email
        server.sendmail(ADMIN_EMAIL, to_email, msg.as_string())
        
        # Close the SMTP server connection
        server.quit()
        
        print("HTML email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")




def send_beautiful_html_email_create_account(
    initial_deposit,
    info_details,
    account_name, 
    account_details,  # This should be a dictionary with details like {"Account Number": "123456789", "Account Type": "Savings", "Branch": "Main"}
    to_email
):
    # Email subject
    subject = f"Thank you for banking with us - {info_details}"
    
    # Generate table rows from account details
    account_details_html = "".join([
        f"<tr><td style='padding: 8px; border: 1px solid #ddd;'>{key}</td><td style='padding: 8px; border: 1px solid #ddd;'>{value}</td></tr>"
        for key, value in account_details.items()
    ])
    
    # Create the HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="cid:logo" alt="Bank Logo" style="width: 150px; height: auto;"/>
            </div>
            <h2 style="color: #4CAF50; text-align: center;">Thank you for banking with us, {account_name}!</h2>
            <p style="font-size: 16px; line-height: 1.6;">
                Dear {account_name},
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                {info_details}
                
            </p>
            <h3 style="color: #333;">Your Account Details:</h3>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 16px;">
                {account_details_html}
            </table>
            <p style="font-size: 16px; line-height: 1.6;">
                We're thrilled to have you with us. If you have any questions, feel free to reach out to our customer service team.
            </p>
            <p style="text-align: center; font-size: 14px; color: #777; margin-top: 30px;">
                © 2024 FirstCitizen Bank. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = ADMIN_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Attach logo image with Content-ID for inline display
    with open(logo_file, 'rb') as img_file:
        logo_image = MIMEImage(img_file.read())
        logo_image.add_header('Content-ID', '<logo>')  # This ID matches the src in the HTML
        logo_image.add_header('Content-Disposition', 'inline', filename="logo.png")
        msg.attach(logo_image)

    try:
        # Set up the SMTP server connection
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
        
        # Send the email
        server.sendmail(ADMIN_EMAIL, to_email, msg.as_string())
        
        # Close the SMTP server connection
        server.quit()
        
        print("HTML email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Password
# hbszkbhmuowlwgyv
# talk2peteresezobor@gmail.com
# 587
# smtp.gmail.com

