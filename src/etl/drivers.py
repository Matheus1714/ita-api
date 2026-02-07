from typing import Optional, List
from dataclasses import dataclass, field

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.etl.constants import PROVAS_ITA_VESTIBULAR_URL

@dataclass
class SeleniumElement:
  name: Optional[str] = None
  identifier: str = ""
  identifier_type: By = By.XPATH
  tag: Optional[str] = None

  def get(self, driver: WebDriver) -> WebElement:
    return driver.find_element(self.identifier_type, self.identifier)

  def get_all(self, driver: WebDriver) -> List[WebElement]:
    return driver.find_elements(self.identifier_type, self.identifier)
  
  def click(self, driver: WebDriver) -> None:
    self.get(driver).click()
  
  def send_keys(self, driver: WebDriver, keys: str) -> None:
    self.get(driver).send_keys(keys)

@dataclass
class SeleniumElementWithIframes(SeleniumElement):
  iframes: List[SeleniumElement] = field(default_factory=list)

  def set_iframes(self, driver: WebDriver) -> None:
    for iframe in self.iframes:
      driver.switch_to.frame(iframe.get(driver))

@dataclass
class SeleniumTable(SeleniumElement):
  ...

@dataclass
class ITAProvasFlow:
  url: str
  navigation_steps: List[SeleniumElement | SeleniumElementWithIframes]
  # tables: SeleniumTable | List[SeleniumTable]

  def navigate(self, driver: WebDriver) -> None:
    for step in self.navigation_steps:
      step.get(driver).click()
      if isinstance(step, SeleniumElementWithIframes):
        step.set_iframes(driver)
      if isinstance(step, SeleniumTable):
        step.get(driver).click()
      if isinstance(step, SeleniumElement):
        step.get(driver).click()

ITA_VESTIBULAR_PROVAS_FLOW = ITAProvasFlow(
  url=PROVAS_ITA_VESTIBULAR_URL,
  navigation_steps=[
    SeleniumElementWithIframes(
      identifier="//a[@href='provas.htm' and @target='mainFrame']",
      tag="a",
      iframes=[
        SeleniumElement(
          identifier="//frame[@name='mainFrame']",
          tag="iframe"
        ),
      ]
    )
  ]
)