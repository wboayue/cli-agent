# Command Line Chat Agent

A Python framework for building interactive command-line agents with real-time status updates and visual feedback.

## Features

- **Interactive CLI Interface** - Accept user requests and display results in a clean, structured format
- **Real-time Status Updates** - Visual feedback with status messages and animated spinners
- **Extensible Architecture** - Easy-to-extend base classes for custom agent implementations
- **Thread-safe Operations** - Proper handling of concurrent status updates
- **Multiple Status Types** - Thinking, processing, success, error, and info states with emoji indicators

## Installation

This project uses `uv` for dependency management:

```bash
# Initialize project (if not already done)
uv init

# Run the basic agent
uv run python agent.py

# Run the enhanced task agent
uv run python example_agent.py

# Run the demonstration
uv run python example_agent.py demo
```

## Quick Start

### Basic Usage

Run the interactive chat interface:

```bash
uv run python agent.py
```

You'll see a prompt where you can type requests:

```
==================================================
  COMMAND LINE CHAT AGENT
==================================================
Type your request and press Enter.
Type 'exit', 'quit', or 'q' to quit.
==================================================

You> Help me analyze this data
> Analyzing request...
™ Breaking down the task...
8 Processing components
9 Generating response...
 Task completed successfully

==================================================
RESULT:
==================================================
  status: success
  response: Processed request: 'Help me analyze this data'
  steps_completed: 4
  processing_time: 4.0
==================================================
```

## Architecture

### Core Components

#### `StatusDisplay`
Manages status message display with animations and thread-safe updates.

```python
from agent import StatusDisplay, StatusType

status = StatusDisplay()
status.update(StatusType.THINKING, "Analyzing request...")
status.start_spinner("Processing data")
# ... long operation ...
status.stop_spinner()
status.complete("Done!")
```

#### `Agent`
Base class for implementing agent logic.

```python
from agent import Agent

class MyAgent(Agent):
    def process_request(self, request: str) -> Dict[str, Any]:
        # Your processing logic here
        self.status_display.update(StatusType.PROCESSING, "Working...")
        result = do_something(request)
        self.status_display.complete("Success")
        return {"status": "success", "result": result}
```

#### `ChatInterface`
Manages the interactive command-line loop.

```python
from agent import ChatInterface

interface = ChatInterface()
interface.run()  # Starts the interactive loop
```

## Extending the Agent

### Creating a Custom Agent

To create your own agent, subclass the `Agent` class and implement the `process_request` method:

```python
from agent import Agent, StatusType
import time
from typing import Dict, Any

class CustomAgent(Agent):
    def process_request(self, request: str) -> Dict[str, Any]:
        """Process user request with custom logic"""
        
        # Show thinking status
        self.status_display.update(StatusType.THINKING, "Understanding request...")
        time.sleep(0.5)
        
        # Perform processing with spinner
        self.status_display.start_spinner("Fetching data from API")
        # ... your API call here ...
        time.sleep(2)
        self.status_display.stop_spinner()
        
        # Show completion
        self.status_display.complete("Processing complete")
        
        # Return results
        return {
            "status": "success",
            "request": request,
            "data": "Your processed data here"
        }
```

### Using Your Custom Agent

```python
from agent import ChatInterface

class CustomChatInterface(ChatInterface):
    def __init__(self):
        super().__init__()
        self.agent = CustomAgent()

if __name__ == "__main__":
    interface = CustomChatInterface()
    interface.run()
```

### Advanced Example: Task-Specific Agent

The `example_agent.py` file demonstrates a more sophisticated implementation:

```python
class TaskAgent(Agent):
    def process_request(self, request: str) -> Dict[str, Any]:
        # Route to different handlers based on request type
        if "calculate" in request.lower():
            return self._handle_calculation(request)
        elif "search" in request.lower():
            return self._handle_search(request)
        # ... more handlers
```

## Status Types

The framework provides several status types for different states:

- `StatusType.THINKING` (>) - Initial analysis/planning phase
- `StatusType.PROCESSING` (™) - Active processing
- `StatusType.SUCCESS` () - Successful completion
- `StatusType.ERROR` (L) - Error occurred
- `StatusType.INFO` (9) - Informational updates

## API Reference

### Agent Methods

- `process_request(request: str) -> Dict[str, Any]` - Main processing method to override
- `display_result(result: Dict[str, Any])` - Formats and displays results

### StatusDisplay Methods

- `update(status_type: StatusType, message: str)` - Update current status
- `start_spinner(message: str)` - Start animated spinner
- `stop_spinner()` - Stop the spinner
- `complete(message: str)` - Mark operation as complete
- `error(message: str)` - Display error message

## Examples

### Simple Calculation Agent

```python
class CalcAgent(Agent):
    def process_request(self, request: str) -> Dict[str, Any]:
        self.status_display.update(StatusType.PROCESSING, "Calculating...")
        
        # Parse and evaluate expression
        try:
            result = eval(request)  # Note: Use safe evaluation in production
            self.status_display.complete("Calculation done")
            return {"status": "success", "result": result}
        except Exception as e:
            self.status_display.error(f"Failed: {e}")
            return {"status": "error", "error": str(e)}
```

### API Integration Agent

```python
class APIAgent(Agent):
    def process_request(self, request: str) -> Dict[str, Any]:
        self.status_display.start_spinner("Connecting to API")
        
        try:
            # Your API logic here
            response = requests.get(f"https://api.example.com/query?q={request}")
            data = response.json()
            
            self.status_display.complete("Data retrieved")
            return {
                "status": "success",
                "data": data,
                "source": "API"
            }
        finally:
            self.status_display.stop_spinner()
```

## Running Tests

Run the included demonstration to see various agent behaviors:

```bash
uv run python example_agent.py demo
```

This will showcase:
- Different request types (calculation, search, analysis)
- Status update patterns
- Spinner animations
- Result formatting

## Contributing

To extend this framework:

1. Subclass `Agent` for custom processing logic
2. Use `StatusDisplay` for user feedback
3. Return structured dictionaries from `process_request`
4. Handle errors gracefully with try/except blocks
5. Use appropriate status types for different phases

## License

MIT

## Support

For issues or questions, please open an issue on the project repository.