# AI Interview Agent

This project implements an AI agent designed to generate interview scripts for developers based on job descriptions, conduct audio interviews, and present technical challenges related to the job's technologies. The application leverages OpenAI's capabilities to enhance the interview process.

## Project Structure

```
ai-interview-agent
├── src
│   ├── main.py                # Entry point of the FastAPI application
│   ├── utils.py               # Utility functions for OpenAI API interactions
│   ├── interview
│   │   ├── script_generator.py # Generates interview scripts based on job descriptions
│   │   ├── audio_interview.py  # Handles the audio interview process
│   │   └── tech_challenge.py    # Creates technical challenges based on job technologies
│   └── models
│       └── schemas.py         # Defines data models and schemas for API
├── requirements.txt           # Project dependencies
├── .env.example               # Template for environment variables
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ai-interview-agent
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in the required values, especially the OpenAI API key.

## Usage

1. **Run the FastAPI application:**
   ```
   uvicorn src.main:app --reload
   ```

2. **Access the API documentation:**
   Open your browser and navigate to `http://localhost:8000/docs` to view the interactive API documentation.

## Functionality

- **Generate Interview Scripts:** Use the `/generate-script` endpoint to create interview scripts based on job descriptions.
- **Conduct Audio Interviews:** Use the `/conduct-audio-interview` endpoint to manage audio interviews and record responses.
- **Present Technical Challenges:** Use the `/create-tech-challenge` endpoint to generate technical challenges related to the job's technologies.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.