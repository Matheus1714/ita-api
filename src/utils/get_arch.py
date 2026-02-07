import platform

from src.constants import Architecture


def get_arch() -> Architecture:
  machine = platform.machine().lower()

  if machine in ("x86_64", "amd64"):
    return Architecture.X64
  if machine in ("arm64", "aarch64"):
    return Architecture.ARM64

  return Architecture.X64
