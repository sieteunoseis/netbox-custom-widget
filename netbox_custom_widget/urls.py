"""URL configuration for NetBox Custom Widget plugin."""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from . import models, views

urlpatterns = [
    # CustomAPIEndpoint URLs
    path(
        "endpoints/",
        views.CustomAPIEndpointListView.as_view(),
        name="customapiendpoint_list",
    ),
    path(
        "endpoints/add/",
        views.CustomAPIEndpointEditView.as_view(),
        name="customapiendpoint_add",
    ),
    path(
        "endpoints/import/",
        views.CustomAPIEndpointBulkImportView.as_view(),
        name="customapiendpoint_import",
    ),
    path(
        "endpoints/edit/",
        views.CustomAPIEndpointBulkEditView.as_view(),
        name="customapiendpoint_bulk_edit",
    ),
    path(
        "endpoints/delete/",
        views.CustomAPIEndpointBulkDeleteView.as_view(),
        name="customapiendpoint_bulk_delete",
    ),
    path(
        "endpoints/<int:pk>/",
        views.CustomAPIEndpointView.as_view(),
        name="customapiendpoint",
    ),
    path(
        "endpoints/<int:pk>/edit/",
        views.CustomAPIEndpointEditView.as_view(),
        name="customapiendpoint_edit",
    ),
    path(
        "endpoints/<int:pk>/delete/",
        views.CustomAPIEndpointDeleteView.as_view(),
        name="customapiendpoint_delete",
    ),
    path(
        "endpoints/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="customapiendpoint_changelog",
        kwargs={"model": models.CustomAPIEndpoint},
    ),
    path(
        "endpoints/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="customapiendpoint_journal",
        kwargs={"model": models.CustomAPIEndpoint},
    ),
    # BookmarkLink URLs
    path("bookmarks/", views.BookmarkLinkListView.as_view(), name="bookmarklink_list"),
    path("bookmarks/add/", views.BookmarkLinkEditView.as_view(), name="bookmarklink_add"),
    path("bookmarks/import/", views.BookmarkLinkBulkImportView.as_view(), name="bookmarklink_import"),
    path("bookmarks/edit/", views.BookmarkLinkBulkEditView.as_view(), name="bookmarklink_bulk_edit"),
    path("bookmarks/delete/", views.BookmarkLinkBulkDeleteView.as_view(), name="bookmarklink_bulk_delete"),
    path("bookmarks/<int:pk>/", views.BookmarkLinkView.as_view(), name="bookmarklink"),
    path("bookmarks/<int:pk>/edit/", views.BookmarkLinkEditView.as_view(), name="bookmarklink_edit"),
    path("bookmarks/<int:pk>/delete/", views.BookmarkLinkDeleteView.as_view(), name="bookmarklink_delete"),
    path(
        "bookmarks/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="bookmarklink_changelog",
        kwargs={"model": models.BookmarkLink},
    ),
    path(
        "bookmarks/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="bookmarklink_journal",
        kwargs={"model": models.BookmarkLink},
    ),
    # HTMX widget refresh
    path(
        "refresh/<int:pk>/",
        views.WidgetRefreshView.as_view(),
        name="widget_refresh",
    ),
]
