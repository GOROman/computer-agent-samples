#!/usr/bin/env python
"""
Example script that uses the Computer-Using Agent to check the weather.
"""
import os
import argparse
from dotenv import load_dotenv

from local_playwright import LocalPlaywright
from agent import Agent


def main():
    """Run the weather example."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Weather example using Computer-Using Agent")
    parser.add_argument(
        "--location", 
        type=str, 
        default="Tokyo", 
        help="Location to check weather for"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug mode"
    )
    parser.add_argument(
        "--show", 
        action="store_true", 
        help="Show images during execution"
    )
    parser.add_argument(
        "--headless", 
        action="store_true", 
        help="Run browser in headless mode"
    )
    
    args = parser.parse_args()
    
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        api_key = input("Please enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Create the computer environment
    # Start with weather.com
    computer = LocalPlaywright(start_url="https://weather.com", headless=args.headless)
    
    # Create the agent
    agent = Agent(
        computer=computer,
        debug=args.debug,
        show_images=args.show,
    )
    
    # Run the agent with the weather query
    user_input = f"Check the current weather for {args.location} and tell me the temperature and forecast for today."
    print(f"\nTask: {user_input}")
    
    # Run the agent
    response = agent.run_full_turn(user_input)
    
    # Print the response
    print("\nAgent response:")
    print(response)


if __name__ == "__main__":
    main()
