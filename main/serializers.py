from rest_framework.serializers import Serializer, ModelSerializer
from .models import InstitutionModel, ScheduleModel, WorkingHoursModel, PostInstitModel, CardTokensModel



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
        
        
class ScheduleModelSerializer(ModelSerializer):
    class Meta:
        model=ScheduleModel
        exclude = ['client']
        read_only_fields=['amount', 'status', 'reservation_details']
    
class CardTokensModelSerializer(ModelSerializer):
    class Meta:
        model = CardTokensModel
        fields="__all__"