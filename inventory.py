from dataclasses import dataclass
from typing import List
from enum import Enum
from pathlib import Path
import json
import os
import subprocess

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

class Card:
    def __init__(self, name: str, type: str, rarity: Rarity, image: str = None, quantity: int = 1):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.image = image
        self.quantity = quantity

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "rarity": self.rarity.name,
            "color": self.rarity.value,
            "quantity": self.quantity,
            "image": self.image or ""
        }

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
                'quantity': card.quantity,
                'image': card.image,
            })
        
        with open('inventory_data.json', 'w') as f:
            json.dump(inventory_data, f, indent=2)

# Example usage
def main():
    inventory = Inventory()
    
    # Ensure images directory exists
    image_path = os.path.join(os.path.dirname(__file__), "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)
        print(f"Created images directory at {image_path}")


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

    # Create a card with an image
    card1 = Card(
        name="Statue",
        type="Painting",
        rarity=Rarity.LEGENDARY,
        image=os.path.expanduser("images/statue.jpg")
        )
    
    print(f"Card1 image path: {card1.image}")  # Debugging line
    # Check if the image file exists
    if os.path.isfile(card1.image):
        print(f"Image file exists: {card1.image}")
    else:
        print(f"Image file does not exist: {card1.image}")

    inventory.add_card(card1)

    # Export JSON data
    inventory.export_to_json()
    
    # Start local server with proper error handling
    print("\nStarting local server...")
    try:
        subprocess.run(
            ["python", "-m", "http.server", "8000"],
            check=True,
            shell=False
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to start server: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped by user")

if __name__ == "__main__":
    main()