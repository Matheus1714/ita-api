from src.etl.transform.constants import (
  DRAFT_PAGE_MAX_TEXT_LEN,
  QUESTION_IN_TEXT_REGEX,
)


def page_has_question(page) -> bool:
  text = page.get_text()
  return bool(QUESTION_IN_TEXT_REGEX.search(text))


def is_draft_page(page) -> bool:
  text = page.get_text().strip()
  if "rascunho" not in text.lower():
    return False
  return len(text) < DRAFT_PAGE_MAX_TEXT_LEN


def is_essay_page(page) -> bool:
  text = page.get_text()
  text_lower = text.lower()
  if page_has_question(page):
    return False
  if is_draft_page(page):
    return False
  if "redação" in text_lower or "redacao" in text_lower:
    return True
  if "questão" not in text_lower and "questao" not in text_lower:
    return True
  return False
