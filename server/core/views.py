import os
import json
from time import time
import subprocess
from django.conf import settings
from core import models, serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

WORKERS = int(settings.WORKERS)

class HealthCheck(APIView):
    def get(self, _):
        data = {}
        for i in range(1, WORKERS + 1):
            start_time = time()
            process = subprocess.Popen(
                f"timeout 1s curl http://worker{str(i)}:800{str(i)}/health_check/",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            _, _ = process.communicate()
            end_time = time()
            time_elapsed = end_time - start_time
            if time_elapsed > 0.99:
                data[f"worker{str(i)}"] = "Error"
            else:
                data[f"worker{str(i)}"] = "OK"
        return Response(data=data, status=status.HTTP_200_OK)


class GetLanguages(APIView):
    def get(self, _):
        langs = models.Language.objects.all()
        data = serializers.LanguageSerializer(langs, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)


class ExecuteCode(APIView):
    def post(self, request):
        WORKER_ID = None
        with open("/app/core/context.json", "r") as jsonFile:
            data = json.load(jsonFile)
            WORKER_ID = data["worker_id"]
        obj = models.Submission.objects.create(**request.data)
        process = subprocess.Popen(
            f'timeout 1s curl -d "id={str(obj.task_id)}" http://worker{str(WORKER_ID)}:800{str(WORKER_ID)}/execute_code/',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        _, _ = process.communicate()
        ret_data = {"id": obj.task_id}
        print(WORKER_ID)
        WORKER_ID = WORKER_ID + 1
        if WORKER_ID > WORKERS:
            WORKER_ID = 1
        
        data["worker_id"] = WORKER_ID

        with open("/app/core/context.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        return Response(data=ret_data, status=status.HTTP_202_ACCEPTED)

class GetResult(APIView):
    def get(slef, _, task_id):
        try:
            obj = models.Submission.objects.filter(task_id = task_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if len(obj) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializers.SubmissionSerializer(obj.first())
        return Response(data=data.data,status=status.HTTP_200_OK)

