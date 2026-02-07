from src.etl.constants import PROVAS_ITA_VESTIBULAR_URL
from src.utils.selenium_elements import (
  BaseElement,
  SeleniumElement,
  ITAProvasFlow,
  SeleniumTable,
  SeleniumTableRow,
)

ITA_VESTIBULAR_PROVAS_FLOW = ITAProvasFlow(
  url=PROVAS_ITA_VESTIBULAR_URL,
  navigation_steps=[
    SeleniumElement(
      element=BaseElement(
        identifier="//a[@href='provas.htm' and @target='mainFrame']",
        tag="a",
      ),
      iframes=[
        BaseElement(identifier="//frame[@name='topFrame']", tag="frame"),
      ],
    ),
  ],
  tables=[
    SeleniumTable(
      element=BaseElement(
        identifier="(//table[@width='750']//table[@width='80%'])[1]",
        tag="table",
      ),
      row=SeleniumTableRow(
        element=BaseElement(
          identifier=".//tr",
          tag="tr",
        ),
        item=SeleniumElement(
          element=BaseElement(
            identifier=".//td",
            tag="td",
          ),
        ),
        skip_first=True,
      ),
      headers=['year', 'prova_1f', 'answer_key_1f', 'matematica', 'fisica', 'quimica', 'portugues', 'answer_key_2f'],
      iframes=[
        BaseElement(identifier="//frame[@name='mainFrame']", tag="iframe"),
      ],
    ),
    SeleniumTable(
      element=BaseElement(
        identifier="(//table[@width='750']//table[@width='80%'])[2]",
        tag="table",
      ),
      row=SeleniumTableRow(
        element=BaseElement(
          identifier=".//tr",
          tag="tr",
        ),
        item=SeleniumElement(
          element=BaseElement(
            identifier=".//td",
            tag="td",
          ),
        ),
        skip_first=True,
      ),
      headers=['year', 'prova_1f', 'answer_key_1f', 'matematica', 'fisica', 'quimica', 'redacao'],
      iframes=[
        BaseElement(identifier="//frame[@name='mainFrame']", tag="iframe"),
      ],
    ),
    SeleniumTable(
      element=BaseElement(
        identifier="(//table[@width='750']//table[@width='80%'])[3]",
        tag="table",
      ),
      row=SeleniumTableRow(
        element=BaseElement(
          identifier=".//tr",
          tag="tr",
        ),
        item=SeleniumElement(
          element=BaseElement(
            identifier=".//td",
            tag="td",
          ),
        ),
        skip_first=True,
      ),
      headers=['fisica', 'portugues', 'ingles', 'matematica', 'quimica', 'answer_key'],
      iframes=[
        BaseElement(identifier="//frame[@name='mainFrame']", tag="iframe"),
      ],
    ),
  ],
)

EXEMPLO_COM_TABELA = ITAProvasFlow(
  url="https://getbootstrap.com/",
  navigation_steps=[
    SeleniumElement(
      element=BaseElement(
        identifier="//*[@id='bdNavbar']/div[2]/ul[1]/li[1]/a",
        tag="a",
      ),
    ),
    SeleniumElement(
      element=BaseElement(
        identifier="//*[@id='bd-docs-nav']/ul/li[4]/ul/li[4]/a",
        tag="a",
      ),
    ),
  ],
  tables=SeleniumTable(
    element=BaseElement(
      identifier="/html/body/div[2]/main/div[3]/div[1]/div/table/tbody",
      tag="table",
    ),
    row=SeleniumTableRow(
      element=BaseElement(
        identifier=".//tr",
        tag="tr",
      ),
      item=SeleniumElement(
        element=BaseElement(
          identifier=".//td",
          tag="td",
        ),
      ),
    ),
  ),
)
