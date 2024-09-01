from django.urls import path
from .views import InstitutionAllViewSet, ScheduleView, WorkingHoursApiView, ShowAvailableHoursApiView, \
    ReserveInstApiView, ProcessPaymentApiView, CardTokensViewSet, RateServiceViewSet
    
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('feed', InstitutionAllViewSet, basename="institution")
router.register('cards', CardTokensViewSet, basename='cards-token')
router.register('rate', RateServiceViewSet, basename='rate-me')

urlpatterns=[
    path('hours', ScheduleView.as_view({'get':'list'}), name="availablehours"),
    path("<int:id>/workinghours", WorkingHoursApiView.as_view(), name="workinghours"),
    path("<int:id>/availablehours", ShowAvailableHoursApiView.as_view(), name="availablehours"),
    path("<int:id>/reserve/", ReserveInstApiView.as_view(), name="reserve"),
    path('payment/<str:id>/', ProcessPaymentApiView.as_view(), name="process-payment")
]+router.urls


