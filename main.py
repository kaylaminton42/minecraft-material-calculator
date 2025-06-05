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
    
class MinecraftCaluclator:
    def __init__(self, recipe_file: str = RECIPE_FILE)
        # Attempt to load recipes from JSON. If fails, fall back to internal default.
        try:
            with open(recipe_file, "r") as f:
                recipes_data: Dict[str, Dict[str, Dict[str, float]]] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default structure: { material_name: {item_name: {batch_output, raw_per_batch}}}
            recipes_data = {
                
            }