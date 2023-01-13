# pylint: disable=undefined-variable
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse

from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework import status, mixins
from .models import Poll, Choice, Vote, Customer
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, CustomerSerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'created_by': self.request.user.id,
                'question': self.request.data.get('question')}

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['GET'],  permission_classes=[IsAuthenticated])
    def my_poll(self, request):
        user_id = self.request.user.id
        myPoll = Poll.objects.filter(created_by_id=user_id)
        serializer = PollSerializer(myPoll, many=True)
        return Response(serializer.data)

class ChoiceViewSet(ModelViewSet):
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["poll_pk"])
        return queryset
    
    def get_serializer_context(self):
        return {'poll_pk': self.kwargs["poll_pk"],
                'user_id': self.request.user.id,
                'choice': self.request.data.get('choice')}

    
class VoteViewSet(CreateModelMixin,
                  GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    def get_serializer_context(self):
        return {'voted_by': self.request.user.id,
                'choice_id': self.request.data.get('choice'),
                'poll_id': self.request.data.get('poll')}
    

class CustomersViewSet(
                mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['GET'],  permission_classes=[IsAuthenticated])
    def me(self,request):
        customer = Customer.objects.get(
            user_id=self.request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
