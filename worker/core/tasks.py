import os
import urllib3
import subprocess
import base64
from django.conf import settings
from celery import shared_task
from core.models import Submission

http = urllib3.PoolManager()
BASE_URL = settings.BASE_URL


def decode_data(base64_message):
    return base64.b64decode(base64_message).decode("utf-8")


def encode_data(message):
    return base64.b64encode(message.encode("utf-8"))


def create_directories(id, lang, code):
    os.system(f"mkdir temp/{id}")
    code = decode_data(code)
    ext = ""
    if lang == "Python":
        ext = ".py"
    else:
        ext = ".cpp"
    os.system(f"touch temp/{id}/main{ext}")
    os.system(f"chmod +x temp/{id}/main{ext}")
    code_file = open(f"temp/{id}/main{ext}", "w")
    code_file.write(code)
    code_file.close()
    return


def delete_directories(id):
    os.system(f"rm -rf temp/{id}")
    return


def compile_code(id):
    print("called")
    out = subprocess.getoutput(f"g++ temp/{id}/main.cpp -o temp/{id}/main.out")
    flag = True
    data = ""
    if out != "":
        flag = False
        data = encode_data(out)
    return [flag, data]


@shared_task(bind=True)
def executeCode(_, context):
    submission_object = Submission.objects.get(task_id=context["id"])
    submission_object.status = "Running"
    submission_object.save()
    print("Executing Code")
    totaltc = submission_object.total_Test_Cases
    probId = submission_object.problem_id
    lang = submission_object.language.name
    code = submission_object.code
    counter = 0

    create_directories(context["id"], lang, code)
    ext = ".py"
    run_cmd = ["python3", f'temp/{context["id"]}/main.py']
    if lang == "CPP":
        ext = ".cpp"
        flag, data = compile_code(context["id"])
        run_cmd = [f'temp/{context["id"]}/main.out']
        if not flag:
            submission_object.stderr = data
            submission_object.status = "Compilation Error"
            submission_object.test_Cases_Passed = counter
            submission_object.score = (
                int((counter / totaltc)) * submission_object.total_score
            )
            submission_object.save()
            delete_directories(context["id"])
            return

    for i in range(1, totaltc + 1):
        input_target_url = BASE_URL + str(probId) + "/" + f"tc-input{str(i)}.txt"
        input_response = http.request("GET", input_target_url)
        input_data = input_response.data.decode("utf-8")
        process = subprocess.Popen(
            run_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            stdout, stderr = process.communicate(input=input_data.encode(), timeout=2)
        except subprocess.TimeoutExpired as e:
            process.kill()
            submission_object.stderr = encode_data(f"TLE on Test Case {i}")
            submission_object.status = "Time Limited Exceeded"
            submission_object.test_Cases_Passed = counter
            submission_object.score = (
                int((counter / totaltc)) * submission_object.total_score
            )
            submission_object.save()
            delete_directories(context["id"])
            return
        if stderr.decode() != "":
            submission_object.stderr = encode_data(stderr.decode())
            submission_object.status = "Runtime Error"
            submission_object.test_Cases_Passed = counter
            submission_object.score = (
                int((counter / totaltc)) * submission_object.total_score
            )
            submission_object.save()
            delete_directories(context["id"])
            return
        stdout = stdout.decode()
        stdout = stdout.strip()
        output_target_url = BASE_URL + str(probId) + "/" + f"tc-output{str(i)}.txt"
        output_response = http.request("GET", output_target_url)
        output_data = output_response.data.decode("utf-8")
        output_data = output_data.strip()
        if output_data == stdout:
            counter += 1
        else:
            submission_object.stderr = encode_data(f"WA on Test Case {i}")
            submission_object.status = "Wrong Answer"
            submission_object.test_Cases_Passed = counter
            submission_object.score = (
                int((counter / totaltc)) * submission_object.total_score
            )
            submission_object.save()
            delete_directories(context["id"])
            return
    submission_object.stderr = encode_data("None")
    submission_object.status = "Accepted"
    submission_object.test_Cases_Passed = counter
    submission_object.score = int((counter / totaltc)) * submission_object.total_score
    submission_object.save()
    delete_directories(context["id"])
    return
