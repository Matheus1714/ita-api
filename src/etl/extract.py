import argparse
from pathlib import Path
from typing import TypedDict, Optional
import json
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.etl.drivers import ITA_VESTIBULAR_PROVAS_FLOW


class ExtractParams(TypedDict, total=False):
  headless: bool
  force_replace: bool


def _json_files_exist(output_dir: Path, n: int) -> bool:
  return all(
    (output_dir / f"{n - i}a_formato_prova_ita_vestibular.json").exists()
    for i in range(n)
  )


def _download_pdfs_from_jsons(output_dir: Path, n: int) -> None:
  provas_dir = output_dir / "provas"
  provas_dir.mkdir(parents=True, exist_ok=True)

  for i in range(n):
    filepath = output_dir / f"{n - i}a_formato_prova_ita_vestibular.json"
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
          filepath_pdf = provas_dir / f"prova_ita_vestibular_{year}_{col}.pdf"
          try:
            resp = requests.get(value, timeout=30, stream=True)
            resp.raise_for_status()
            filepath_pdf.write_bytes(resp.content)
          except requests.RequestException:
            pass

def _create_json_files(
  output_dir: Path,
  headless: bool,
) -> None:
  tables = ITA_VESTIBULAR_PROVAS_FLOW.tables
  n = len(tables)

  options = Options()
  if headless:
    options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)

  try:
    driver.get(ITA_VESTIBULAR_PROVAS_FLOW.url)
    ITA_VESTIBULAR_PROVAS_FLOW.navigate(driver)
    for i, table in enumerate(tables):
      data = table.get_data(driver)
      filename = f"{n - i}a_formato_prova_ita_vestibular.json"
      filepath = output_dir / filename
      with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
  finally:
    driver.quit()

def extract(params: Optional[ExtractParams] = None):
  params = params or {}
  headless = params.get("headless", True)
  force_replace = params.get("force_replace", False)

  output_dir = Path("data/vestibular")
  output_dir.mkdir(parents=True, exist_ok=True)

  tables = ITA_VESTIBULAR_PROVAS_FLOW.tables
  n = len(tables)
  json_exist = _json_files_exist(output_dir, n)

  if force_replace or not json_exist:
    _create_json_files(output_dir, headless)
  _download_pdfs_from_jsons(output_dir, n)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--no-headless",
    action="store_true",
    help="run Chrome with window visible",
  )
  parser.add_argument(
    "--force",
    action="store_true",
    default=False,
    help="regenerate JSON files from site even if they exist",
  )
  args = parser.parse_args()
  extract(ExtractParams(headless=not args.no_headless, force_replace=args.force))
