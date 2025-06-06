import json
import math
from typing import Dict

RECIPE_FILE = "recipes.json"

class Material:
    def __init__(self, name: str, recipes: Dict[str, Dict[str, float]]):
        """
        name: the raw material (e.g., wood, cobblestone, etc)
        a dict mapping each craftable item with
            "batch_output": how many items you get per craft
            "raw_per_batch": how many raw units the batch consumes
        """
        self.name = name
        self.recipes = recipes

    def raw_units_needed(self, item: str, quantity: int) -> float:
        """
        Calculate how many raw units of material needed to produce the quantity of item, given that you can only craft in multiples of "batch_output"
        Steps:
        1. Look up batch_output and raw_per_batch
        2. Compute number of batches = ceil(quantity / batch_output)
        3. Return batches * raw_per_batch
        """
        if item not in self.recipes:
            raise ValueError(f"Item '{item}' not found in recipes for '{self.name}'.")
        
        entry = self.recipes[item]
        batch_output = int(entry["batch_output"])
        raw_per_batch = float(entry["raw_per_batch"])

        batches_required = math.ceil(quantity / batch_output)
        return batches_required * raw_per_batch
    
class MinecraftCalculator:
    def __init__(self, recipe_file: str = RECIPE_FILE):
        # Attempt to load recipes from JSON. If fails, fall back to internal default.
        try:
            with open(recipe_file, "r") as f:
                recipes_data: Dict[str, Dict[str, Dict[str, float]]] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default structure: { material_name: {item_name: {batch_output, raw_per_batch}}}
            recipes_data = {
                "wood": {
                    "plank": {"batch_output": 4, "raw_per_batch": 1.0},
                    "stick": {"batch_output": 4, "raw_per_batch": 0.25},
                    "door": {"batch_output": 3, "raw_per_batch": 1.5}
                },
                "cobblestone": {
                    "furnace": {"batch_output": 1, "raw_per_batch": 8.0}
                }
            }
        # Instantiate a Material Object for each raw material in the JSON/dict
        self.materials: Dict[str, Material] = {
            mat_name: Material(mat_name, mat_recipes)
            for mat_name, mat_recipes in recipes_data.items()
        }
    
    def list_materials(self) -> None:
        # Print all available raw materials.
        print("\nAvailable raw materials:")
        for name in sorted(self.materials.keys()):
            print(f"  • {name}")
        print()
    
    def list_items_for(self, material_name: str) -> None:
        """
        Print each craftable item for the given material, along with its batch output and raw_per_batch values.
        """
        mat = self.materials[material_name]
        print(f"\nCraftable items for '{material_name}':")
        for item_name, info in mat.recipes.items():
            bo = info["batch_output"]
            rp = info["raw_per_batch"]
            print(f" - {item_name:<10} (makes {bo:<2} at a time, costs {rp} raw units/batch)")
        print()
    
    def run(self) -> None:
        """
        Mani loop: keep prombting the user until they choose to quit
        """
        print("\n===Minecraft Raw-Material Calculator ===")
        while True:
            self.list_materials()
            choice = input("Choose a material (or 'q' to quit): ").strip().lower()
            if choice == "q":
                print("\nGoodbye!")
                return
            if choice not in self.materials:
                print(f" -> '{choice}' isn't a valid material. Try again.\n")
                continue

            mat = self.materials[choice]
            self.list_items_for(choice)

            item = input("Enter item to craft: ").strip().lower()
            if item not in mat.recipes:
                print(f" -> '{item}' not found for material '{choice}'. Returning to menu.\n")
                continue

            qty_str = input("Quantity needed: ").strip()
            if not qty_str.isdigit() or int(qty_str) <= 0:
                print(" -> Quantity must be a postitive integer. Starting over.\n")
                continue
            qty = int(qty_str)

            needed_raw = mat.raw_units_needed(item, qty)
            print(f"\nYou need {needed_raw} raw '{choice}' unit(s) to fract {qty} '{item}'(s).\n")
    
if __name__ == "__main__":
    app = MinecraftCalculator()
    app.run()