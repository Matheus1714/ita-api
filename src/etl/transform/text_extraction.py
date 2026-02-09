import pymupdf

from src.etl.transform.constants import QUESTION_IN_TEXT_REGEX


def block_contains_question(text: str) -> bool:
  return bool(QUESTION_IN_TEXT_REGEX.search(text))


def get_text_in_rect(page, rect: pymupdf.Rect) -> str:
  return page.get_text(clip=rect, sort=True).strip()


def extract_question_texts(
  doc: pymupdf.Document,
  question_rects: dict[int, list[tuple[int, pymupdf.Rect]]],
) -> tuple[dict[int, str], dict[int, str]]:
  inside: dict[int, str] = {}
  outside: dict[int, str] = {}
  for num, clips in question_rects.items():
    inside_parts = []
    for page_no, clip in clips:
      page = doc[page_no]
      inside_parts.append(get_text_in_rect(page, clip))
    inside[num] = "\n\n".join(t for t in inside_parts if t)
    outside_parts = []
    for page_no, clip in clips:
      page = doc[page_no]
      blocks = page.get_text("blocks", clip=page.rect)
      for b in blocks:
        if len(b) < 5:
          continue
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        if not text.strip():
          continue
        if block_contains_question(text):
          continue
        block_rect = pymupdf.Rect(x0, y0, x1, y1)
        if not clip.intersects(block_rect):
          outside_parts.append(f"[Page {page_no + 1}]\n" + text.strip())
    outside[num] = "\n---\n".join(outside_parts) if outside_parts else ""
  return inside, outside
