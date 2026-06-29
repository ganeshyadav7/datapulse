"""Optional PySpark integration helpers."""

from app.schemas.spark_job import SparkJobCreate
from app.utils.time import utc_now


def run_sample_spark_job() -> SparkJobCreate:
    """Run a tiny PySpark job when PySpark is installed, otherwise return mock metrics."""
    started = utc_now()
    try:
        from pyspark.sql import SparkSession

        spark = (
            SparkSession.builder.appName("datapulse-sample-job").master("local[*]").getOrCreate()
        )
        rows = spark.range(0, 1000).repartition(4)
        input_records = rows.count()
        output_records = rows.where("id >= 0").count()
        partitions = rows.rdd.getNumPartitions()
        spark.stop()
        status = "success"
        error_message = None
    except Exception as exc:
        input_records = 1000
        output_records = 1000
        partitions = 4
        status = "success"
        error_message = f"PySpark unavailable; mock mode used: {exc.__class__.__name__}"
    ended = utc_now()
    return SparkJobCreate(
        job_name="datapulse_sample_spark_job",
        app_id=f"datapulse-{int(started.timestamp())}",
        status=status,
        start_time=started,
        end_time=ended,
        duration_seconds=(ended - started).total_seconds(),
        input_records=input_records,
        output_records=output_records,
        executor_count=1,
        memory_used_mb=512,
        partitions=partitions,
        error_message=error_message,
    )
