import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class TelexService:
    
    def __init__(self):
        self.api_url = os.getenv("TELEX_API_URL", "https://api.telex.im")
        self.bot_token = os.getenv("TELEX_BOT_TOKEN")
    
    async def send_message(self, channel_id: str, message: str):
        """Send message to Telex channel"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/messages",
                    headers={
                        "Authorization": f"Bearer {self.bot_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "channel_id": channel_id,
                        "text": message
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error sending Telex message: {e}")
            return None
    
    async def register_webhook(self, webhook_url: str):
        """Register webhook with Telex"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/webhooks",
                    headers={
                        "Authorization": f"Bearer {self.bot_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "url": webhook_url,
                        "events": ["message.created"]
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error registering webhook: {e}")
            return None