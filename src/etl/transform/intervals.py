from __future__ import annotations

import pymupdf


def question_intervals_on_page(
  question_rects: dict[int, list[tuple[int, pymupdf.Rect]]],
  page_no: int,
) -> list[tuple[float, float]]:
  out = []
  for _num, clips in question_rects.items():
    for pn, clip in clips:
      if pn == page_no:
        out.append((clip.y0, clip.y1))
        break
  return sorted(out, key=lambda x: x[0])


def merge_intervals(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
  if not intervals:
    return []
  out = [list(intervals[0])]
  for a, b in intervals[1:]:
    if a <= out[-1][1]:
      out[-1][1] = max(out[-1][1], b)
    else:
      out.append([a, b])
  return [(x[0], x[1]) for x in out]


def non_question_intervals_on_page(
  question_rects: dict[int, list[tuple[int, pymupdf.Rect]]],
  page_no: int,
  page_rect: pymupdf.Rect,
) -> list[tuple[float, float]]:
  q_intervals = question_intervals_on_page(question_rects, page_no)
  merged = merge_intervals(q_intervals)
  y0_page, y1_page = page_rect.y0, page_rect.y1
  out = []
  current = y0_page
  for a, b in merged:
    if current < a - 1:
      out.append((current, a))
    current = max(current, b)
  if current < y1_page - 1:
    out.append((current, y1_page))
  return out
