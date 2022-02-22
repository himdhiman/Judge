from celery import shared_task


@shared_task(bind=True)
def executeCode(self, context):
    print(self.id)
    print(context)
    print("Executing Code")
    return