import argparse
from typing import TypedDict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.etl.drivers import ITA_VESTIBULAR_PROVAS_FLOW


class ExtractionParams(TypedDict):
  headless: bool


def extraction(params: ExtractionParams):
  options = Options()

  if params["headless"]:
    options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)

  try:
    driver.get(ITA_VESTIBULAR_PROVAS_FLOW.url)
    ITA_VESTIBULAR_PROVAS_FLOW.navigate(driver)
  finally:
    driver.quit()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--no-headless",
    action="store_false",
    help="run Chrome with window visible",
  )
  args = parser.parse_args()
  extraction(ExtractionParams(headless=not args.no_headless))
