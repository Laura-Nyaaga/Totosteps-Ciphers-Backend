from django.urls import path
<<<<<<< HEAD
from .views import(
    ChildListView,
    ChildDetailView,

)


urlpatterns = [
    path('children/', ChildListView.as_view(), name='child-list'),
    path('children/<int:id>/', ChildDetailView.as_view(), name='child')
]
=======
from .views import AutismImageDetailListView, AutismResultDetailListView, AutismResultListView, AutismImageListView

urlpatterns = [
    # path('upload-image/', AutismImageListView.as_view(), name='upload-autism-image'),  
    path('results/<int:image_id>/', AutismResultDetailListView.as_view(), name='autism-result-detail'), 
    path('results/', AutismResultListView.as_view(), name='autism-result-list'),  
    path('images/', AutismImageListView.as_view(), name='image-list'),  
    path('images/<int:image_id>/',AutismImageDetailListView.as_view(), name='image-details'),  
]
>>>>>>> 28d6f20 (add autism results and the image)
