from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Poll, Choice, Vote, Customer


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'choice', 'poll' , 'voted_by']
        read_only_fields = ['voted_by']

    def create(self, validated_data):
        choice_id = self.context['choice_id']
        poll_id = self.context['poll_id']
        voted_by_id = self.context['voted_by']
        
        poll = Poll.objects.get(pk=poll_id)
        choice = Choice.objects.get(pk=choice_id)
        try: 
            if poll.created_by_id == voted_by_id:
                raise PermissionDenied("You can not vote for your poll.")
            if poll.id != choice.poll_id:
                raise PermissionDenied("Sorry, you cannot select an option that is not associated with the question")             
            else:
                return Vote.objects.create(choice_id=choice_id, poll_id=poll_id, voted_by_id=voted_by_id,**validated_data)
        except IntegrityError:
                raise PermissionDenied("You can not vote twice.")


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice', 'poll']
        read_only_fields = ['poll']

    def create(self, validated_data):
        poll_pk = self.context['poll_pk']
        user_id = self.context['user_id']
        choice = self.context['choice']
        poll = Poll.objects.get(pk=poll_pk)
        choices_count = Choice.objects.filter(poll_id=poll_pk).count()

        if not user_id == poll.created_by_id:
            raise PermissionDenied("You can not create choice for this poll.")
        elif choices_count >= 4:
            raise PermissionDenied("You can not create more than 4 options.")
        else:
            return Choice.objects.create(poll_id=poll_pk,choice=choice)
        
        
class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'create_date']
        read_only_fields = ['created_by']
    
    def create(self, validated_data):
        created_by = self.context['created_by']
        question = self.context['question']

        poll_user = Poll.objects.filter(created_by_id=created_by)
        if poll_user.count() >= 5 :
            raise serializers.ValidationError('You cant add more than 5 questions')
        else:
            return Poll.objects.create(question=question, created_by_id=created_by)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email','phone']
