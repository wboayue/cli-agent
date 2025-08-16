#!/usr/bin/env python3
"""
Example of a more realistic agent implementation
Shows how to extend the base agent with actual processing logic
"""

import time
import random
from typing import Dict, Any, List
from agent import Agent, StatusType


class TaskAgent(Agent):
    """Example agent that performs various task types"""
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """Process user request with task-specific logic"""
        
        # Analyze request type
        self.status_display.update(StatusType.THINKING, "Analyzing request type...")
        time.sleep(0.5)
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['calculate', 'compute', 'math']):
            return self._handle_calculation(request)
        elif any(word in request_lower for word in ['search', 'find', 'look']):
            return self._handle_search(request)
        elif any(word in request_lower for word in ['analyze', 'review', 'check']):
            return self._handle_analysis(request)
        else:
            return self._handle_general(request)
    
    def _handle_calculation(self, request: str) -> Dict[str, Any]:
        """Handle calculation requests"""
        self.status_display.update(StatusType.PROCESSING, "Parsing mathematical expression...")
        time.sleep(0.5)
        
        self.status_display.update(StatusType.PROCESSING, "Computing result...")
        time.sleep(0.5)
        
        # Mock calculation
        result = random.randint(1, 100)
        
        self.status_display.complete("Calculation complete")
        
        return {
            "status": "success",
            "type": "calculation",
            "request": request,
            "result": f"The answer is {result}",
            "confidence": "95%"
        }
    
    def _handle_search(self, request: str) -> Dict[str, Any]:
        """Handle search requests"""
        self.status_display.start_spinner("Searching database")
        time.sleep(1.5)
        self.status_display.stop_spinner()
        
        self.status_display.update(StatusType.PROCESSING, "Ranking results...")
        time.sleep(0.5)
        
        self.status_display.update(StatusType.INFO, "Formatting output...")
        time.sleep(0.3)
        
        self.status_display.complete("Search complete")
        
        return {
            "status": "success",
            "type": "search",
            "request": request,
            "results_found": random.randint(5, 50),
            "top_result": "Example result item",
            "relevance_score": "87%"
        }
    
    def _handle_analysis(self, request: str) -> Dict[str, Any]:
        """Handle analysis requests"""
        steps = [
            "Loading data...",
            "Preprocessing input...",
            "Running analysis algorithms...",
            "Validating results...",
            "Generating insights..."
        ]
        
        for step in steps:
            self.status_display.update(StatusType.PROCESSING, step)
            time.sleep(0.6)
        
        self.status_display.complete("Analysis complete")
        
        return {
            "status": "success",
            "type": "analysis",
            "request": request,
            "insights_generated": random.randint(3, 8),
            "confidence_level": "High",
            "recommendation": "Consider reviewing the detailed report"
        }
    
    def _handle_general(self, request: str) -> Dict[str, Any]:
        """Handle general requests"""
        self.status_display.update(StatusType.THINKING, "Understanding request...")
        time.sleep(0.8)
        
        self.status_display.start_spinner("Processing request")
        time.sleep(1.2)
        self.status_display.stop_spinner()
        
        self.status_display.complete("Request processed")
        
        return {
            "status": "success",
            "type": "general",
            "request": request,
            "response": "Your request has been processed successfully",
            "next_steps": "You can continue with another request"
        }


class StreamingAgent(Agent):
    """Example agent that simulates streaming responses"""
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """Process with simulated streaming output"""
        
        self.status_display.update(StatusType.THINKING, "Preparing response stream...")
        time.sleep(0.5)
        
        # Simulate token generation
        tokens = request.split()
        processed_tokens = []
        
        self.status_display.update(StatusType.PROCESSING, f"Processing 0/{len(tokens)} tokens...")
        
        for i, token in enumerate(tokens, 1):
            time.sleep(0.2)  # Simulate processing time
            processed_tokens.append(token.upper())
            self.status_display.update(
                StatusType.PROCESSING, 
                f"Processing {i}/{len(tokens)} tokens..."
            )
        
        self.status_display.complete("Stream complete")
        
        return {
            "status": "success",
            "type": "streaming",
            "original": request,
            "processed": " ".join(processed_tokens),
            "tokens_processed": len(tokens)
        }


def demo():
    """Run a demonstration of different agent types"""
    
    print("\n" + "="*60)
    print("  AGENT DEMONSTRATION")
    print("="*60)
    
    # Demo TaskAgent
    print("\n1. Task Agent Demo:")
    print("-" * 40)
    task_agent = TaskAgent()
    
    requests = [
        "Calculate the sum of numbers",
        "Search for Python tutorials",
        "Analyze this dataset for patterns",
        "Help me with my project"
    ]
    
    for req in requests:
        print(f"\nRequest: '{req}'")
        result = task_agent.process_request(req)
        task_agent.display_result(result)
        time.sleep(1)
    
    # Demo StreamingAgent
    print("\n2. Streaming Agent Demo:")
    print("-" * 40)
    streaming_agent = StreamingAgent()
    
    print("\nRequest: 'Process this text word by word'")
    result = streaming_agent.process_request("Process this text word by word")
    streaming_agent.display_result(result)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        # Run the task agent as default
        from agent import ChatInterface
        
        class TaskChatInterface(ChatInterface):
            def __init__(self):
                super().__init__()
                self.agent = TaskAgent()
        
        interface = TaskChatInterface()
        interface.run()