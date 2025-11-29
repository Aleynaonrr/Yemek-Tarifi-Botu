from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import List
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient


@dataclass
class Recipe:
    name: str
    url: str
    search_term: str
    timestamp: str = field(default_factory=lambda: str(datetime.datetime.now()))


class IDataCollector(ABC):
    @abstractmethod
    def scrape_recipes(self, ingredient: str) -> List[Recipe]:
        pass


class RecipeBot(IDataCollector):
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.base_url = "https://www.nefisyemektarifleri.com/?s="

    def scrape_recipes(self, ingredient: str) -> List[Recipe]:
        print(f"Bot is starting browser... Searching for '{ingredient}'")
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=self.service, options=options)

        results = []
        try:
            driver.get(self.base_url + ingredient)
            time.sleep(3)

            cards = driver.find_elements(By.CSS_SELECTOR, "a.c-entry")
            print(f"Found {len(cards)} recipes. Processing the first 3...")

            for card in cards[:3]:
                recipe_url = card.get_attribute("href")

                try:
                    title_element = card.find_element(By.CLASS_NAME, "c-entry__title")
                    recipe_name = title_element.text
                except:
                    recipe_name = card.get_attribute("title")
                    if not recipe_name:
                        recipe_name = card.text

                if recipe_name and recipe_url:
                    recipe_name = recipe_name.strip()

                    new_recipe = Recipe(
                        name=recipe_name,
                        url=recipe_url,
                        search_term=ingredient
                    )
                    results.append(new_recipe)
                    print(f" Found: {recipe_name}")

        except Exception as e:
            print(f"An error occured: {e}")
        finally:
            driver.quit()

        return results


class DatabaseManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client["RecipeProjectDB"]
            self.collection = self.db["Recipes"]
            print("Connected to MongoDB.")
        except Exception as e:
            print(f"Database connection failed: {e}")

    def save_recipes(self, recipes: List[Recipe]):
        if not recipes:
            print("No recipes to save.")
            return

        print(f"Saving {len(recipes)} recipes to MongoDB...")

        for recipe in recipes:
            recipe_data = asdict(recipe)
            if self.collection.find_one({"url": recipe_data["url"]}) is None:
                self.collection.insert_one(recipe_data)
                print(f"   [SAVED]: {recipe_data['name']}")
            else:
                print(f"   [SKIPPED]: {recipe_data['name']} (Already exists)")


if __name__ == "__main__":
    bot = RecipeBot()

    print("--- TEST MODE: PRINT ONLY (NO DATABASE) ---")
    user_ingredient = input("Enter an ingredient to search (e.g., patates): ")

    found_recipes = bot.scrape_recipes(user_ingredient)

    print("\n" + "=" * 40)
    print(f"RESULTS: {len(found_recipes)} recipes found.")
    print("=" * 40)

    for recipe in found_recipes:
        print(f"Name : {recipe.name}")
        print(f"URL  : {recipe.url}")
        print("-" * 20)