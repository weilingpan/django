from django.http import HttpResponse
import django_rq

def trigger_task(request):
    queue = django_rq.get_queue('default')
    
    task_name = "my-first-task"
    queue.enqueue('data_process.tasks.process', task_name)
    return HttpResponse("Process task has been enqueued.")