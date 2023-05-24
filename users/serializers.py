from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from .utils import validate_email_address, AuthenticationFailed, get_username
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email')
     

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if validate_email_address(attrs["email"]) is False:
            raise serializers.ValidationError("Enter a Valid Email Address.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=get_username(validated_data["email"])
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    default_error_message = {
        "no_active_account":_('No active account found with the given credentials'),
    }
    username_field = get_user_model().EMAIL_FIELD
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password":attrs["password"]
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError as k:
            pass
        self.user  = authenticate(**authenticate_kwargs)
        if not self.user:
            raise AuthenticationFailed(
                self.default_error_message["no_active_account"],
                "no_active_account"
            )
        else:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['id'] = self.user.id
            data['email'] = self.user.email
            return data