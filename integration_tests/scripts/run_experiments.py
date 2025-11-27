import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pysatl_experiment.cli.commands.build_and_run.build_and_run import build_and_run


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    exp_name = sys.argv[1]
    start = time.perf_counter()
    try:
        build_and_run(exp_name)
        status = "SUCCESS"
    except Exception as e:
        status = f"FAILED: {e}"
    end = time.perf_counter()

    results_file = Path("integration-tests/results/results.csv")
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(f"{exp_name},{status},{end - start:.3f}\n")

    print(f"\n{exp_name}: {status} in {end - start:.3f} seconds\n")


if __name__ == "__main__":
    main()