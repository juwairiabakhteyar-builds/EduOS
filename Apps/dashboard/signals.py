from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from Apps.students.models import Student
from Apps.teachers.models import Teacher
from Apps.attendance.models import Attendance

from .models import ActivityLog


def create_activity(instance, module, action, description):
    ActivityLog.objects.create(
        module=module,
        action=action,
        description=description,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=str(instance.pk),
    )


@receiver(post_save, sender=Student)
def student_activity(sender, instance, created, **kwargs):
    if created:
        create_activity(
            instance,
            "Students",
            "created",
            f"New student admitted: {instance.full_name}",
        )


@receiver(post_save, sender=Teacher)
def teacher_activity(sender, instance, created, **kwargs):
    if created:
        create_activity(
            instance,
            "Teachers",
            "created",
            f"New teacher added: {instance.full_name}",
        )


@receiver(post_save, sender=Attendance)
def attendance_activity(sender, instance, created, **kwargs):
    if created:
        create_activity(
            instance,
            "Attendance",
            "created",
            f"Attendance marked: {instance.student.full_name} — {instance.status}",
        )
    else:
        create_activity(
            instance,
            "Attendance",
            "updated",
            f"Attendance updated: {instance.student.full_name} — {instance.status}",
        )