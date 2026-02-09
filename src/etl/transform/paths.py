from pathlib import Path


def get_base_data_dir(*, from_cwd: Path | None = None) -> Path:
  cwd = from_cwd or Path.cwd()
  if cwd.name == "notebooks":
    return (cwd.parent / "data" / "vestibular").resolve()
  return (cwd / "data" / "vestibular").resolve()


def get_questions_figs_dir(*, from_cwd: Path | None = None) -> Path:
  return get_base_data_dir(from_cwd=from_cwd) / "figs" / "questoes"


def get_non_questions_figs_dir(*, from_cwd: Path | None = None) -> Path:
  return get_base_data_dir(from_cwd=from_cwd) / "figs" / "fora_questoes"


def get_question_texts_dir(*, from_cwd: Path | None = None) -> Path:
  return get_base_data_dir(from_cwd=from_cwd) / "figs" / "textos_questoes"


def get_question_regions_pdf_path(*, from_cwd: Path | None = None) -> Path:
  return get_base_data_dir(from_cwd=from_cwd) / "figs" / "questoes_regioes.pdf"
