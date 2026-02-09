"""
Email service for sending conversion emails
"""
from flask_mail import Mail, Message
from flask import current_app
import json


def send_email(subject, recipients, body_html, body_text=None):
    """
    Send an email using Flask-Mail
    
    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        body_html: HTML email body
        body_text: Plain text email body (optional)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # In development with console backend, just print to console
        mail_backend = current_app.config.get('MAIL_BACKEND', 'smtp')
        
        if mail_backend == 'console':
            print("\n" + "="*70)
            print("📧 EMAIL (Console Backend)")
            print("="*70)
            print(f"To: {', '.join(recipients)}")
            print(f"Subject: {subject}")
            print("-"*70)
            print(body_text or "HTML Email - Check email client for formatted version")
            print("="*70 + "\n")
            return True
        
        # Otherwise use Flask-Mail
        mail = Mail(current_app)
        msg = Message(
            subject=subject,
            recipients=recipients,
            html=body_html,
            body=body_text or body_html.replace('<br>', '\n').replace('</p>', '\n\n')
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        # In development, print to console as fallback
        if current_app.config.get('DEBUG'):
            print(f"\n⚠️ Email send failed: {str(e)}")
            print("Email would be sent to:", recipients)
        return False


def send_itinerary_email(user_email, user_name, attractions_data, itinerary_summary):
    """
    Send itinerary email to user
    
    Args:
        user_email: Recipient email
        user_name: User's name
        attractions_data: List of attraction dictionaries
        itinerary_summary: Summary dict with total_days, total_cost, etc.
    """
    subject = f"Your {itinerary_summary.get('total_days', 5)}-Day Nepal Itinerary"
    
    # Build HTML email
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 20px; }}
            .summary-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea; }}
            .attraction-item {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #e0e0e0; }}
            .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🗺️ Your Nepal Adventure Awaits!</h1>
                <p>Hi {user_name},</p>
            </div>
            
            <div class="content">
                <p>Thank you for using Nepal Tourism Recommender! Here's your personalized itinerary:</p>
                
                <div class="summary-box">
                    <h2>📋 Trip Summary</h2>
                    <p><strong>Duration:</strong> {itinerary_summary.get('total_days', 'N/A')} days</p>
                    <p><strong>Estimated Cost:</strong> ${itinerary_summary.get('total_cost', 0):.2f}</p>
                    <p><strong>Daily Average:</strong> ${itinerary_summary.get('average_daily_cost', 0):.2f}</p>
                    <p><strong>Attractions:</strong> {itinerary_summary.get('attractions_count', 0)}</p>
                    <p><strong>Regions:</strong> {', '.join(itinerary_summary.get('regions_covered', []))}</p>
                </div>
                
                <h2>📍 Selected Attractions</h2>
    """
    
    for attr in attractions_data:
        html_body += f"""
                <div class="attraction-item">
                    <h3>{attr.get('name', 'N/A')}</h3>
                    <p><strong>Region:</strong> {attr.get('region', 'N/A')}</p>
                    <p><strong>Category:</strong> {attr.get('category', 'N/A')}</p>
                    <p><strong>Duration:</strong> {attr.get('duration_days', 1)} days</p>
                    <p><strong>Cost:</strong> ${attr.get('avg_cost_usd', 0)}</p>
                    <p><strong>Difficulty:</strong> {attr.get('difficulty', 'Moderate')}</p>
                    <p><strong>Best Season:</strong> {attr.get('best_season', 'Year-round')}</p>
                </div>
        """
    
    html_body += f"""
                <p style="margin-top: 30px;">
                    <strong>Need help planning your trip?</strong><br>
                    Our local travel experts are here to assist you. Reply to this email or contact us to get a customized quote.
                </p>
                
                <p>
                    <a href="mailto:{current_app.config.get('ADMIN_EMAIL', 'info@nepaltourism.com')}" class="btn">
                        💬 Contact Our Experts
                    </a>
                </p>
            </div>
            
            <div class="footer">
                <p>Nepal Tourism Recommender</p>
                <p>Happy Travels! 🎒✈️</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, [user_email], html_body)


def send_expert_consultation_notification(lead_data, admin_email):
    """
    Send notification to admin about new expert consultation request
    
    Args:
        lead_data: Lead dictionary with user info
        admin_email: Admin email to notify
    """
    subject = f"New Expert Consultation Request - {lead_data.get('name', 'Unknown')}"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #ff9800; color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 20px; }}
            .info-box {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ff9800; }}
            .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💬 New Expert Consultation Request</h1>
            </div>
            
            <div class="content">
                <p>A new user has requested expert consultation:</p>
                
                <div class="info-box">
                    <p><strong>Name:</strong> {lead_data.get('name', 'N/A')}</p>
                    <p><strong>Email:</strong> {lead_data.get('email', 'N/A')}</p>
                    <p><strong>Phone:</strong> {lead_data.get('phone', 'Not provided')}</p>
                    <p><strong>Contact Method:</strong> {lead_data.get('contact', 'Email')}</p>
                    <p><strong>Requested At:</strong> {lead_data.get('created_at', 'Just now')}</p>
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>Please contact this lead within 24 hours.</strong>
                </p>
                
                <p>
                    <a href="mailto:{lead_data.get('email', '')}" style="display: inline-block; padding: 10px 20px; background: #ff9800; color: white; text-decoration: none; border-radius: 5px;">
                        Reply to Lead
                    </a>
                </p>
            </div>
            
            <div class="footer">
                <p>Nepal Tourism Recommender - Admin Portal</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, [admin_email], html_body)


def send_quote_request_notification(lead_data, admin_email):
    """
    Send notification to admin about new quote request
    
    Args:
        lead_data: Lead dictionary with user info and attraction IDs
        admin_email: Admin email to notify
    """
    subject = f"New Quote Request - {lead_data.get('name', 'Unknown')}"
    
    attraction_ids = lead_data.get('attraction_ids', [])
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #4CAF50; color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 20px; }}
            .info-box {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #4CAF50; }}
            .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💵 New Quote Request</h1>
            </div>
            
            <div class="content">
                <p>A new user has requested a customized quote:</p>
                
                <div class="info-box">
                    <p><strong>Name:</strong> {lead_data.get('name', 'N/A')}</p>
                    <p><strong>Email:</strong> {lead_data.get('email', 'N/A')}</p>
                    <p><strong>Attractions Requested:</strong> {len(attraction_ids)} attraction(s)</p>
                    <p><strong>Attraction IDs:</strong> {', '.join(map(str, attraction_ids))}</p>
                    <p><strong>Requested At:</strong> {lead_data.get('created_at', 'Just now')}</p>
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>Please prepare a customized quote and send it to the user.</strong>
                </p>
                
                <p>
                    <a href="mailto:{lead_data.get('email', '')}" style="display: inline-block; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">
                        Send Quote
                    </a>
                </p>
            </div>
            
            <div class="footer">
                <p>Nepal Tourism Recommender - Admin Portal</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, [admin_email], html_body)


def send_confirmation_email(user_email, user_name, request_type):
    """
    Send confirmation email to user after their request
    
    Args:
        user_email: User's email
        user_name: User's name
        request_type: Type of request ('email', 'expert', 'quote')
    """
    messages = {
        'email': {
            'subject': 'Your Itinerary is on the way!',
            'message': 'We\'re preparing your itinerary and will send it to you shortly. Please check your email in a few minutes.'
        },
        'expert': {
            'subject': 'Expert Consultation Request Received',
            'message': 'Thank you for requesting expert consultation. One of our local travel experts will contact you within 24 hours to help plan your perfect Nepal adventure!'
        },
        'quote': {
            'subject': 'Quote Request Received',
            'message': 'Thank you for your interest! We\'re preparing a customized quote for your selected attractions. Our team will send you a detailed quote within 1-2 business days.'
        }
    }
    
    msg_info = messages.get(request_type, messages['email'])
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 20px; }}
            .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Request Received!</h1>
            </div>
            
            <div class="content">
                <p>Hi {user_name},</p>
                <p>{msg_info['message']}</p>
                <p>If you have any questions, feel free to reply to this email.</p>
                <p>Happy planning! 🎒</p>
            </div>
            
            <div class="footer">
                <p>Nepal Tourism Recommender</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(msg_info['subject'], [user_email], html_body)
