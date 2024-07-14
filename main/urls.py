from django.urls import path
from views import InstitutionAllModelViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('/', InstitutionAllModelViewSet, basename="institution")

urlpatterns=[
    
]+router.urls


