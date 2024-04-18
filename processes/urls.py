from django.urls import include
from django.urls import path

from processes.views import process as process_views
from processes.views import process_activity as processactivity_views
from processes.views import process_activity_instance as processactivityinstance_views
from processes.views import process_instance as processinstance_views

processinstance_urlpatterns = [
    path(
        "",
        processinstance_views.ProcessInstanceListView.as_view(),
        name="processinstance_list",
    ),
    path(
        "create/",
        processinstance_views.ProcessInstanceCreateView.as_view(),
        name="processinstance_create",
    ),
    path(
        "<int:pk>/",
        processinstance_views.ProcessInstanceDetailView.as_view(),
        name="processinstance_detail",
    ),
    path(
        "<int:pk>/update/",
        processinstance_views.ProcessInstanceUpdateView.as_view(),
        name="processinstance_update",
    ),
    path(
        "<int:pk>/delete/",
        processinstance_views.ProcessInstanceDeleteView.as_view(),
        name="processinstance_delete",
    ),
]

process_urlpatterns = [
    path(
        "",
        process_views.ProcessListView.as_view(),
        name="process_list",
    ),
    path(
        "create/",
        process_views.ProcessCreateView.as_view(),
        name="process_create",
    ),
    path(
        "<int:pk>/",
        process_views.ProcessDetailView.as_view(),
        name="process_detail",
    ),
    path(
        "<int:pk>/update/",
        process_views.ProcessUpdateView.as_view(),
        name="process_update",
    ),
    path(
        "<int:pk>/delete/",
        process_views.ProcessDeleteView.as_view(),
        name="process_delete",
    ),
    path(
        "<int:parent_pk>/activities/create/",
        processactivity_views.ProcessActivityCreateView.as_view(),
        name="processactivity_create",
    ),
]

processactivityinstance_urlpatterns = [
    path(
        "<int:pk>/complete/",
        processactivityinstance_views.ProcessActivityInstanceCompleteView.as_view(),
        name="processactivityinstance_complete",
    )
]

processactivity_urlpatterns = [
    path(
        "<int:pk>/",
        processactivity_views.ProcessActivityDetailView.as_view(),
        name="processactivity_detail",
    ),
    path(
        "<int:pk>/update/",
        processactivity_views.ProcessActivityUpdateView.as_view(),
        name="processactivity_update",
    ),
    path(
        "<int:pk>/delete/",
        processactivity_views.ProcessActivityDeleteView.as_view(),
        name="processactivity_delete",
    ),
]

urlpatterns = [
    path("processes/", include(processinstance_urlpatterns)),
    path("processes/", include(process_urlpatterns)),
    path("activity-instances/", include(processactivityinstance_urlpatterns)),
    path("activities/", include(processactivity_urlpatterns)),
]
