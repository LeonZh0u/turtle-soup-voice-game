from typing import AsyncIterable, Dict, Optional
from livekit.agents import Agent
from livekit.agents.llm import ChatContext, ChatChunk
from pydantic import BaseModel
from ..utils.utils import generate_turtle_soup_prompt

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
        super().__init__()
        self.game_state = GameState(
            mystery=mystery,
            answer=answer,
            keywords=keywords
        )
        self.max_hints = 3
        self.max_questions = 20
        self._system_prompt = generate_turtle_soup_prompt(
            story=mystery,
            truth=answer,
            tips=", ".join(keywords)
        )

    async def llm_node(
        self,
        chat_ctx: ChatContext,
        tools,
        model_settings
    ) -> AsyncIterable[ChatChunk]:
        """Process player questions and generate appropriate responses."""
        if not chat_ctx.messages:
            intro = self._get_introduction()
            self.game_state.last_response = intro
            yield ChatChunk(text=intro)
            return

        user_question = chat_ctx.messages[-1].content
        self.game_state.question_count += 1

        # Check if we've exceeded the question limit
        if self.game_state.question_count > self.max_questions:
            response = "I'm sorry, but you've reached the maximum number of questions. Would you like to know the answer?"
            self.game_state.last_response = response
            yield ChatChunk(text=response)
            return

        # Process the question and generate response
        response = await self._process_question(user_question)
        self.game_state.last_response = response
        yield ChatChunk(text=response)

    def _get_introduction(self) -> str:
        """Generate the game introduction."""
        return (
            f"Welcome to Turtle Soup! I have a mystery for you to solve:\n\n"
            f"{self.game_state.mystery}\n\n"
            f"You can ask me yes/no questions to figure out what's happening. "
            f"I'll respond with 'Yes', 'No', 'Maybe', or 'Irrelevant'. "
            f"You have {self.max_questions} questions to solve the mystery. "
            f"Good luck!"
        )

    async def _process_question(self, question: str) -> str:
        """Process a player's question using LLM to determine the appropriate response."""
        # Create a chat context with the system prompt and user question
        chat_context = ChatContext(
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": question}
            ]
        )

        # Get response from LLM
        async for chunk in self.llm_node(chat_context, None, None):
            response = chunk.text.strip()
            
            # If the response indicates a crucial question, add a hint
            if "crucial" in response.lower() and self._should_give_hint():
                self.game_state.hints_given += 1
                response += " (This is a crucial question that's getting closer to the truth!)"
            
            return response

    async def on_enter(self) -> None:
        """Called when the agent enters a room."""
        pass

    async def on_exit(self) -> None:
        """Called when the agent exits a room."""
        pass

    def _should_give_hint(self) -> bool:
        """Determine if a hint should be given based on game state."""
        return (self.game_state.question_count > 10 and 
                self.game_state.hints_given < self.max_hints) 