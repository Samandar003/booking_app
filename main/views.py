from rest_framework.viewsets import ModelViewSet
from serializers import InstitutionModelSerializer
from models import InstitutionModel, PostInstitModel, WorkingHoursModel, ScheduleModel

class InstitutionAllModelViewSet(ModelViewSet):
    serializer_class=InstitutionModelSerializer
    
    def get_queryset(self):
        queryset=InstitutionModel.objects.all().order_by("-dislikes")
        queryset=queryset.order_by("likes")
        
        

