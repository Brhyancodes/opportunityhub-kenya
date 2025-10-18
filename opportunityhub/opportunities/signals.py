from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Application
from notifications.email_service import EmailService
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Application)
def track_application_status_change(sender, instance, **kwargs):
    """
    Track the old status before saving to detect changes
    """
    if instance.pk:  # Only for existing applications (updates)
        try:
            old_instance = Application.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Application.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None  # New application


@receiver(post_save, sender=Application)
def send_status_change_email(sender, instance, created, **kwargs):
    """
    Send email when application status changes to accepted or rejected
    """
    if not created:  # Only for updates, not new applications
        old_status = getattr(instance, "_old_status", None)
        new_status = instance.status

        # Only send email if status changed to accepted or rejected
        if old_status != new_status and new_status in ["accepted", "rejected"]:
            try:
                youth = instance.youth
                opportunity = instance.opportunity
                employer = opportunity.employer

                EmailService.send_application_status_update(
                    user_email=youth.email,
                    user_name=youth.first_name or youth.username,
                    opportunity_title=opportunity.title,
                    status=new_status,
                    employer_name=employer.company_name,
                )
                logger.info(f"Status email sent to {youth.email}: {new_status}")

            except Exception as e:
                logger.error(f"Failed to send status email: {str(e)}")
