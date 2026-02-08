from pathlib import Path

def json_files_exist(
  *,
  output_dir: Path,
  n: int,
  json_prefix: str,
) -> bool:
  return all(
    (output_dir / f"{n - i}{json_prefix}").exists()
    for i in range(n)
  )
