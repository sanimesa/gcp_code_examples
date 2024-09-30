"""Example DAG using KubernetesPodOperator."""
import datetime

from airflow import models
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

with models.DAG(
    dag_id="composer_sample_kubernetes_pod",
    schedule_interval=None,
    start_date=YESTERDAY,
) as dag:
    kubernetes_min_pod = KubernetesPodOperator(
        task_id="pod-ex-minimum",
        name="pod-ex-minimum",
        cmds=["echo"],
        namespace="composer-user-workloads",
        image="gcr.io/gcp-runtimes/ubuntu_20_0_4",
        config_file="/home/airflow/composer_kube_config",
        kubernetes_conn_id="kubernetes_default",
    )

    kubernetes_min_pod
