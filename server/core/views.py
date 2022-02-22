import os
from time import time
import subprocess
from core import models, serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class HealthCheck(APIView):
    def get(self, _):
        workers = int(os.environ.get("workers"))
        data = {}
        for i in range(1, workers + 1):
            start_time = time()
            process = subprocess.Popen(f"timeout 1s curl http://worker{str(i)}:800{str(i)}/health_check/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            _, _ = process.communicate()
            end_time = time()
            time_elapsed = end_time-start_time
            if time_elapsed > 0.99:
                data[f"worker{str(i)}"] = "Error"
            else:
                data[f"worker{str(i)}"] = "OK"
        return Response(data=data,status=status.HTTP_200_OK)

class GetLanguages(APIView):
    def get(self, _):
        langs = models.Language.objects.all()
        data = serializers.LanguageSerializer(langs, many = True)
        return Response(data=data.data,status=status.HTTP_200_OK)


class ExecuteCode(APIView):
    def post(self, request):
        print(request.data)
        i = 1
        process = subprocess.Popen(f'timeout 1s curl -d "name=himanshu&pass=himanshu" http://worker{str(i)}:800{str(i)}/execute_code/', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        _, _ = process.communicate()
        return Response(status=status.HTTP_202_ACCEPTED)
