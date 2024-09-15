# Math with Gestures

**Math with Gestures** is an interactive application that allows users to perform mathematical operations using hand gestures. The system tracks hand movements to recognize mathematical symbols and numbers drawn in the air, providing real-time feedback and solutions.

## Technologies Used
- **Mediapipe**: For real-time hand tracking and gesture detection.
- **OpenCV**: For image capture and processing of the camera feed.
- **Google Gemini**: For analyzing and recognizing mathematical symbols drawn by the user.
- **Streamlit**: For building the web-based user interface.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/math-with-gestures.git
   cd math-with-gestures
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate    # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Launch the application using the command mentioned above.
2. The camera feed will open, and you can use your fingers to draw numbers or mathematical symbols in the air.
3. The app will recognize the gestures and perform the corresponding mathematical operations in real-time, displaying results on the Streamlit dashboard.

## Contributing

Feel free to open issues or pull requests if you'd like to contribute to the project.