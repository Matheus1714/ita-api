import pymupdf

from src.etl.transform.constants import (
  MARGIN_BOTTOM,
  MARGIN_LEFT,
  MARGIN_TOP,
  OBJECTIVE_BLOCK_END_MARGIN,
  OBJECTIVE_OPTION_LETTERS,
)


def _objective_block_bottom_y(page, clip: pymupdf.Rect, margin: float = OBJECTIVE_BLOCK_END_MARGIN) -> float | None:
  rects = []
  for letter in OBJECTIVE_OPTION_LETTERS:
    rects.extend(page.search_for(f"{letter} (", clip=clip))
    rects.extend(page.search_for(f"{letter} ( )", clip=clip))
  if not rects:
    return None
  return max(r.y1 for r in rects) + margin


def _clip_to_objective_block_end(page, clip: pymupdf.Rect) -> pymupdf.Rect:
  y1_options = _objective_block_bottom_y(page, clip)
  if y1_options is None or y1_options >= clip.y1:
    return clip
  return pymupdf.Rect(clip.x0, clip.y0, clip.x1, y1_options)


def build_question_rectangles(
  doc,
  positions: list[tuple[int, int, pymupdf.Rect]],
) -> dict[int, list[tuple[int, pymupdf.Rect]]]:
  if not positions:
    return {}
  x0_page = doc[0].rect.x0 + MARGIN_LEFT
  x1_page = doc[0].rect.x1
  questions: dict[int, list[tuple[int, pymupdf.Rect]]] = {}
  for i, (num, page_no, rect) in enumerate(positions):
    start_page = page_no
    start_y = rect.y0 - MARGIN_TOP
    if i + 1 < len(positions):
      _next_num, next_page, next_rect = positions[i + 1]
      end_page = next_page
      end_y = next_rect.y0 - MARGIN_BOTTOM
    else:
      end_page = start_page
      end_y = doc[start_page].rect.y1
    if start_page == end_page:
      clip = pymupdf.Rect(x0_page, start_y, x1_page, end_y)
      clip = _clip_to_objective_block_end(doc[start_page], clip)
      questions[num] = [(start_page, clip)]
    else:
      questions[num] = []
      pr = doc[start_page].rect
      questions[num].append((start_page, pymupdf.Rect(x0_page, start_y, x1_page, pr.y1)))
      for p in range(start_page + 1, end_page):
        pr = doc[p].rect
        questions[num].append((p, pymupdf.Rect(x0_page, pr.y0, x1_page, pr.y1)))
      pr = doc[end_page].rect
      clip_last = pymupdf.Rect(x0_page, pr.y0, x1_page, end_y)
      clip_last = _clip_to_objective_block_end(doc[end_page], clip_last)
      questions[num].append((end_page, clip_last))
  return questions
