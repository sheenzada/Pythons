import json
import os
from typing import List, Dict, Any, Optional

class Ingredient:
    """Represents a standardized ingredient entity."""
    def __init__(self, name: str):
        self.name: str = name.strip().lower()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Recipe:
    """Represents a rich Recipe model with matching capability."""
    def __init__(self, name: str, cuisine: str, prep_time: int, difficulty: str, ingredients: List[str], instructions: List[str]):
        self.name: str = name
        self.cuisine: str = cuisine
        self.prep_time_mins: int = prep_time
        self.difficulty: str = difficulty
        self.required_ingredients: List[Ingredient] = [Ingredient(ing) for ing in ingredients]
        self.instructions: List[str] = instructions

    def calculate_match_score(self, available_ingredients: List[Ingredient]) -> float:
        """Calculates the match percentage based on available ingredients."""
        if not self.required_ingredients:
            return 0.0
        
        available_set = set(available_ingredients)
        matched_count = sum(1 for ing in self.required_ingredients if ing in available_set)
        
        return round((matched_count / len(self.required_ingredients)) * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the object for clean console or API output."""
        return {
            "name": self.name,
            "cuisine": self.cuisine,
            "prep_time_mins": self.prep_time_mins,
            "difficulty": self.difficulty,
            "ingredients": [ing.name for ing in self.required_ingredients],
            "instructions": self.instructions
        }


class RecipeEngine:
    """Core Core Business Logic Layer to handle ingestion and searching."""
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.recipes: List[Recipe] = []
        self._load_database()

    def _load_database(self) -> None:
        """Loads and parses the JSON database with error boundaries."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Critical Error: Database file not found at {self.db_path}")
        
        try:
            with open(self.db_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    self.recipes.append(Recipe(
                        name=item['name'],
                        cuisine=item['cuisine'],
                        prep_time=item['prep_time_mins'],
                        difficulty=item['difficulty'],
                        ingredients=item['ingredients'],
                        instructions=item['instructions']
                    ))
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Database Corruption Error: Failed to parse schema. Details: {e}")

    def generate_recommendations(self, user_inputs: List[str], min_threshold: float = 40.0) -> List[Dict[str, Any]]:
        """
        Filters and ranks recipes using a scoring matrix.
        Returns a prioritized list of matching recipes.
        """
        available_ingredients = [Ingredient(ing) for ing in user_inputs]
        scored_recipes = []

        for recipe in self.recipes:
            score = recipe.calculate_match_score(available_ingredients)
            if score >= min_threshold:
                recipe_data = recipe.to_dict()
                recipe_data['match_score'] = score
                scored_recipes.append(recipe_data)

        # Sort dynamically by match score descending, then by prep time ascending
        return sorted(scored_recipes, key=lambda x: (-x['match_score'], x['prep_time_mins']))


# --- Presentation Layer (CLI Wrapper for Evaluation) ---
if __name__ == "__main__":
    # Initialize the engine
    DB_FILE = "recipes_db.json"
    
    print("=" * 60)
    print("        ADVANCED COGNITIVE RECIPE GENERATION ENGINE       ")
    print("=" * 60)
    
    try:
        engine = RecipeEngine(db_path=DB_FILE)
        
        # Simulating User Interface Input
        raw_input = input("\nEnter available ingredients (comma-separated, e.g., rice, garlic, egg): ")
        user_ingredients = [item.strip() for item in raw_input.split(",") if item.strip()]
        
        if not user_ingredients:
            print("[!] Empty inventory submitted. Execution aborted.")
            exit()

        print(f"\n[INFO] Processing inventory: {user_ingredients}")
        recommendations = engine.generate_recommendations(user_ingredients, min_threshold=30.0)
        
        print("\n" + "="*20 + " MATCH RESULTS " + "="*20)
        if not recommendations:
            print("[-] No recipes matched your inventory threshold.")
        else:
            for idx, recipe in enumerate(recommendations, 1):
                print(f"\n{idx}. {recipe['name']} [{recipe['cuisine']}]")
                print(f"   -> Match Score: {recipe['match_score']}%")
                print(f"   -> Complexity: {recipe['difficulty']} | Prep Time: {recipe['prep_time_mins']} mins")
                print("   -> Required Base: " + ", ".join(recipe['ingredients']))
                print("   -> Execution Steps:")
                for step_num, step in enumerate(recipe['instructions'], 1):
                    print(f"      Step {step_num}: {step}")
                print("-" * 50)
                
    except Exception as error:
        print(f"\n[CRITICAL FAILURE] {error}")