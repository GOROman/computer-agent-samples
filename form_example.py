#!/usr/bin/env python
"""
Example script that uses the Computer-Using Agent to fill out a form on a website.
"""
import os
import argparse
from dotenv import load_dotenv

from local_playwright import LocalPlaywright
from agent import Agent


def main():
    """Run the form filling example."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Form filling example using Computer-Using Agent")
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
    # Start with a simple form website
    computer = LocalPlaywright(start_url="https://httpbin.org/forms/post", headless=args.headless)
    
    # Create the agent
    agent = Agent(
        computer=computer,
        debug=args.debug,
        show_images=args.show,
    )
    
    # Run the agent with the form filling task
    user_input = "Fill out this form with sample data and submit it. Then tell me what happened."
    print(f"\nTask: {user_input}")
    
    # Run the agent
    response = agent.run_full_turn(user_input)
    
    # Print the response
    print("\nAgent response:")
    print(response)


if __name__ == "__main__":
    main()
