from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role')
        model = User