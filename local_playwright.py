"""
Local Playwright implementation of the Computer abstraction.
"""
import time
from typing import Dict, List, Optional, Tuple, Union
import io
import base64
from PIL import Image

from playwright.sync_api import sync_playwright

from computer import Computer


class LocalPlaywright(Computer):
    """Local Playwright implementation of the Computer abstraction."""

    def __init__(self, start_url: str = "https://bing.com", headless: bool = False):
        """Initialize the LocalPlaywright computer."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self.page.goto(start_url)
        # Wait for page to load
        self.page.wait_for_load_state("networkidle")

    def __del__(self):
        """Clean up resources."""
        try:
            self.browser.close()
            self.playwright.stop()
        except:
            pass

    def screenshot(self) -> Image.Image:
        """Take a screenshot of the current state of the computer."""
        screenshot_bytes = self.page.screenshot()
        return Image.open(io.BytesIO(screenshot_bytes))

    def click(self, x: int, y: int, button: str = "left") -> None:
        """Click at the specified coordinates."""
        self.page.mouse.click(x, y, button=button)

    def double_click(self, x: int, y: int) -> None:
        """Double click at the specified coordinates."""
        self.page.mouse.dblclick(x, y)

    def type(self, text: str) -> None:
        """Type the specified text."""
        self.page.keyboard.type(text)

    def scroll(self, x: int, y: int, scroll_x: int = 0, scroll_y: int = 0) -> None:
        """Scroll at the specified coordinates."""
        self.page.mouse.move(x, y)
        self.page.mouse.wheel(delta_x=scroll_x, delta_y=scroll_y)

    def wait(self, ms: int = 1000) -> None:
        """Wait for the specified number of milliseconds."""
        self.page.wait_for_timeout(ms)

    def move(self, x: int, y: int) -> None:
        """Move the cursor to the specified coordinates."""
        self.page.mouse.move(x, y)

    def keypress(self, keys: List[str]) -> None:
        """Press the specified keys."""
        for key in keys:
            self.page.keyboard.press(key)

    def drag(self, path: List[List[int]]) -> None:
        """Drag along the specified path."""
        if len(path) < 2:
            return
        
        start = path[0]
        self.page.mouse.move(start[0], start[1])
        self.page.mouse.down()
        
        for point in path[1:]:
            self.page.mouse.move(point[0], point[1])
        
        self.page.mouse.up()
        
    # Additional helper methods
    def goto(self, url: str) -> None:
        """Navigate to the specified URL."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        
    def back(self) -> None:
        """Go back to the previous page."""
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")
