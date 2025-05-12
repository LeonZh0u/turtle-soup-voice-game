from typing import Dict, List, Tuple

class Mystery:
    def __init__(self, scenario: str, answer: str, keywords: List[str]):
        self.scenario = scenario
        self.answer = answer
        self.keywords = keywords

# Collection of predefined mysteries
MYSTERIES: Dict[str, Mystery] = {
    "the_man_who_hanged_himself": Mystery(
        scenario=(
            "A man is found dead, hanging from the ceiling of his room. "
            "The room is completely empty except for a puddle of water on the floor. "
            "How did he die?"
        ),
        answer=(
            "The man was an ice sculptor. He stood on a block of ice to reach the ceiling, "
            "tied the noose, and then waited for the ice to melt."
        ),
        keywords=["ice", "sculptor", "melt", "water", "block", "stand"]
    ),
    "the_deadly_room": Mystery(
        scenario=(
            "A man enters a room and dies immediately. "
            "The room is completely empty and sealed. "
            "What happened?"
        ),
        answer=(
            "The man was a deep-sea diver. The room was a decompression chamber, "
            "and someone had removed all the air, causing him to die from the pressure change."
        ),
        keywords=["diver", "pressure", "decompression", "air", "sea", "deep"]
    ),
    "the_mysterious_death": Mystery(
        scenario=(
            "A man is found dead in the middle of a field. "
            "He is completely naked and holding a match. "
            "How did he die?"
        ),
        answer=(
            "The man was a passenger in a hot air balloon. "
            "The balloon was losing altitude, so the passengers had to remove their clothes "
            "to lighten the load. When that wasn't enough, they drew matches to see who would jump. "
            "He drew the short match and had to jump to his death."
        ),
        keywords=["balloon", "hot air", "jump", "match", "naked", "field"]
    )
}

def get_random_mystery() -> Tuple[str, Mystery]:
    """Returns a random mystery from the collection."""
    import random
    mystery_id = random.choice(list(MYSTERIES.keys()))
    return mystery_id, MYSTERIES[mystery_id] 