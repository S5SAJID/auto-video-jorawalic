import requests
from typing import Optional, Dict, Any

class GiphyClient:
    """
    A lightweight wrapper for the Giphy API providing clean access to common endpoints.
    """
    BASE_URL = "https://api.giphy.com/v1/gifs"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}
        params["api_key"] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}" if endpoint else self.BASE_URL
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search(self, q: str, limit: int = 25, offset: int = 0, rating: str = "g", lang: str = "en") -> list[Dict[str, str]]:
        """Search all GIPHY GIFs for a word or phrase. Returns a list of dicts with 'url', 'title', and 'description'."""
        params = {"q": q, "limit": limit, "offset": offset, "rating": rating, "lang": lang}
        response = self._request("search", params)
        
        # Extract only the gif URL (medium size), title, and description
        results = []
        for gif in response.get("data", []):
            gif_data = {
                "url": gif.get("images", {}).get("fixed_height", {}).get("url", ""),
                "title": gif.get("title", ""),
                "slug": gif.get("slug", "") 
            }
            results.append(gif_data)
        
        return results

    def trending(self, limit: int = 25, offset: int = 0, rating: str = "g") -> Dict[str, Any]:
        """Fetch the latest trending GIFs."""
        params = {"limit": limit, "offset": offset, "rating": rating}
        return self._request("trending", params)

    def random(self, tag: Optional[str] = None, rating: str = "g") -> Dict[str, Any]:
        """Returns a random GIF, optionally filtered by a specific tag."""
        params = {"tag": tag, "rating": rating}
        return self._request("random", params)

    def translate(self, s: str, rating: str = "g") -> Dict[str, str]:
        """The translate engine provides a way to convert words and phrases to the perfect GIF.
        Returns a dict with 'url', 'title', 'id', and 'slug'."""
        params = {"s": s, "rating": rating}
        response = self._request("translate", params)
        
        # Extract essential fields from the single GIF result
        gif = response.get("data", {})
        return {
            "url": gif.get("images", {}).get("fixed_height", {}).get("url", ""),
            "title": gif.get("title", ""),
            "id": gif.get("id", ""),
            "slug": gif.get("slug", "")
        }

    def get_by_id(self, gif_id: str) -> Dict[str, Any]:
        """Returns a GIF object based on its unique ID."""
        return self._request(gif_id)
