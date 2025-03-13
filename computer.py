"""
Computer abstraction for OpenAI Computer-Using Agent.
This defines the interface for interacting with a computer environment.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union
from PIL import Image


class Computer(ABC):
    """Base class for computer environments."""

    @abstractmethod
    def screenshot(self) -> Image.Image:
        """Take a screenshot of the current state of the computer."""
        pass

    @abstractmethod
    def click(self, x: int, y: int, button: str = "left") -> None:
        """Click at the specified coordinates."""
        pass

    @abstractmethod
    def double_click(self, x: int, y: int) -> None:
        """Double click at the specified coordinates."""
        pass

    @abstractmethod
    def type(self, text: str) -> None:
        """Type the specified text."""
        pass

    @abstractmethod
    def scroll(self, x: int, y: int, scroll_x: int = 0, scroll_y: int = 0) -> None:
        """Scroll at the specified coordinates."""
        pass

    @abstractmethod
    def wait(self, ms: int = 1000) -> None:
        """Wait for the specified number of milliseconds."""
        pass

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        """Move the cursor to the specified coordinates."""
        pass

    @abstractmethod
    def keypress(self, keys: List[str]) -> None:
        """Press the specified keys."""
        pass

    @abstractmethod
    def drag(self, path: List[List[int]]) -> None:
        """Drag along the specified path."""
        pass
