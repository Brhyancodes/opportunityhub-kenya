from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notifications.email_service import EmailService
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    """
    Automatically send welcome email when a new user registers
    """
    if created:  # Only run for newly created users
        try:
            from django.db import transaction

            def send_email():
                try:
                    # Determine user type
                    if hasattr(instance, "youthprofile"):
                        user_type = "youth"
                    elif hasattr(instance, "employerprofile"):
                        user_type = "employer"
                    else:
                        user_type = (
                            instance.user_type
                            if hasattr(instance, "user_type")
                            else "youth"
                        )

                    # Send welcome email
                    success = EmailService.send_welcome_email(
                        user_email=instance.email,
                        user_name=instance.first_name or instance.username,
                        user_type=user_type,
                    )

                    if success:
                        logger.info(f"Welcome email sent to: {instance.email}")
                    else:
                        logger.warning(f"Welcome email failed for: {instance.email}")

                except Exception as e:
                    logger.error(
                        f"Error sending welcome email to {instance.email}: {str(e)}"
                    )

            transaction.on_commit(send_email)

        except Exception as e:
            logger.error(f"Error queueing welcome email for {instance.email}: {str(e)}")
