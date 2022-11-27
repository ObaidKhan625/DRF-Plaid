from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
app_name = 'Task'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('get-accounts/', GetAccounts.as_view(), name="get-accounts"),
    path('exchange-token/', ExchangeToken.as_view(), name="exchange-token"),
    path('get-transactions/', GetTransactions.as_view(), name="get-transactions"),
    path('update-transactions-webhook/', updateTransactionsWebhook, name="update-transactions"),
]
