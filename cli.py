#!/usr/bin/env python
"""
Command-line interface for the OpenAI Computer-Using Agent.
"""
import argparse
import os
from dotenv import load_dotenv

from local_playwright import LocalPlaywright
from agent import Agent


def main():
    """Run the CLI."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="OpenAI Computer-Using Agent CLI")
    parser.add_argument(
        "--input", 
        type=str, 
        help="Initial input to the agent"
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
        "--start-url", 
        type=str, 
        default="https://bing.com", 
        help="Start URL for browser environments"
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
    computer = LocalPlaywright(start_url=args.start_url, headless=args.headless)
    
    # Create the agent
    agent = Agent(
        computer=computer,
        debug=args.debug,
        show_images=args.show,
    )
    
    # Initial input
    user_input = args.input
    
    # Main loop
    try:
        while True:
            # If no input is provided, prompt the user
            if not user_input:
                user_input = input("\nEnter your instruction (or 'exit' to quit): ")
                
                if user_input.lower() in ["exit", "quit"]:
                    break
            
            # Run the agent
            response = agent.run_full_turn(user_input)
            
            # Print the response
            print("\nAgent response:")
            print(response)
            
            # Reset user input for the next iteration
            user_input = None
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up resources
        del computer


if __name__ == "__main__":
    main()
