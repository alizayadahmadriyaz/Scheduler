from celery import shared_task
from django.utils.timezone import now
from .models import task,Message  # Ensure it's correctly imported

@shared_task(bind=True)
def delete_expired_tasks(self):
    """Delete tasks that are past their scheduled time."""
    try:
        expired_tasks = task.objects.filter(date__lt=now())

# Get users who owned those tasks
        task_users = expired_tasks.values_list("user", flat=True)  # Extract user IDs

        # Delete messages from those users
        Message.objects.filter(sender_id__in=task_users).delete()

        # Delete messages linked to these tasks
        # deleted_messages_count, _ = Message.objects.filter(task_id__in=task_users).delete()

        # Delete expired tasks
        deleted_tasks_count, _ = expired_tasks.delete()

        return f"Deleted {deleted_tasks_count} expired tasks ."

        


        # return f"Deleted {deleted_count} expired tasks."
    except Exception as e:
        self.retry(exc=e, countdown=5)  # Retry if failure occurs
