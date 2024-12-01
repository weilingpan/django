import time

def process(task_name: str):
    print(f"Start process - {task_name} ...")
    for i in range(30):
        print(f"{task_name} - {i}")
        time.sleep(1)
    print(f"[{time.time()}]End process - {task_name}")