from pathlib import Path

import pymupdf

from src.etl.transform.constants import MAX_QUESTIONS
from src.etl.transform.export_text import save_question_text_files
from src.etl.transform.images import (
  export_non_question_figures,
  export_question_figures,
  export_question_regions_pdf,
)
from src.etl.transform.positions import find_question_positions
from src.etl.transform.rectangles import build_question_rectangles
from src.etl.transform.text_extraction import extract_question_texts


def run_transform(
  doc: pymupdf.Document,
  *,
  max_questions: int = MAX_QUESTIONS,
  export_question_images: bool = True,
  export_non_question_images: bool = True,
  export_texts: bool = True,
  export_regions_pdf: bool = True,
  questions_figs_dir: Path | None = None,
  non_questions_figs_dir: Path | None = None,
  texts_dir: Path | None = None,
  regions_pdf_path: Path | None = None,
) -> dict:
  positions = find_question_positions(doc, max_questions=max_questions)
  question_rects = build_question_rectangles(doc, positions)
  result = {"positions": positions, "question_rects": question_rects}
  if export_question_images:
    result["questions_figs_dir"] = export_question_figures(
      doc, question_rects, out_dir=questions_figs_dir
    )
  if export_non_question_images:
    result["non_questions_figs_dir"] = export_non_question_figures(
      doc, question_rects, out_dir=non_questions_figs_dir
    )
  if export_texts:
    inside, outside = extract_question_texts(doc, question_rects)
    result["inside_texts"] = inside
    result["outside_texts"] = outside
    result["texts_dir"] = save_question_text_files(inside, outside, out_dir=texts_dir)
  if export_regions_pdf:
    result["regions_pdf_path"] = export_question_regions_pdf(
      doc, question_rects, output_path=regions_pdf_path
    )
  return result


def main() -> None:
  file_example = "data/vestibular/provas/prova_ita_vestibular_2025_prova_1f.pdf"
  doc = pymupdf.open(file_example)
  positions = find_question_positions(doc)
  found = {p[0] for p in positions}
  missing = [n for n in range(1, MAX_QUESTIONS + 1) if n not in found]
  print(f"Found {len(positions)} question start positions.")
  if missing:
    print(f"  Note: questions not found (different format or other exam): {missing}")
  for p in positions[:10]:
    print(
      f"  Question {p[0]} on page {p[1]}: bbox = ({p[2].x0:.1f}, {p[2].y0:.1f}, {p[2].x1:.1f}, {p[2].y1:.1f})"
    )
  question_rects = build_question_rectangles(doc, positions)
  print(f"Built rectangles for {len(question_rects)} questions.")
  for i in range(len(positions) - 1):
    num, next_num = positions[i][0], positions[i + 1][0]
    if next_num != num + 1:
      print(
        f"  Gap: after Question {num} came Question {next_num} (missing: {list(range(num + 1, next_num))})."
      )
  result = run_transform(
    doc,
    export_question_images=True,
    export_non_question_images=True,
    export_texts=True,
  )
  print(f"Question figures saved to {result['questions_figs_dir']}")
  print(f"Non-question figures saved to {result['non_questions_figs_dir']}")
  print(f"Texts saved to {result['texts_dir']}")
  print(f"PDF with regions marked in red: {result['regions_pdf_path']}")


if __name__ == "__main__":
  main()
