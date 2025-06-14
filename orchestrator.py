from prefect import flow, task

@task
def run_batch(year: int, month: int):
    from batch import run
    output_file, mean = run(year, month)
    print(f"Output saved: {output_file}")
    print(f"Mean predicted duration: {mean:.2f}")
    return output_file

@flow
def taxi_duration_pipeline(year: int = 2023, month: int = 4):
    run_batch(year, month)

# DO NOT call .deploy() here anymore
if __name__ == "__main__":
    taxi_duration_pipeline(year=2023, month=4)
