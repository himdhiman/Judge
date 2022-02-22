from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from core import tasks


class HealthCheck(APIView):
    def get(self, _):
        return Response(status=status.HTTP_200_OK)

class ExecuteCode(APIView):
    def post(selg, request):
        print(request.data)
        tasks.executeCode.delay(request.data)
        return Response(status=status.HTTP_200_OK)