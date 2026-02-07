from typing import Optional, List, Any
from dataclasses import dataclass, field

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class BaseElement:
  name: Optional[str] = None
  identifier: str = ""
  identifier_type: By = By.XPATH
  tag: Optional[str] = None

  def find(self, ctx) -> WebElement:
    return ctx.find_element(self.identifier_type, self.identifier)

  def find_all(self, ctx) -> List[WebElement]:
    return ctx.find_elements(self.identifier_type, self.identifier)

  def click(self, ctx) -> None:
    self.find(ctx).click()

  def send_keys(self, ctx, keys: str) -> None:
    self.find(ctx).send_keys(keys)


@dataclass
class SeleniumElement(BaseElement):
  element: BaseElement = None
  iframes: List[BaseElement] = field(default_factory=list)

  def _resolve_context(self, driver: WebDriver):
    driver.switch_to.default_content()

    for iframe in self.iframes:
      driver.switch_to.frame(iframe.find(driver))

    return driver

  def find(self, driver: WebDriver) -> WebElement:
    context = self._resolve_context(driver)
    return self.element.find(context)

  def click(self, driver: WebDriver) -> None:
    try:
      self.find(driver).click()
    except:
      element = self.find(driver)
      driver.execute_script("arguments[0].click()", element)

  def send_keys(self, driver: WebDriver, keys: str) -> None:
    self.find(driver).send_keys(keys)


@dataclass
class SeleniumTableRow(SeleniumElement):
  item: SeleniumElement = None


@dataclass
class SeleniumTable(SeleniumElement):
  row: SeleniumTableRow = None

  def get_data(self, driver: WebDriver) -> List[List[str]]:
    data = []
    element = self.find(driver)
    rows = self.row.element.find_all(element)
    for row in rows:
      items = self.row.item.element.find_all(row)
      data.append([item.text for item in items])
    return data


@dataclass
class ITAProvasFlow:
  url: str
  navigation_steps: List[SeleniumElement] = field(default_factory=list)
  tables: SeleniumTable | List[SeleniumTable] = None

  def navigate(self, driver: WebDriver) -> None:
    for step in self.navigation_steps:
      step.click(driver)
