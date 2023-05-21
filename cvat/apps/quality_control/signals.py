# Copyright (C) 2023 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from django.db.models.signals import post_save
from django.dispatch import receiver

from cvat.apps.engine.models import Annotation, Job, Project, Task

from cvat.apps.quality_control import quality_reports as qc
from cvat.apps.quality_control.models import QualitySettings


@receiver(post_save, sender=Job,
    dispatch_uid=__name__ + ".save_job-update_quality_metrics")
@receiver(post_save, sender=Task,
    dispatch_uid=__name__ + ".save_task-update_quality_metrics")
@receiver(post_save, sender=Project,
    dispatch_uid=__name__ + ".save_project-update_quality_metrics")
@receiver(post_save, sender=Annotation,
    dispatch_uid=__name__ + ".save_annotation-update_quality_metrics")
def __save_job__update_quality_metrics(instance, created, **kwargs):
    tasks = []

    if isinstance(instance, Project):
        tasks += list(instance.tasks.all())
    elif isinstance(instance, Task):
        tasks.append(instance)
    elif isinstance(instance, Job):
        tasks.append(instance.segment.task)
    elif isinstance(instance, Annotation):
        tasks.append(instance.job.segment.task)
    else:
        assert False

    for task in tasks:
        qc.QualityReportUpdateManager().schedule_quality_autoupdate_job(task)


@receiver(post_save, sender=Task,
    dispatch_uid=__name__ + ".save_task-initialize_quality_settings")
def __save_task__initialize_quality_settings(instance, created, **kwargs):
    # Initializes default quality settings for the task
    # this is done here to make the components decoupled
    if created:
        QualitySettings.objects.get_or_create(task=instance)