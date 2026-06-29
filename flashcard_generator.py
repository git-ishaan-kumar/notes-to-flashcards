import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

class Flashcard(BaseModel):
    front: str = Field(description="The question, prompt, or term.")
    back: str = Field(description="The answer, explanation, or definition.")
    concept_tag: str = Field(description="Sub-topic tag (e.g., 'Cell Organelles', 'Genetics').")

class FlashcardCollection(BaseModel):
    title: str = Field(description="A descriptive title for this study deck.")
    cards: List[Flashcard] = Field(description="List of extracted flashcards.")

def generate_cards(
    extracted_elements: List, 
    num_cards: Union[int, Literal["Auto"]] = "Auto", 
    flashcard_mode: Literal["Terms & Definitions", "Practice Test", "Fill-in-the-Blank", "Auto"] = "Auto"
) -> Optional[FlashcardCollection]:
    """Generates a validated FlashcardCollection from extracted text and images using Gemini 3.1 Flash Lite."""
    instructions = f"""
    You are an expert study assistant. Analyze the source material provided below, and generate a deck of flashcards.
    
    CRITICAL SETTINGS:
    1. Card Count Rule:
       - If num_cards is an integer, generate exactly that number of cards (currently: {num_cards}).
       - If num_cards is "Auto": analyze the depth of the material and determine the optimal number of cards.

    2. Flashcard Mode: {flashcard_mode}. 
       - If 'Terms & Definitions', focus on vocabulary and clear definitions.
       - If 'Practice Test', format the fronts of the cards like formal exam questions.
       - If 'Fill-in-the-Blank', create sentences with a missing key word/phrase represented by "___" on the front, and the missing word on the back.
       - If 'Auto', analyze the content and dynamically select the single most appropriate mode, or combine styles where it fits best.
    """
    
    full_payload = [instructions] + extracted_elements
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=full_payload,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FlashcardCollection,
                temperature=0.1
            )
        )
        return response.parsed
    except Exception:
        return None