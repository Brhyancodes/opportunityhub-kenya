import resend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Resend with API key
resend.api_key = settings.RESEND_API_KEY


class EmailService:
    """
    Email service for OpportunityHub notifications using Resend
    Supports both plain text and HTML emails
    """

    @staticmethod
    def send_opportunity_match(
        user_email, user_name, opportunity_title, opportunity_link, match_score
    ):
        """
        Send email when a new opportunity matches a youth's profile

        Args:
            user_email (str): Recipient's email address
            user_name (str): User's first name
            opportunity_title (str): Title of the opportunity
            opportunity_link (str): URL to the opportunity
            match_score (int): Match score percentage (0-100)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        subject = f"🎯 New Opportunity Match: {opportunity_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <div style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); padding: 30px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 28px;">OpportunityHub Kenya</h1>
                    <p style="color: #e8f8f5; margin: 10px 0 0 0; font-size: 14px;">Connecting Talent with Opportunities 🇰🇪</p>
                </div>
                
                <div style="padding: 40px 30px;">
                    <h2 style="color: #2c3e50; margin: 0 0 20px 0; font-size: 24px;">Hi {user_name}! 👋</h2>
                    <p style="color: #555; font-size: 16px; line-height: 1.6; margin: 0 0 25px 0;">
                        Great news! We found an opportunity that matches your skills and profile.
                    </p>
                    
                    <div style="background-color: #f8f9fa; border-left: 4px solid #27ae60; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <h3 style="color: #27ae60; margin: 0 0 15px 0; font-size: 20px;">{opportunity_title}</h3>
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="background-color: #27ae60; color: white; padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: bold;">
                                {match_score}% Match
                            </span>
                        </div>
                        <p style="color: #666; font-size: 14px; line-height: 1.5; margin: 15px 0 0 0;">
                            This opportunity aligns well with your profile based on your skills, experience, and location preferences.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{opportunity_link}" 
                           style="display: inline-block; background-color: #27ae60; color: white; 
                                  padding: 14px 40px; text-decoration: none; border-radius: 6px; 
                                  font-size: 16px; font-weight: bold;">
                            View Opportunity →
                        </a>
                    </div>
                    
                    <p style="color: #999; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0; padding-top: 20px; border-top: 1px solid #eee;">
                        <strong>Pro Tip:</strong> Apply early to increase your chances!
                    </p>
                </div>
                
                <div style="background-color: #2c3e50; padding: 25px 30px; text-align: center;">
                    <p style="color: #bdc3c7; font-size: 14px; margin: 0;">
                        Best regards,<br>
                        <strong style="color: #ecf0f1;">The OpportunityHub Kenya Team</strong>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return EmailService._send_email(
            to_email=user_email, subject=subject, html_content=html_content
        )

    @staticmethod
    def send_application_status_update(
        user_email, user_name, opportunity_title, status, employer_name=None
    ):
        """
        Send email when application status changes
        """
        status_config = {
            "accepted": {
                "emoji": "🎉",
                "title": "Congratulations!",
                "message": "Your application has been accepted!",
                "color": "#27ae60",
                "bg_color": "#e8f8f5",
            },
            "rejected": {
                "emoji": "💪",
                "title": "Application Update",
                "message": "Not this time, but keep trying!",
                "color": "#e74c3c",
                "bg_color": "#fadbd8",
            },
        }

        config = status_config.get(
            status.lower(),
            {
                "emoji": "📋",
                "title": "Application Update",
                "message": f"Status updated to: {status}",
                "color": "#95a5a6",
                "bg_color": "#f8f9fa",
            },
        )

        subject = f"{config['emoji']} Application Update: {opportunity_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <div style="background: #2c3e50; padding: 30px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0;">OpportunityHub Kenya</h1>
                </div>
                
                <div style="padding: 40px 30px;">
                    <h2 style="color: #2c3e50; margin: 0 0 20px 0;">Hi {user_name}! 👋</h2>
                    
                    <div style="background-color: {config['bg_color']}; border-left: 4px solid {config['color']}; padding: 25px; border-radius: 8px; margin: 25px 0;">
                        <div style="font-size: 36px; margin-bottom: 10px;">{config['emoji']}</div>
                        <h3 style="color: {config['color']}; margin: 0 0 15px 0;">{config['title']}</h3>
                        <h4 style="color: #2c3e50; margin: 0 0 10px 0;">{opportunity_title}</h4>
                        <p style="color: #555; font-size: 16px; margin: 20px 0 0 0;">
                            {config['message']}
                        </p>
                    </div>
                </div>
                
                <div style="background-color: #2c3e50; padding: 25px 30px; text-align: center;">
                    <p style="color: #bdc3c7; font-size: 14px; margin: 0;">
                        Best regards,<br>
                        <strong style="color: #ecf0f1;">The OpportunityHub Kenya Team</strong>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return EmailService._send_email(
            to_email=user_email, subject=subject, html_content=html_content
        )

    @staticmethod
    def send_welcome_email(user_email, user_name, user_type):
        """
        Send welcome email to new users
        """
        subject = "🎉 Welcome to OpportunityHub Kenya!"

        if user_type == "youth":
            message = "Start discovering opportunities that match your skills!"
            steps = """
                <li style="margin-bottom: 12px; color: #555;">✅ Complete your profile</li>
                <li style="margin-bottom: 12px; color: #555;">🔍 Browse opportunities</li>
                <li style="margin-bottom: 12px; color: #555;">📝 Apply to positions</li>
            """
        else:
            message = "Start posting opportunities and connect with talent!"
            steps = """
                <li style="margin-bottom: 12px; color: #555;">✅ Complete company profile</li>
                <li style="margin-bottom: 12px; color: #555;">📢 Post opportunities</li>
                <li style="margin-bottom: 12px; color: #555;">👥 Review applications</li>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <div style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); padding: 40px 20px; text-align: center;">
                    <div style="font-size: 64px; margin-bottom: 15px;">🎉</div>
                    <h1 style="color: #ffffff; margin: 0; font-size: 32px;">Welcome to OpportunityHub!</h1>
                    <p style="color: #e8f8f5; margin: 15px 0 0 0;">Connecting Talent with Opportunities 🇰🇪</p>
                </div>
                
                <div style="padding: 40px 30px;">
                    <h2 style="color: #2c3e50; margin: 0 0 15px 0;">Hi {user_name}! 👋</h2>
                    <p style="color: #555; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        Thank you for joining OpportunityHub Kenya!
                    </p>
                    <p style="color: #555; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                        {message}
                    </p>
                    
                    <div style="background-color: #f8f9fa; padding: 25px; border-radius: 8px; margin: 25px 0;">
                        <h3 style="color: #27ae60; margin: 0 0 20px 0;">🚀 Get Started:</h3>
                        <ul style="list-style: none; padding: 0; margin: 0;">
                            {steps}
                        </ul>
                    </div>
                </div>
                
                <div style="background-color: #2c3e50; padding: 25px 30px; text-align: center;">
                    <p style="color: #bdc3c7; font-size: 14px; margin: 0;">
                        Best regards,<br>
                        <strong style="color: #ecf0f1;">The OpportunityHub Kenya Team</strong>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return EmailService._send_email(
            to_email=user_email, subject=subject, html_content=html_content
        )

    @staticmethod
    def _send_email(to_email, subject, html_content):
        """
        Internal method to send email using Resend
        """
        try:
            params = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }

            response = resend.Emails.send(params)

            logger.info(
                f"Email sent successfully to {to_email} - ID: {response.get('id', 'N/A')}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
