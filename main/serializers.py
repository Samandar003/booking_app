from rest_framework.serializers import Serializer, ModelSerializer
from .models import InstitutionModel, ScheduleModel, WorkingHoursModel, PostInstitModel



class InstitutionModelSerializer(ModelSerializer):
    class Meta:
        model=InstitutionModel
        # fields='__all__'
        exclude=["likes", "dislikes"]
        
    def create(self, validated_data):
        return super().create(validated_data, owner=self.request.user)


class WorkingHoursSerializer(ModelSerializer):
    class Meta:
        model=WorkingHoursModel
        exclude = ["day", "open_time", "close_time", "institution"]
        