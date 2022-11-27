from .models import MyUser
from .tasks import get_transactions
from .serializers import *
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
import json

class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            MyUser.objects.create(username = request.data.get('username'), password = request.data.get('password'))
            return Response(serializer.data)

class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self, request):
        serializer = LogoutUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# Exhange public token with accesss token
class ExchangeToken(generics.GenericAPIView):
    serializer = ExchangeTokenSerializer

    def post(self, request):
        serializer = ExchangeTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# Get all account data for a user
class GetAccounts(generics.GenericAPIView):
    serializer = GetAccountSerializer

    def post(self, request):
        serializer = GetAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# # Get all transactions for a user between specified dates
class GetTransactions(generics.GenericAPIView):
    serializer = GetTransactionsSerializer

    def post(self, request):
        serializer = GetTransactionsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@csrf_exempt
def updateTransactionsWebhook(request):
    body_unicode = request.body.decode('utf-8')
    request_data = json.loads(body_unicode)
    
    webhook_type = request_data.get('webhook_type')
    webhook_code = request_data.get('webhook_code')
    if webhook_type == 'TRANSACTIONS':
        item_id = request_data.get('item_id')
        if webhook_code == 'TRANSACTIONS_REMOVED':
            removed_transactions = request_data.get('removed_transactions')
        else:
            new_transactions = request_data.get('new_transactions')            
            response = fetch_transactions.delay(request_data['item_id'], new_transactions).get()
    response['new_transactions'] = new_transactions
    # Writing to sample.json
    print(response)
    with open("sample.json", "w") as outfile:
        json.dump(response, outfile)
    return JsonResponse(response)
