import subprocess
import csv
import time
import sys
import os
import sqlite3
from pathlib import Path

CONFIG_NAME = "critical_value_speed_measure"  # имя эксперимента
PARALLEL_WORKERS = 4
N_RUNS = 30
DB_PATH = "C:\\Users\\\u0410\u043b\u0438\u043d\u0430\\PycharmProjects\\pysatl-experiment2\\.storage\\power.sqlite"  # путь из storage_connection
CSV_OUTPUT = f"results/critical_value_speed.csv"
# ---------------------------------------------------------

Path("results").mkdir(exist_ok=True)

def get_experiment_id(db_path: str) -> int:
    """Получает ID последнего эксперимента из БД."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM experiments ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise RuntimeError("No experiment found in DB")
    return row[0]

def delete_experiment_by_id(db_path: str, exp_id: int):
    """Удаляет эксперимент и связанные данные (по ID)."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Теперь удаляем сам эксперимент
    cur.execute("DELETE FROM experiments WHERE id = ?", (exp_id,))
    conn.commit()
    conn.close()

def run_single() -> float:
    """Запускает эксперимент и возвращает время в секундах."""
    start = time.time()
    try:
        env = os.environ.copy()
        subprocess.run(
            ["poetry", "run", "experiment", "build-and-run", CONFIG_NAME],
            check=True,
            capture_output=True,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        print("❌ Run failed:", e.stderr.decode())
        return -1.0
    end = time.time()
    return end - start

def main():
    print(f"Starting {N_RUNS} runs for parallel_workers={PARALLEL_WORKERS}...")
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["run_id", "4_duration_sec"])

        for i in range(1, N_RUNS + 1):
            print(f"  Run {i}/{N_RUNS}...", end=" ")
            duration = run_single()
            if duration < 0:
                exp_id = -1
                print("FAILED")
            else:
                try:
                    exp_id = get_experiment_id(DB_PATH)
                    delete_experiment_by_id(DB_PATH, exp_id)
                    print(f"OK (id={exp_id})")
                except Exception as e:
                    print(f"Cleanup failed: {e}")
                    exp_id = -1

            writer.writerow([i, duration])
            f.flush()

    print(f"✅ Results saved to {CSV_OUTPUT}")

if __name__ == "__main__":
    main()