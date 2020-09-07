from django.urls import path
from .views import NewUser, ApiTransfer  # TransferView,
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [

    path('', ApiTransfer.as_view(), name='transfers'),
    path('obtain_token/', obtain_auth_token, name='obtain_token'),
    path('signup/', NewUser.as_view(), name='signup'),
]
