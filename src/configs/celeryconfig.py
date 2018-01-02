BROKER_URL='pyamqp://localhost'
# CELERY_ROUTES = ('router.MyRouter',)
# CELERY_QUEUES = (
#   Queue('tasks.execute_client', Exchange('celery'), routing_key='tasks.execute_client'),
#   Queue('tasks.log_processing', Exchange('celery'), routing_key='tasks.log_processing'),
# )

CELERY_ROUTES = {"tasks.execute_client": {"queue" : "ssh"},
                "tasks.log_processing" : {"queue" : "log"},
                "tasks.send_email" : {"queue" : "email"}
                }
