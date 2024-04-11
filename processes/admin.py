from django.contrib import admin

from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_definition import ProcessActivityDefinition
from processes.models.process_definition import ProcessDefinition


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessDefinition)
class ProcessDefinitionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessActivityDefinition)
class ProcessActivityDefinitionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessActivity)
class ProcessActivityAdmin(admin.ModelAdmin):
    pass
