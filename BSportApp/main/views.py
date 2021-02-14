from django.shortcuts import render
from rest_framework import viewsets,generics
from .models import User,Appointment
from rest_framework.serializers import *
from .serializers import AppointmentSerializer,UserSerializer
from . import models
from rest_framework.response import Response
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from rest_framework.decorators import api_view
from django.views import View
from django.http import JsonResponse

dynamodb = boto3.resource('dynamodb',endpoint_url="http://host.docker.internal:8000/", region_name='us-west-2')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)




class DynamoDB(View):
    def get(self, request, *args, **kwargs):
        table = dynamodb.Table('Appointments')
        fields = "appointment_date, description, user_FK"
        # Expression Attribute Names for Projection Expression only.
        # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
        esk = None

        response = table.scan(
            ProjectionExpression=fields,
            )

        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))
            # or do something else, like items.append(i)

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ProjectionExpression=pe,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )

        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))
            # or do something else, like items.append(i)
            validated_response=(json.dumps(i, cls=DecimalEncoder))
            return JsonResponse(validated_response, safe=False)


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()



