from django.urls import path
from .views import(
    ChildListView,
    ChildDetailView,

)


urlpatterns = [
    path('children/', ChildListView.as_view(), name='child-list'),
    path('children/<int:id>/', ChildDetailView.as_view(), name='child')
]