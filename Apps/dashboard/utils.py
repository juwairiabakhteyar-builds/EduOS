from django.contrib.contenttypes.models import ContentType

from .models import ActivityLog


def log_activity(
    *,
    actor,
    instance,
    module,
    action,
    description,
):
    ActivityLog.objects.create(
        actor=actor if actor and actor.is_authenticated else None,
        module=module,
        action=action,
        description=description,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=str(instance.pk),
    )