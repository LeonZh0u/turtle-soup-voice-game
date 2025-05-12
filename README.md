# Turtle Soup Voice Game

A voice-interactive Turtle Soup lateral thinking game powered by LiveKit's STT-LLM-TTS pipeline.

## 🎮 Overview

This game implements a voice-based version of the classic Turtle Soup lateral thinking game. Players can ask yes/no questions to solve mysteries, with an AI game master responding through voice interaction.

## 🛠️ Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/turtle-soup-voice-game.git
cd turtle-soup-voice-game
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```bash
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
OPENAI_API_KEY=your_openai_api_key
```

## 🚀 Running the Game

1. Start the server:
```bash
python src/main.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Join a game room and start playing!

## 🎯 How to Play

1. The AI game master will present a mystery scenario
2. Players take turns asking yes/no questions
3. The game master responds with:
   - "Yes" - The question is correct and relevant
   - "No" - The question is incorrect
   - "Maybe" - The question is partially correct
   - "Irrelevant" - The question doesn't help solve the mystery

## 📝 License

MIT License
