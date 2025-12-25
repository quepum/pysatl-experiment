### Parallel Execution

To accelerate resource-intensive experiments (`power`, `critical_value`), you can enable parallel execution by specifying the number of worker processes.

> ⚠️ **Important**: Parallel mode is **not recommended** for `time_complexity` experiments, as concurrent execution distorts real execution time measurements and violates methodological correctness.

#### Enable parallel mode

Set the `parallel-workers` parameter to the desired number of processes (typically equal to or less than the number of logical CPU cores on your machine):

```shell
poetry run experiment configure NAME parallel-workers 8