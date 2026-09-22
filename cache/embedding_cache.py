import os
import json


class EmbeddingCache:
    def __init__(self, cache_file = "cache/embeddings.json"):
        self.cache_file = cache_file
        self.cache = {}

        os.makedirs("cache", exist_ok=True)

    def load(self):
        if not os.path.exists(self.cache_file):
            return

        try:
            with open(self.cache_file, "r") as file:
                self.cache = json.load(file)

        except (json.JSONDecodeError, OSError):
            self.cache = {}
    

    def save(self):
        with open(self.cache_file, "w") as file:
            json.dump(self.cache, file, indent=4)

    def get(self, text):
        return self.cache.get(text)

    def set(self, text, embedding):
        self.cache[text] = embedding
        self.save()