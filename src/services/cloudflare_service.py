import httpx
from src.config import config
from src.utils.logger import logger

class CloudflareService:
    @staticmethod
    async def purge_cache(slug: str):
        """
        Purge Cloudflare cache for the given app slug.
        Constructs the URL as https://{domain_name}/{slug}
        """
        if not config.cf_zone_id or not config.cf_api_token:
            logger.warning("Cloudflare credentials not configured. Skipping cache purge.")
            return

        url = f"https://api.cloudflare.com/client/v4/zones/{config.cf_zone_id}/purge_cache"
        headers = {
            "Authorization": f"Bearer {config.cf_api_token}",
            "Content-Type": "application/json"
        }
        
        # Construct the file URL to purge
        # Assuming the app is accessed via https://domain/slug
        # If it's a specific file like index.html, we might need to purge that too or just the path
        # User example: "https://a.104800.xyz/game.html"
        # Our apps are at /slug which serves index.html. 
        # Let's purge both /slug and /slug/ just in case, or whatever the canonical URL is.
        # Based on user request, they want to update "html file".
        # If the user accesses /slug, it's the html content.
        
        file_url = f"https://{config.domain_name}/{slug}"
        
        payload = {
            "files": [file_url]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"Successfully purged Cloudflare cache for {file_url}")
                else:
                    logger.error(f"Failed to purge Cloudflare cache: {result.get('errors')}")
            else:
                logger.error(f"Cloudflare API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Exception during Cloudflare cache purge: {e}")
