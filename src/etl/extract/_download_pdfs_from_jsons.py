from pathlib import Path
import json
import requests


def download_pdfs_from_jsons(
  *,
  output_dir: Path,
  n: int,
  json_prefix: str,
  pdf_filename_prefix: str = "prova_ita_vestibular",
) -> None:
  provas_dir = output_dir / "provas"
  provas_dir.mkdir(parents=True, exist_ok=True)

  for i in range(n):
    filepath = output_dir / f"{n - i}{json_prefix}"
    if not filepath.exists():
      continue
    with open(filepath, encoding="utf-8") as f:
      data = json.load(f)
    for row in data:
      items = list(row.items())
      if not items:
        continue
      year = items[0][1]
      for col, value in items[1:]:
        if isinstance(value, str) and value.startswith("http"):
          filepath_pdf = provas_dir / f"{pdf_filename_prefix}_{year}_{col}.pdf"
          try:
            resp = requests.get(value, timeout=30, stream=True)
            resp.raise_for_status()
            filepath_pdf.write_bytes(resp.content)
          except requests.RequestException:
            pass
