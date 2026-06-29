from typing import Literal
from flashcard_generator import FlashcardCollection

def format_flashcards(
    deck: FlashcardCollection, 
    format_type: Literal["tab", "comma", "custom"] = "tab",
    custom_term_sep: str = "\t",
    custom_card_sep: str = ""
) -> str:
    """
    Formats a FlashcardCollection into a single string for exporting.
    """
    if format_type == "tab":
        term_sep = "\t"
        card_sep = ""
    elif format_type == "comma":
        term_sep = ","
        card_sep = ";"
    elif format_type == "custom":
        term_sep = custom_term_sep
        card_sep = custom_card_sep
    else:
        raise ValueError("Invalid format_type. Choose 'tab', 'comma', or 'custom'.")

    formatted_cards = []
    
    for card in deck.cards:
        front_clean = card.front.replace("\n", " ").replace(term_sep, " ")
        back_clean = card.back.replace("\n", " ").replace(term_sep, " ")
        
        if card_sep:
            front_clean = front_clean.replace(card_sep, " ")
            back_clean = back_clean.replace(card_sep, " ")
            
        formatted_cards.append(f"{front_clean}{term_sep}{back_clean}")
        
    join_string = f"{card_sep}\n"
    
    return join_string.join(formatted_cards)