from django.urls import path
from . import views
from . import api

app_name = 'collection_agency'
urlpatterns = [
    path("", views.load_file, name="load_file"),
    path("accounts/", api.DebtListView.as_view(), name='debt-list'),
    path("ws-load-file", api.wsUploadFile.as_view(), name="wsUploadFile")
]

