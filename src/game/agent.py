from typing import AsyncIterable, Dict, Optional
from livekit.agents import Agent, llm
from livekit.agents.llm import ChatContext, ChatChunk
from pydantic import BaseModel
from utils.utils import generate_turtle_soup_prompt
import logging
import uuid
from livekit.plugins import (
    deepgram, 
    elevenlabs, 
    openai, 
)
import os

logger = logging.getLogger(__name__)

class GameState(BaseModel):
    """Represents the current state of the game."""
    mystery: str
    answer: str
    keywords: list[str]
    is_solved: bool = False
    question_count: int = 0
    hints_given: int = 0
    last_response: str = ""

class TurtleSoupAgent(Agent):
    def __init__(self, mystery: str, answer: str, keywords: list[str]):
        super().__init__(
            instructions=generate_turtle_soup_prompt(
                story=mystery,
                truth=answer,
                tips=", ".join(keywords)
            ),
            stt=deepgram.STT(),
            llm=openai.LLM(),
            tts=elevenlabs.TTS(voice_id=os.environ["ELEVENLABS_VOICE_ID"]),  # Using ElevenLabs for TTS
        )
        self.game_state = GameState(
            mystery=mystery,
            answer=answer,
            keywords=keywords
        )
        self.max_hints = 3
        self.max_questions = 20

    async def llm_node(
        self,
        chat_ctx: ChatContext,
        tools,
        model_settings
    ) -> AsyncIterable[ChatChunk]:
        """Process player questions and generate appropriate responses."""
        # if self.game_state.last_response == "":
        #     yield ChatChunk(
        #         role="assistant",
        #         content=""
        #     )
        #     return

        # Check if we've exceeded the question limit
        if self.game_state.question_count > self.max_questions:
            response = "I'm sorry, but you've reached the maximum number of questions. Would you like to know the answer?"
            yield ChatChunk(
                id=str(uuid.uuid4()),
                role="assistant",
                content=response
            )
            return

        # Process the question and generate response
        # async for chunk in Agent.default.llm_node(self, chat_ctx, None, None):
        #     logger.info(f"chat_ctx: {chat_ctx.items[-1]}")
        #     content = self._extract_content(chunk)
        #     if content is not None:
        #         full_response += content
        #         yield ChatChunk(
        #             id=str(uuid.uuid4()),
        #             role="assistant",
        #             content=chunk
        #         )
        async with self.llm.chat(
            chat_ctx=chat_ctx,
        ) as stream:
            async for chunk in stream:
                yield chunk
        self.game_state.question_count += 1
        # self.game_state.last_response = full_response.strip()

    def _get_introduction(self) -> str:
        """Generate the game introduction."""
        return (
            f"I am the host of the game Turtle Soup today. Are you ready to hear about the mystery?"
        )

    async def _process_question(self, chat_ctx: ChatContext) -> AsyncIterable[str]:
        """Process a player's question using LLM to determine the appropriate response."""
        full_response = ""
        # Get response from LLM
        async for chunk in Agent.default.llm_node(self, chat_ctx, None, None):
            logger.info(f"chat_ctx: {chat_ctx.items[-1]}")
            content = self._extract_content(chunk)
            if content is not None:
                full_response += content
                yield content
        self.game_state.question_count += 1
        self.game_state.last_response = full_response.strip()
        
        # If the response indicates a crucial question, add a hint
        # if "crucial" in full_response.lower() and self._should_give_hint():
        #     self.game_state.hints_given += 1
        #     yield " (This is a crucial question that's getting closer to the truth!)"

    async def on_enter(self) -> None:
        """Called when the agent enters a room."""
        self.session.say(self._get_introduction())

    def _should_give_hint(self) -> bool:
        """Determine if a hint should be given based on game state."""
        return (self.game_state.question_count > 10 and 
                self.game_state.hints_given < self.max_hints) 
    
    def _extract_content(self, chunk: any) -> Optional[str]:
        """Extract content from a chunk, handling different chunk formats."""
        if not chunk:
            return None
        if isinstance(chunk, str):
            return chunk
        if hasattr(chunk, 'delta'):
            return getattr(chunk.delta, 'content', None)
        return None