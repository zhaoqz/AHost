import urllib.request
import json
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
        
        file_url = f"https://{config.domain_name}/{slug}"
        
        payload = {
            "files": [file_url]
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        try:
            # Since this is an async method but urllib is synchronous, 
            # in a high-load async app we might want to run this in a thread executor.
            # But for this low-frequency admin action, blocking briefly is acceptable.
            # Or we can just wrap it in a simple try/except block.
            
            with urllib.request.urlopen(req) as response:
                response_body = response.read().decode('utf-8')
                result = json.loads(response_body)
                
                if result.get("success"):
                    logger.info(f"Successfully purged Cloudflare cache for {file_url}")
                else:
                    logger.error(f"Failed to purge Cloudflare cache: {result.get('errors')}")
                    
        except urllib.error.HTTPError as e:
            logger.error(f"Cloudflare API error: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            logger.error(f"Exception during Cloudflare cache purge: {e}")
