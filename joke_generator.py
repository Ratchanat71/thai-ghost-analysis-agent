#!/usr/bin/env python3
"""
Random Joke Generator using external APIs
Supports multiple joke APIs and formats
"""

import requests
import json
from typing import Dict, List, Any, Optional
from enum import Enum
import random


class JokeAPI(Enum):
    """Available joke API sources"""
    OFFICIAL_JOKE_API = "https://official-joke-api.appspot.com"
    JOKES_API = "https://v2.jokeapi.dev"
    RANDOM_JOKES = "https://api.api-ninjas.com/v1/jokes"


class JokeGenerator:
    """Generate random jokes from various external APIs"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize joke generator
        
        Args:
            api_key: Optional API key for services that require authentication
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JokeGeneratorApp/1.0'
        })
    
    def get_joke_from_official_api(self) -> Dict[str, Any]:
        """
        Get a random joke from Official Joke API
        Returns both single and multiple part jokes
        
        Returns:
            Dictionary containing joke data
        """
        try:
            url = f"{JokeAPI.OFFICIAL_JOKE_API.value}/random_joke"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return {
                "source": "Official Joke API",
                "type": "single",
                "setup": data.get("setup", ""),
                "punchline": data.get("punchline", ""),
                "full_joke": f"{data.get('setup', '')} {data.get('punchline', '')}",
                "id": data.get("id"),
                "status": "success"
            }
        except requests.RequestException as e:
            return {
                "source": "Official Joke API",
                "status": "error",
                "error": str(e)
            }
    
    def get_joke_from_jokeapi(self, category: str = "any") -> Dict[str, Any]:
        """
        Get a random joke from JokeAPI with category support
        
        Args:
            category: Joke category (any, programming, knock-knock, general, etc.)
        
        Returns:
            Dictionary containing joke data
        """
        try:
            url = f"{JokeAPI.JOKES_API.value}/joke/{category}"
            params = {
                "format": "json",
                "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit"
            }
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("type") == "single":
                return {
                    "source": "JokeAPI",
                    "type": "single",
                    "joke": data.get("joke", ""),
                    "category": data.get("category", ""),
                    "id": data.get("id"),
                    "status": "success"
                }
            else:
                return {
                    "source": "JokeAPI",
                    "type": "two-part",
                    "setup": data.get("setup", ""),
                    "delivery": data.get("delivery", ""),
                    "full_joke": f"{data.get('setup', '')} {data.get('delivery', '')}",
                    "category": data.get("category", ""),
                    "id": data.get("id"),
                    "status": "success"
                }
        except requests.RequestException as e:
            return {
                "source": "JokeAPI",
                "status": "error",
                "error": str(e)
            }
    
    def get_joke_from_ninja_api(self) -> Dict[str, Any]:
        """
        Get a random joke from API Ninjas
        
        Returns:
            Dictionary containing joke data
        """
        try:
            url = f"{JokeAPI.RANDOM_JOKES.value}"
            headers = {}
            if self.api_key:
                headers["X-Api-Key"] = self.api_key
            
            response = self.session.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                joke = data[0]
            else:
                joke = data
            
            return {
                "source": "API Ninjas",
                "type": "single",
                "joke": joke.get("joke", ""),
                "status": "success"
            }
        except requests.RequestException as e:
            return {
                "source": "API Ninjas",
                "status": "error",
                "error": str(e)
            }
    
    def get_random_joke(self) -> Dict[str, Any]:
        """
        Get a random joke from a random API
        
        Returns:
            Dictionary containing joke data
        """
        apis = [
            self.get_joke_from_official_api,
            self.get_joke_from_jokeapi,
            self.get_joke_from_ninja_api
        ]
        
        selected_api = random.choice(apis)
        return selected_api()
    
    def get_jokes_batch(self, count: int = 5, api_choice: str = "random") -> List[Dict[str, Any]]:
        """
        Get multiple jokes at once
        
        Args:
            count: Number of jokes to retrieve
            api_choice: Which API to use (random, official, jokeapi, ninja)
        
        Returns:
            List of joke dictionaries
        """
        jokes = []
        
        for i in range(count):
            if api_choice == "random":
                joke = self.get_random_joke()
            elif api_choice == "official":
                joke = self.get_joke_from_official_api()
            elif api_choice == "jokeapi":
                joke = self.get_joke_from_jokeapi()
            elif api_choice == "ninja":
                joke = self.get_joke_from_ninja_api()
            else:
                joke = self.get_random_joke()
            
            jokes.append(joke)
        
        return jokes
    
    def get_jokes_by_category(self, category: str = "programming") -> Dict[str, Any]:
        """
        Get jokes filtered by category (using JokeAPI)
        
        Args:
            category: Joke category (programming, knock-knock, general, etc.)
        
        Returns:
            Dictionary containing joke data
        """
        return self.get_joke_from_jokeapi(category=category)
    
    def get_programming_joke(self) -> Dict[str, Any]:
        """Get a programming-related joke"""
        return self.get_joke_from_jokeapi(category="programming")
    
    def get_knock_knock_joke(self) -> Dict[str, Any]:
        """Get a knock-knock joke"""
        return self.get_joke_from_jokeapi(category="knock-knock")


class JokeFormatterter:
    """Format and display jokes in different styles"""
    
    @staticmethod
    def format_text(joke: Dict[str, Any]) -> str:
        """Format joke as plain text"""
        if joke.get("status") == "error":
            return f"❌ Error: {joke.get('error')}"
        
        if joke.get("type") == "single":
            return f"😂 {joke.get('joke', joke.get('full_joke', ''))}"
        else:
            setup = joke.get("setup", "")
            punchline = joke.get("punchline", joke.get("delivery", ""))
            return f"Q: {setup}\nA: {punchline}"
    
    @staticmethod
    def format_json(joke: Dict[str, Any]) -> str:
        """Format joke as JSON"""
        return json.dumps(joke, indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_markdown(joke: Dict[str, Any]) -> str:
        """Format joke as Markdown"""
        if joke.get("status") == "error":
            return f"❌ **Error**: {joke.get('error')}"
        
        source = joke.get("source", "Unknown")
        output = f"## 😂 Joke from {source}\n\n"
        
        if joke.get("type") == "single":
            output += f"> {joke.get('joke', joke.get('full_joke', ''))}\n"
        else:
            output += f"**Q:** {joke.get('setup', '')}\n\n"
            output += f"**A:** {joke.get('punchline', joke.get('delivery', ''))}\n"
        
        return output
    
    @staticmethod
    def format_html(joke: Dict[str, Any]) -> str:
        """Format joke as HTML"""
        if joke.get("status") == "error":
            return f"<p>❌ Error: {joke.get('error')}</p>"
        
        source = joke.get("source", "Unknown")
        html = f"<div class='joke'>\n<h3>😂 Joke from {source}</h3>\n"
        
        if joke.get("type") == "single":
            html += f"<p>{joke.get('joke', joke.get('full_joke', ''))}</p>\n"
        else:
            html += f"<p><strong>Q:</strong> {joke.get('setup', '')}</p>\n"
            html += f"<p><strong>A:</strong> {joke.get('punchline', joke.get('delivery', ''))}</p>\n"
        
        html += "</div>"
        return html


# CLI Interface
def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Random Joke Generator")
    parser.add_argument("--count", type=int, default=1, help="Number of jokes to generate")
    parser.add_argument("--format", choices=["text", "json", "markdown", "html"], 
                       default="text", help="Output format")
    parser.add_argument("--api", choices=["random", "official", "jokeapi", "ninja"], 
                       default="random", help="Which API to use")
    parser.add_argument("--category", type=str, help="Joke category (for JokeAPI)")
    parser.add_argument("--api-key", type=str, help="API key for services that require it")
    
    args = parser.parse_args()
    
    generator = JokeGenerator(api_key=args.api_key)
    formatter = JokeFormatterter()
    
    if args.count == 1:
        if args.category:
            joke = generator.get_jokes_by_category(args.category)
        else:
            if args.api == "random":
                joke = generator.get_random_joke()
            elif args.api == "official":
                joke = generator.get_joke_from_official_api()
            elif args.api == "jokeapi":
                joke = generator.get_joke_from_jokeapi()
            else:
                joke = generator.get_joke_from_ninja_api()
        
        if args.format == "json":
            print(formatter.format_json(joke))
        elif args.format == "markdown":
            print(formatter.format_markdown(joke))
        elif args.format == "html":
            print(formatter.format_html(joke))
        else:
            print(formatter.format_text(joke))
    else:
        jokes = generator.get_jokes_batch(count=args.count, api_choice=args.api)
        for i, joke in enumerate(jokes, 1):
            print(f"\n--- Joke {i} ---")
            if args.format == "json":
                print(formatter.format_json(joke))
            elif args.format == "markdown":
                print(formatter.format_markdown(joke))
            elif args.format == "html":
                print(formatter.format_html(joke))
            else:
                print(formatter.format_text(joke))


if __name__ == "__main__":
    main()
