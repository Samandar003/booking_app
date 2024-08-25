from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework import status
from .serializers import InstitutionModelSerializer, WorkingHoursSerializer, ScheduleModelSerializer
from .models import InstitutionModel, PostInstitModel, WorkingHoursModel, ScheduleModel, CardTokensModel
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import service
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import NotFound
from datetime import date, timedelta
import stripe

class InstitutionAllViewSet(ViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    queryset=InstitutionModel.objects.all()
    
    def create(self, request):
        serializer=InstitutionModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def list(self, request):
        queryset=self.queryset.order_by("-dislikes")
        queryset=queryset.order_by("likes")    
        serializer=InstitutionModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        obj=get_object_or_404(self.queryset, pk=pk)
        serializer=InstitutionModelSerializer(obj)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        instance=self.queryset.get(pk=kwargs.get('pk'))
        serializer=InstitutionModelSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ScheduleView(ViewSet):
    def list(self, request):
        inst_obj=InstitutionModel.objects.all().first()
        response=service.show_available_hours(instit_obj=inst_obj, day="sunday")
        return Response({"response":response})

    def retrieve(self, request, pk=None):
        queryset=ScheduleModel.objects.all()

class WorkingHoursApiView(APIView):
    def get(self, request, id=None):
        if id is None:
            return Response({"error": "Home ID is required."}, status=400)
        query=WorkingHoursModel.objects.filter(institution=id)
        serializer = WorkingHoursSerializer(query, many=True)
        return Response(serializer.data)
    
DAY_MAPPING = {
    0: 'monday',
    1: 'tuesday',
    2: 'wednesday',
    3: 'thursday',
    4: 'friday',
    5: 'saturday',
    6: 'sunday',
}

class ShowAvailableHoursApiView(APIView):
    def get(self, request, id=None):
        if id is None:
            return Response({"error": "Home ID is required."}, status=400)
        day = request.query_params.get('day', None)
        if not day:  
            today = date.today()
            today_weekday = today.weekday()
            day=DAY_MAPPING[today_weekday]
        inst_obj=InstitutionModel.objects.get(id=id)
        result=service.show_available_hours(instit_obj=inst_obj, day=day)
        return Response({'res':result, "day":day})
    
class ReserveInstApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # insit=get_object_or_404(InstitutionModel, pk)
        serializer=ScheduleModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_t=serializer.validated_data.get("start_time")
        end_t=serializer.validated_data.get("end_time")
        inst=serializer.validated_data.get('institution')
        duration = end_t - start_t
        min_duration = timedelta(minutes=30)
        max_duration = timedelta(hours=4)
        if not min_duration <= duration <= max_duration:
            return Response({'ms':"At least 30 mins, at most 4 hours"}, status=status.HTTP_403_FORBIDDEN)
        cost_service=service.calculate_perhour(inst, duration)
        tru_fal=service.check_time_conflict(start_t, end_t, day=serializer.validated_data.get("day"), inst=inst)
        if tru_fal:
            serializer.save(client=request.user, amount=cost_service, status="pending")
            return Response(serializer.data)    
        return Response({'ms':"time conflict, reserve at different time"}, status=status.HTTP_403_FORBIDDEN)
    

class ProcessPaymentApiView(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        try:
            card = CardTokensModel.objects.get(user=request.user)
        except:
            return Response({'ms':"you have to save your card first"}, status=status.HTTP_403_FORBIDDEN)
        
        reservation_id=kwargs.get('id')
        reservation = ScheduleModel.objects.get(id=reservation_id, client=request.user)
        if reservation.status == 'paid':
            return Response({'error': 'Reservation is already paid.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            charge = stripe.Charge.create(
                amount=int(reservation.amount * 100),  # amount in cents
                currency='usd',
                description=f'Reservation {reservation_id} payment',
                source=request.data['stripeToken'],
            )
            
            # Update reservation status
            reservation.status = 'paid'
            reservation.save()

            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
