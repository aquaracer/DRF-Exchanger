from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.db.transaction import atomic

from .models import Transfers
from .serializers import AddTransferSerializer, TransfersSerializer, UserSerializer
from .service import TransferFunds

class NewUser(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ((IsAdminUser,))


class ApiTransfer(APIView):
    permission_classes = ((IsAuthenticated,))

    def get(self, request):
        transfers = Transfers.objects.filter(account_id=request.user.id)
        serializer = TransfersSerializer(transfers, many=True)
        return Response(serializer.data)

    @atomic()
    def post(self, request):
        serializer = AddTransferSerializer(data=request.data)
        if serializer.is_valid():
            new_status = TransferFunds(request.user.username, request.data)
            return Response(status=new_status)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
