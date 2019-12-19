from django.contrib import admin
from django.urls import path

from itnotes.views import (itnotes_index, treetest, treemptt, 
LocalNotesFormView, devnavbar, get_content_note, post_update_note, post_create_note, post_delete_note)

urlpatterns = [
    path("", itnotes_index, name='itnotes_index'),
    path("treetest/", treetest, name='itnotes_tree'),
    path("treemptt/", treemptt, name='itnotes_treemptt'),
    path('treeitnotes/', LocalNotesFormView.as_view(), name="treeitnotes"),
    path('devnavbar/', devnavbar, name="devnavbar"),
    path('note/<str:namenotes>/', get_content_note, name='content_note'),
    path('noteupdate/<str:namenotes>/', post_update_note, name='post_update_note'),
    path('notecreate/<str:namenotes>/', post_create_note, name='post_create_note'),
    path('notedelete/<str:namenotes>/', post_delete_note, name='post_delete_note'),
]
