from rest_framework import serializers
from RestApp.models import TaskModel
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

#serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=User.Roles.choices, default=User.Roles.OTHER)

    class Meta:
        model  = User
        fields = ('id', 'username', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            role = validated_data['role']
        )
        return user
#serializer for user login
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role 
        return token

#serializer for task model
class TaskModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaskModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    #validate if title is not empty | we can also use validate_title for particular field validation
    def validate(self, data):
        if(len(data.get('title')) == 0):
            raise serializers.validationError("Title is Empty")
        else:
            return data