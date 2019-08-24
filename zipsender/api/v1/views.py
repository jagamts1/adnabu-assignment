from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InputSerializer
from zipsender.tasks import (
    send_to_mail,
)


class ZipSender(APIView):

    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            send_to_mail.delay(data=data)
            return Response({"data": serializer.data, "message": "data send to given email id."}, status=status.HTTP_200_OK)
        return Response({"data": serializer.errors, "message": "missing field"}, status=status.HTTP_400_BAD_REQUEST)
