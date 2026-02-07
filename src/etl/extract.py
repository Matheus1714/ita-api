import argparse
from typing import TypedDict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.etl.drivers import ITA_VESTIBULAR_PROVAS_FLOW, EXEMPLO_COM_TABELA


class ExtractParams(TypedDict):
  headless: bool = True


def extract(params: Optional[ExtractParams] = None):
  options = Options()

  if params["headless"]:
    options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)

  try:
    driver.get(EXEMPLO_COM_TABELA.url)
    EXEMPLO_COM_TABELA.navigate(driver)
    data = EXEMPLO_COM_TABELA.tables.get_data(driver)
    print(data)
  finally:
    driver.quit()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--no-headless",
    action="store_true",
    help="run Chrome with window visible",
  )
  args = parser.parse_args()
  extract(ExtractParams(headless=not args.no_headless))
