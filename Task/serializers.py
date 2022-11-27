from .models import MyUser, Item
from .tasks import *
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import plaid
from uuid import uuid4
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'password']

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    login_token = serializers.CharField(required = False)

    def validate(self, data):
        """
        Get username and password from request, return error if 
        either empty or an incorrect combination is given
        """
        username = data.get('username', None)
        password = data.get('password', None)
        if not username or not password:
            raise ValidationError('Enter both username and password.')
        
        user = None
        try:
            user = MyUser.objects.get(username=username, password=password)
            if user.is_logged_in:
                raise ValidationError('User is already logged in.')
        except ObjectDoesNotExist:
            raise ValidationError('Incorrect username/password combination.')
        
        """
        Activate Logged in status, and assign a unique token
        update the user state in DB, the token is stored with the client
        """
        data['login_token'] = uuid4()
        user.login_token = data['login_token']
        user.is_logged_in = True
        user.save()
        return data

class LogoutUserSerializer(serializers.Serializer):
    login_token = serializers.CharField()
    auth_status = serializers.CharField(required = False)

    def validate(self, data):
        """
        We change is_logged_in to false and set access_token and token to an empty string ''
        Also to logout we will query the user using the token, we used which will be stored on the client
        """
        login_token = data.get("login_token", None)
        user = None
        try:
            user = MyUser.objects.get(login_token=login_token)
            if not user.is_logged_in:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError("Incorrect login_token")
        user.is_logged_in = False
        user.login_token = ""
        user.access_token = ""
        user.save()
        data['auth_status'] = "User is logged out!"
        return data

class ExchangeTokenSerializer(serializers.Serializer):
    login_token = serializers.CharField()
    public_token = serializers.CharField()
    access_token = serializers.CharField(required=False)

    def validate(self, data):
        # Check if both token and public token are passed
        login_token = None
        public_token = None
        try:
            login_token = data.get('login_token')
            public_token = data.get('public_token')
            if not login_token or not public_token:
                raise ValidationError('Please pass both login_token and public token.')
        except Exception as e:
            raise ValidationError(e)
        
        # Check if both login_token and public token are passed
        user = None
        try:
            user = MyUser.objects.get(login_token=login_token)
            if user.access_token:
                raise ValidationError('Access token already exists.')
        except ObjectDoesNotExist:
            raise ValidationError('login_token does not exist.')
        
        # Exchange public token for access token
        try:
            exchange_response = get_access_token.delay(public_token)
            exchange_response = exchange_response.get()
            Item.objects.create(user=user, item_id=exchange_response['item_id'], 
            access_token=exchange_response['access_token'])
            user.access_token = exchange_response['access_token']
            user.save()
        except Exception as e:
            raise ValidationError(e)
        exchange_response['login_token'] = login_token
        exchange_response['public_token'] = public_token
        return exchange_response

class GetAccountSerializer(serializers.Serializer):
    login_token = serializers.CharField()
    accounts = serializers.JSONField(required=False)

    def validate(self, data):
        try:
            login_token = data.get('login_token')
            if not login_token:
                raise ValidationError('Invalid Credentials.')
        except Exception as e:
            raise ValidationError(e)
        
        try:
            user = MyUser.objects.get(login_token=login_token)
            if not user.access_token:
                raise ValidationError('Access Token not found.')
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.')
        
        response = {}
        
        """
        Get the associated account of the access_token
        from celery
        """
        try:
            response = get_accounts.delay(user.access_token).get()
        except plaid.errors.PlaidError as e:
            raise ValidationError(e)
        response['login_token'] = login_token
        return response

class GetTransactionsSerializer(serializers.Serializer):
    login_token = serializers.CharField()
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")
    transactions = serializers.JSONField(required=False)

    def validate(self, data):
        login_token = data.get('login_token', None)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)

        """
        Type date is not JSON serializable
        """
        start_date = "{:%Y-%m-%d}".format(start_date)
        end_date = "{:%Y-%m-%d}".format(end_date)

        """
        Check if all details are passed
        """
        try:
            if not login_token or not start_date or not end_date:
                raise ValidationError('Provide login_token, start and end date.')
        except Exception as e:
            raise ValidationError(e)
        
        """
        Check if user exists
        """
        try:
            user = MyUser.objects.get(login_token=login_token)
            if not user.access_token:
                raise ValidationError('Access Token not found.')
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.')
        except Exception as e:
            raise ValidationError(e)
        
        """
        Invoke celery to get transactions
        of account with access_token token between the 
        particular dates
        """
        try:
            transactions = get_transactions.delay(user.access_token, start_date, end_date).get()
        except plaid.errors.PlaidError as e:
            raise ValidationError(e)
        response = {}
        response['login_token'] = login_token
        response['start_date'] = start_date
        response['end_date'] = end_date
        response['transactions'] = transactions.get('transactions')
        return response