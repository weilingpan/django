from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import django_rq
from datetime import datetime
import rq

from data_process.models import Book

def trigger_task(request):
    queue = django_rq.get_queue('default')
    
    task_name = "my-first-task"
    queue.enqueue('data_process.tasks.process', task_name)
    return HttpResponse("Process task has been enqueued.")

def view_job_status(request):
    queue = django_rq.get_queue('default')
    started_registry = queue.started_job_registry
    deferred_registry = queue.deferred_job_registry
    failed_registry = queue.failed_job_registry
    finished_registry = queue.finished_job_registry
    scheduled_registry = queue.scheduled_job_registry

    return JsonResponse({
        "started_registry": {
            # "details": started_registry.__dict__,
            "count": started_registry.count,
            "job_ids": started_registry.get_job_ids(),
        },
        "deferred_registry": deferred_registry.count,
        "failed_registry": failed_registry.count,
        "finished_registry": finished_registry.count,
        "scheduled_registry": scheduled_registry.count,
    })

def get_job_status(request):
    queue = django_rq.get_queue('default')
    # Only failed jobs are not included in the list below.
    job_ids = set(queue.get_job_ids() +
        queue.started_job_registry.get_job_ids() +
        queue.finished_job_registry.get_job_ids() +
        queue.scheduled_job_registry.get_job_ids() +
        queue.deferred_job_registry.get_job_ids())
    print(f"job_ids = {job_ids}")
    rq_job_list = queue.job_class.fetch_many(job_ids, connection=queue.connection)
    print(f"rq_job_list = {rq_job_list}")

    for rq_job in rq_job_list:
        print(f"rq_job = {rq_job}")

        # {'connection': <redis.client.Redis(<redis.connection.ConnectionPool(<redis.connection.Connection(host=localhost,port=6379,db=0)>)>)>, 
        #  '_id': '234348ba-f13b-47b9-a290-bcff10426ef8', 
        #  'created_at': datetime.datetime(2024, 12, 1, 15, 10, 39, 161445), 
        #  '_data': b'\x80\x05\x956\x00\x00\x00\x00\x00\x00\x00(\x8c\x1adata_process.tasks.process\x94N\x8c\rmy-first-task\x94\x85\x94}\x94t\x94.', 
        #  '_func_name': <object object at 0x7f8a0e373190>, 
        #  '_instance': <object object at 0x7f8a0e373190>, 
        #  '_args': <object object at 0x7f8a0e373190>, 
        #  '_kwargs': <object object at 0x7f8a0e373190>, 
        #  '_success_callback_name': None,
        #  '_success_callback': <object object at 0x7f8a0e373190>, 
        #  '_failure_callback_name': None, 
        #  '_failure_callback': <object object at 0x7f8a0e373190>, 
        #  '_stopped_callback_name': None, 
        #  '_stopped_callback': <object object at 0x7f8a0e373190>, 
        #  'description': "data_process.tasks.process('my-first-task')", 
        #  'origin': 'default', 
        #  'enqueued_at': datetime.datetime(2024, 12, 1, 15, 10, 39, 166005), 
        #  'started_at': datetime.datetime(2024, 12, 1, 15, 10, 39, 554783), 
        #  'ended_at': None, '_result': None, '_exc_info': None, 'timeout': 360, '_success_callback_timeout': None, 
        #  '_failure_callback_timeout': None, '_stopped_callback_timeout': None, 'result_ttl': None, 'failure_ttl': None, 
        #  'ttl': None, 'worker_name': 'a9ee9316514a491f953670eb677ac509', '_status': 'started', '_dependency_ids': [],
        #    'meta': {}, 'serializer': <class 'rq.serializers.DefaultSerializer'>, 'retries_left': None, 
        #    'retry_intervals': None, 'redis_server_version': None, 
        #    'last_heartbeat': datetime.datetime(2024, 12, 1, 15, 10, 39, 554783), 
        #    'allow_dependency_failures': None, 'enqueue_at_front': None, '_cached_result': Non
    
    if rq_job_list:
        return JsonResponse({
            "data": [
                {
                    "job_id": _._id,
                    "description": _.description,
                    "status": _._status
                }
                for _ in rq_job_list
            ]}
        )
    else:
        return JsonResponse({"status": "not found"})


def check_default_task(request, rq_id):
    print(f"check rq_id: {rq_id} ...")
    try:
        # rq_job = rq.get_current_job()
        # print(f"here!!!!! {rq_job}")


        queue = django_rq.get_queue('default')
        rq_job = queue.fetch_job(rq_id)

        print(f"[{datetime.now()}] rq_job = {rq_job}")
        print(rq_job.get_status())
        print(f"is_queued = {rq_job.is_queued}")
        print(f"is_started = {rq_job.is_started}")
        print(f"is_finished = {rq_job.is_finished}")

        if rq_job is not None:
            if rq_job.is_queued or rq_job.is_started:
                return JsonResponse({"status": rq_job.get_status()})
            elif rq_job.is_finished:
                return JsonResponse({"status": rq_job.get_status()})
            else:
                return JsonResponse({"status": rq_job.get_status(), "stderr": rq_job.exc_info})
        else:
            return JsonResponse({"status": "unknown"})
    except Exception as ex:
        print("error occurred during checking repository request with rq id {}".format(rq_id))
        return HttpResponseBadRequest(str(ex))

# AbandonedJobError 是在使用 RQ (Redis Queue) 時出現的一個錯誤，通常是當某個工作（job）在隊列中被放置超過最大執行時間（timeout）或被放棄（abandoned）時，會拋出這個錯誤。

def check_default_progress(request, rq_id):
    queue = django_rq.get_queue('default')
    rq_job = queue.fetch_job(rq_id)

    # Fetch the progress from job's meta
    progress = rq_job.meta.get('progress', None)
    
    return JsonResponse({'progress': progress})

def add_book(request):
    book = Book.objects.create(
        title='GraphQL與Django入門',
        content='GraphQL是如何整合Django',
    )

    response_data = {
        "title": book.title,
        "content": book.content
    }
    return JsonResponse(response_data, status=201)