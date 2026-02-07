from src.etl.extract import extract
from src.etl.transform import transform
from src.etl.load import load

if __name__ == "__main__":
  extract()
  transform()
  load()
