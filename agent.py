"""
Agent implementation for OpenAI Computer-Using Agent.
"""
import json
import os
from typing import Dict, List, Optional, Any, Union
import base64
from io import BytesIO

from openai import OpenAI
from PIL import Image

from computer import Computer


class Agent:
    """Agent for interacting with OpenAI Computer-Using Agent."""

    def __init__(
        self,
        computer: Computer,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        debug: bool = False,
        show_images: bool = False,
    ):
        """Initialize the agent."""
        self.computer = computer
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.debug = debug
        self.show_images = show_images
        
        # Default tools including computer use
        self.tools = tools or []
        
        # Add computer use tool if not already present
        if not any(tool.get("type") == "computer_vision" for tool in self.tools):
            self.tools.append({"type": "computer_vision"})
        
        self.messages = []

    def _encode_image(self, image: Image.Image) -> str:
        """Encode image to base64."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def run_full_turn(self, user_input: Optional[str] = None) -> str:
        """Run a full turn of the agent."""
        # Take a screenshot
        screenshot = self.computer.screenshot()
        
        if self.show_images:
            screenshot.show()
        
        # Encode the screenshot
        base64_image = self._encode_image(screenshot)
        
        # Create the message content
        content = []
        
        # Add user input if provided
        if user_input:
            content.append({"type": "text", "text": user_input})
        
        # Add the screenshot
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}",
                    "detail": "high",
                },
            }
        )
        
        # Add the message to the conversation
        self.messages.append({"role": "user", "content": content})
        
        if self.debug:
            print(f"User message: {user_input}")
        
        # Get the response from the model
        response = self.client.responses.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
        )
        
        # Extract the response message
        response_message = response.choices[0].message
        self.messages.append(response_message)
        
        # Process tool calls if any
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                if tool_call.type == "computer_vision":
                    self._handle_computer_call(tool_call)
        
        # Return the response text
        return response_message.content or ""
    
    def _handle_computer_call(self, tool_call: Any) -> None:
        """Handle a computer call."""
        computer_call = tool_call.computer_vision
        
        if self.debug:
            print(f"Computer call: {computer_call}")
        
        # Process each action
        for action in computer_call.actions:
            action_type = action.type
            
            if action_type == "click":
                self.computer.click(action.coordinates.x, action.coordinates.y, action.button)
            elif action_type == "double_click":
                self.computer.double_click(action.coordinates.x, action.coordinates.y)
            elif action_type == "type":
                self.computer.type(action.text)
            elif action_type == "scroll":
                self.computer.scroll(
                    action.coordinates.x, 
                    action.coordinates.y, 
                    action.delta.x, 
                    action.delta.y
                )
            elif action_type == "wait":
                self.computer.wait(action.duration_ms)
            elif action_type == "move":
                self.computer.move(action.coordinates.x, action.coordinates.y)
            elif action_type == "keypress":
                self.computer.keypress(action.keys)
            elif action_type == "drag":
                path = [[point.x, point.y] for point in action.path]
                self.computer.drag(path)
            
            # Wait a bit after each action to let the UI update
            self.computer.wait(500)
