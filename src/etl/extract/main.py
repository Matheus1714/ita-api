import argparse

from src.etl.extract._extract_pos import extract_pos
from src.etl.extract._extract_vestibular import extract_vestibular


def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "type",
    nargs="?",
    choices=["vestibular", "pos"],
    default=None,
    help="type of extraction: vestibular or pos (mandatory)",
  )
  parser.add_argument(
    "--no-headless",
    action="store_true",
    help="run Chrome with window visible",
  )
  parser.add_argument(
    "--force",
    action="store_true",
    default=False,
    help="regenerate JSON files from site even if they exist",
  )
  args = parser.parse_args()

  if args.type is None:
    parser.error("It is mandatory to choose a type of extraction: vestibular or pos")

  common = dict(
    headless=not args.no_headless,
    force_replace=args.force,
  )
  if args.type == "vestibular":
    extract_vestibular(**common)
  else:
    extract_pos(**common)


if __name__ == "__main__":
  main()
