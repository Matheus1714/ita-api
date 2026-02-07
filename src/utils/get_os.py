from typing import Optional
import platform

from src.constants import OperatingSystem

def get_os() -> Optional[OperatingSystem]:
  system = platform.system().lower()
  for os_ in OperatingSystem:
    if os_.value in system:
      return os_
  return None
