#!/usr/bin/env python3
"""
Command Line Chat Agent
A CLI tool that accepts user requests, displays status updates, and shows results.
"""

import sys
import time
import threading
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class StatusType(Enum):
    """Types of status messages"""
    THINKING = "🤔"
    PROCESSING = "⚙️"
    SUCCESS = "✅"
    ERROR = "❌"
    INFO = "ℹ️"


@dataclass
class StatusMessage:
    """Represents a status message"""
    type: StatusType
    message: str
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class StatusDisplay:
    """Handles status message display with updates"""
    
    def __init__(self):
        self.current_status: Optional[str] = None
        self.status_history: List[StatusMessage] = []
        self._lock = threading.Lock()
        self._spinner_thread = None
        self._stop_spinner = False
        
    def update(self, status_type: StatusType, message: str):
        """Update the current status message"""
        with self._lock:
            status = StatusMessage(status_type, message)
            self.status_history.append(status)
            
            # Clear current line and display new status
            self._clear_line()
            print(f"{status.type.value} {message}", end='', flush=True)
            self.current_status = message
    
    def complete(self, message: str = "Complete"):
        """Mark the current operation as complete"""
        self.stop_spinner()
        self.update(StatusType.SUCCESS, message)
        print()  # Move to next line
        
    def error(self, message: str):
        """Display an error message"""
        self.stop_spinner()
        self.update(StatusType.ERROR, message)
        print()  # Move to next line
        
    def start_spinner(self, message: str):
        """Start an animated spinner for long-running operations"""
        self.stop_spinner()
        self._stop_spinner = False
        self._spinner_thread = threading.Thread(
            target=self._spin, 
            args=(message,)
        )
        self._spinner_thread.start()
        
    def stop_spinner(self):
        """Stop the spinner animation"""
        if self._spinner_thread:
            self._stop_spinner = True
            self._spinner_thread.join(timeout=0.5)
            self._spinner_thread = None
            
    def _spin(self, message: str):
        """Spinner animation loop"""
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while not self._stop_spinner:
            with self._lock:
                self._clear_line()
                print(f"{spinner[i % len(spinner)]} {message}", end='', flush=True)
            time.sleep(0.1)
            i += 1
            
    def _clear_line(self):
        """Clear the current line in the terminal"""
        print('\r' + ' ' * 80 + '\r', end='', flush=True)


class Agent:
    """Main agent class that processes user requests"""
    
    def __init__(self):
        self.status_display = StatusDisplay()
        
    def process_request(self, request: str) -> Dict[str, Any]:
        """
        Process a user request and return results
        
        Args:
            request: The user's input request
            
        Returns:
            Dictionary containing the result and any metadata
        """
        # Start processing
        self.status_display.update(StatusType.THINKING, "Analyzing request...")
        time.sleep(1)  # Simulate thinking
        
        # Perform some mock processing steps
        self.status_display.update(StatusType.PROCESSING, "Breaking down the task...")
        time.sleep(0.5)
        
        self.status_display.start_spinner("Processing components")
        time.sleep(2)  # Simulate long operation
        self.status_display.stop_spinner()
        
        self.status_display.update(StatusType.INFO, "Generating response...")
        time.sleep(0.5)
        
        # Complete processing
        self.status_display.complete("Task completed successfully")
        
        # Return mock result
        return {
            "status": "success",
            "response": f"Processed request: '{request}'",
            "steps_completed": 4,
            "processing_time": 4.0
        }
    
    def display_result(self, result: Dict[str, Any]):
        """Display the final result to the user"""
        print("\n" + "="*50)
        print("RESULT:")
        print("="*50)
        
        for key, value in result.items():
            print(f"  {key}: {value}")
        
        print("="*50 + "\n")


class ChatInterface:
    """Command line chat interface"""
    
    def __init__(self):
        self.agent = Agent()
        self.running = True
        
    def run(self):
        """Main interaction loop"""
        self._display_welcome()
        
        while self.running:
            try:
                # Get user input
                request = self._get_user_input()
                
                if request.lower() in ['exit', 'quit', 'q']:
                    self.running = False
                    print("Goodbye!")
                    break
                    
                if request.strip() == '':
                    continue
                
                # Process request
                print()  # Add spacing
                result = self.agent.process_request(request)
                
                # Display result
                self.agent.display_result(result)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                self.running = False
                
            except Exception as e:
                self.agent.status_display.error(f"Error: {str(e)}")
                
    def _display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*50)
        print("  COMMAND LINE CHAT AGENT")
        print("="*50)
        print("Type your request and press Enter.")
        print("Type 'exit', 'quit', or 'q' to quit.")
        print("="*50 + "\n")
        
    def _get_user_input(self) -> str:
        """Get input from the user"""
        return input("You> ").strip()


def main():
    """Main entry point"""
    interface = ChatInterface()
    interface.run()


if __name__ == "__main__":
    main()