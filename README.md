# Gesture-painting
A web-based application for creating and analyzing gesture paintings using hand movements, providing a unique and interactive art experience.

## Features
- Real-time Hand Gesture Detection: Utilizes Mediapipe to detect hand landmarks.
- Interactive Drawing: Draw on the canvas by moving your finger in front of the webcam.
- Color Selection: Choose from multiple colors (white, green, red, black).
- Clear Canvas: Clear the canvas using a specific gesture.

## Getting Started

### Prerequisites

- Python 3.6 or later
- `virtualenv` or `venv` for creating virtual environments
- Docker (for containerization)

### Project Structure

```plaintext
Gesture Painting/
├── Dockerfile
├── requirements.txt
├── Makefile
├── tests/

```

## Example

### Usage
To use the chatbot, send a POST request to the /chat endpoint with a JSON payload containing the message.

### Input
The application uses your webcam to capture hand gestures. No manual input is required.

### Output
A digital painting created based on your hand gestures, along with feedback on your technique.

Clone the repository:
   ```bash
   git clone git@github.com:hitesharora1997/gesture_painting.git
   cd gesture_painting
   ```
Create a virtual environment and install dependencies:
   ```bash
   make setup
   ```
Run the application:
   ```bash
   make run
   ```
To run the test:
   ```bash
   make test
   ```
Building Docker Image
   ```bash
   make docker
   ```
Running Docker Image
   ```bash
   make docker-run
   ```

Cleaning up the virtual environment and other generated files:
   ```bash
   make clean
   ```
Help
   ```bash
   make help
   ```

### Caveats and Limitations
Caveats and Limitations
- Gesture Recognition Accuracy: The accuracy of gesture recognition may vary depending on lighting conditions and background noise.
- Performance: Real-time processing might experience latency on lower-end hardware.
- Error Handling: Basic error handling is implemented. More comprehensive error handling could be added for robustness.
- Testing Coverage: The tests cover major functionalities. Additional tests for edge cases and stress conditions could improve reliability.
- Data Persistence: Currently, data is stored in memory during runtime and is not persisted after the application stops.
- Compatibility: The application is tested on modern browsers. Compatibility with older browsers is not guaranteed.
