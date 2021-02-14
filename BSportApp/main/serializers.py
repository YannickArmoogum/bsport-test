from rest_framework import serializers
from . import models
from django.db.models.signals import post_delete
from datetime import datetime
from rest_framework.serializers import(
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
import boto3
from django.dispatch import receiver
 
dynamodb = boto3.resource('dynamodb',endpoint_url="http://host.docker.internal:8000/", region_name='us-west-2')
table = dynamodb.Table('Appointments')

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='main:appointment-detail')
    user_FK = serializers.PrimaryKeyRelatedField(read_only=False,queryset=models.User.objects.all())
    class Meta:
        model = models.Appointment
        fields = [
            'url',
            'date',
            'description',
            'user_FK',
        ]
    def create(self, validated_data):
        objCreated = models.Appointment.objects.create(**validated_data)
        print('test',objCreated.user_FK.id,)
        dynamoData = {
            "id": objCreated.id,
            "appointment_date":validated_data['date'].strftime("%d/%m/%Y"),
            "description":validated_data['description'],
            "user_FK":objCreated.user_FK.id
        }
        table.put_item(
            Item=dynamoData
        )

        return models.Appointment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):

        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.user_FK = validated_data.get('user_FK', instance.user_FK)
        instance.save()
        print("user_FK",instance.user_FK.id)
        table.update_item(
            Key={
                'id': instance.id,
                'user_FK': instance.user_FK.id
            },
            UpdateExpression="set appointment_date=:d, description=:des, User_FK=:u",
            ExpressionAttributeValues={
                ':d': validated_data.get('date', instance.date).strftime("%d/%m/%Y"),
                ':des': validated_data.get('description', instance.description),
                ':u': validated_data.get('user_FK.id', instance.user_FK.id)
            },
            ReturnValues="UPDATED_NEW"
        )

        return instance

    @receiver(post_delete)
    def delete_obj(sender, instance, **kwargs):
        try:
            response = table.delete_item(
                Key={
                    'id': instance.id,
                    'user_FK': instance.user_FK.id
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise




##complete user info serializer###
class UserSerializer(serializers.ModelSerializer):
    appointments =  serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                 view_name='main:appointment-detail')
    url = serializers.HyperlinkedIdentityField(view_name='main:user-detail')
    class Meta:
        model = models.User
        fields = [
            'url',
            'id',
            'firstName',
            'lastName',
            'email',
            'dateJoined',
            'telephone',
            'appointments'
        ]


