from dataclasses import dataclass
from typing import List
from enum import Enum
import json

class Rarity(Enum):
    LAME = ("Lame", "#808080")          # Dark Gray
    LAME_PLUS = ("Lame+", "#999999")    # Gray
    COMMON = ("Common", "#e6e6e6")       # Light Gray
    COMMON_PLUS = ("Common+", "#ffffff") # White
    RARE = ("Rare", "#0066FF")          # Blue
    RARE_PLUS = ("Rare+", "#00AAFF")    # Light Blue
    LEGENDARY = ("Legendary", "#FFD700") # Gold
    LEGENDARY_PLUS = ("Legendary+", "#FFA500") # Orange
    SPECIAL = ("Special", "#FF0000")     # Red
    SPECIAL_PLUS = ("Special+", "#FF1493") # Deep Pink

    def __init__(self, label: str, color: str):
        self.label = label
        self.color = color

@dataclass
class Card:
    name: str
    type: str
    rarity: Rarity
    quantity: int = 1

class Inventory:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        # Check if card already exists
        for existing_card in self.cards:
            if (existing_card.name == card.name):
                existing_card.quantity += card.quantity
                return
        self.cards.append(card)

    def display_inventory(self) -> None:
        print("\n=== Card Inventory ===")
        print("Name".ljust(20) + "Type".ljust(8) + "Rarity".ljust(8) + "Quantity".ljust(8))
        print("-" * 56)  
        for card in self.cards:
            rarity_display = f"{card.rarity.value[1]}{card.rarity.value[0]}"
            quantity_str = str(card.quantity).ljust(8)
            print(f"{card.name.ljust(20)}{card.type.ljust(8)}{rarity_display.ljust(20)}{quantity_str}")

    def export_to_json(self) -> None:
        """Export inventory to JSON file for web display"""
        inventory_data = []
        for card in self.cards:
            inventory_data.append({
                'name': card.name,
                'type': card.type,
                'rarity': card.rarity.value[0],
                'color': card.rarity.value[1],
                'quantity': card.quantity
            })
        
        with open('inventory_data.json', 'w') as f:
            json.dump(inventory_data, f, indent=2)

# Example usage
def main():
    inventory = Inventory()
    
    # Add the cards attributes
    card_attributes = [
        Card("Thing1", "Type", Rarity.LAME),
        Card("Thing2", "Type", Rarity.LAME_PLUS),
        Card("Thing3", "Type", Rarity.COMMON),
        Card("Thing4", "Type", Rarity.COMMON_PLUS),
        Card("Thing5", "Type", Rarity.RARE),
        Card("Thing6", "Type", Rarity.RARE_PLUS),
        Card("Thing7", "Type", Rarity.LEGENDARY),
        Card("Thing8", "Type", Rarity.LEGENDARY_PLUS),
        Card("Thing9", "Type", Rarity.SPECIAL),
        Card("Thing10", "Type", Rarity.SPECIAL_PLUS)
    ]
    
    for card in card_attributes:
        inventory.add_card(card)

    # Export JSON data
    inventory.export_to_json()
    
    # Start local server
    import subprocess
    print("\nStarting local server...")
    subprocess.run(["python", "-m", "http.server", "8000"], shell=True)

if __name__ == "__main__":
    main()