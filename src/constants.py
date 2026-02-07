from enum import Enum

class OperatingSystem(Enum):
  MACOS = "darwin"
  LINUX = "linux"
  WINDOWS = "windows"

class Architecture(Enum):
  X64 = "x64"
  ARM64 = "arm64"

OS_ARCH_MAP = {
  OperatingSystem.MACOS: {
    Architecture.X64: "mac-x64",
    Architecture.ARM64: "mac-arm64",
  },
  OperatingSystem.LINUX: {
    Architecture.X64: "linux-x64",
    Architecture.ARM64: "linux-arm64",
  },
  OperatingSystem.WINDOWS: {
    Architecture.X64: "win-x64",
    Architecture.ARM64: "win-arm64",
  },
}
