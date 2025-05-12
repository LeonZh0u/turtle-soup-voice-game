import os
from typing import Dict
from pydantic import BaseModel
from dotenv import load_dotenv
from livekit.agents import Agent, JobContext, WorkerOptions
from livekit.agents import AgentSession, RoomInputOptions
from livekit.plugins import deepgram, elevenlabs, silero, openai
from livekit import agents

from game.agent import TurtleSoupAgent
from game.mysteries import get_random_mystery

# Load environment variables
load_dotenv()

class UserData(BaseModel):
    """User data model for the game session."""
    agents: Dict[str, Agent] = {}
    current_mystery: str = ""
    mystery_id: str = ""

async def entrypoint(ctx: JobContext):
    """Main entry point for the LiveKit agent."""
    await ctx.connect()

    # Get a random mystery
    mystery_id, mystery = get_random_mystery()
    
    # Initialize user data
    userdata = UserData()
    userdata.current_mystery = mystery.scenario
    userdata.mystery_id = mystery_id
    
    # Create and register the game agent
    userdata.agents.update({
        "game_master": TurtleSoupAgent(
            mystery=mystery.scenario,
            answer=mystery.answer,
            keywords=mystery.keywords
        )
    })

    # Initialize the agent session with STT, LLM, TTS, and VAD
    session = AgentSession[UserData](
        userdata=userdata,
        stt=deepgram.STT(),
        llm=openai.LLM(),
        tts=elevenlabs.TTS(),  # Using ElevenLabs for TTS
        vad=silero.VAD.load(),
        max_tool_steps=5
    )

    # Start the session with the game master agent
    await session.start(
        agent=userdata.agents["game_master"],
        room=ctx.room,
        room_input_options=RoomInputOptions()
    )

if __name__ == "__main__":
    agents.cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint)) 