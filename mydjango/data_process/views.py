from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import django_rq
from datetime import datetime

def trigger_task(request):
    queue = django_rq.get_queue('default')
    
    task_name = "my-first-task"
    queue.enqueue('data_process.tasks.process', task_name)
    return HttpResponse("Process task has been enqueued.")

def check_default_task(request, rq_id):
    print(f"check rq_id: {rq_id} ...")
    try:
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