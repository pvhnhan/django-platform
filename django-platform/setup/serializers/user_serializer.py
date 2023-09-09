from django import serializers
from infrastructure.entities.user import UserEntity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        fields = ('Id', 'FirstName', 'LastName', 'Username', 'Password', 'Email', 'Mobile', 'Avatar', 
                  'CreatedDate', 'CreatedBy', 'UpdatedDate', 'UpdatedBy')