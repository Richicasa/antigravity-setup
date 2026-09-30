import os
import ssl
import urllib.request
import urllib.parse
from PIL import Image

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def download_image(url_or_keyword, output_path, min_width=1600):
    """
    Downloads an image from a direct URL or fetches a curated high-res 
    editorial photograph from Unsplash based on keywords.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    if url_or_keyword.startswith("http://") or url_or_keyword.startswith("https://"):
        img_url = url_or_keyword
    else:
        # Generate high-res Unsplash search direct source URL
        clean_keyword = urllib.parse.quote(url_or_keyword)
        # Using Unsplash high-res endpoint
        img_url = f"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w={min_width}&auto=format&fit=crop&q=85"
        # If specific keywords are passed, we can map to curated collections or use search
        # For general keywords, let's use direct query or fallback
        if any(k in url_or_keyword.lower() for k in ["tech", "ai", "software", "code", "cyber"]):
            img_url = f"https://images.unsplash.com/photo-1518770660439-4636190af475?w={min_width}&auto=format&fit=crop&q=85"
        elif any(k in url_or_keyword.lower() for k in ["luxury", "real estate", "building", "house", "apartment", "residence"]):
            img_url = f"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w={min_width}&auto=format&fit=crop&q=85"
        elif any(k in url_or_keyword.lower() for k in ["nature", "mountain", "forest", "landscape"]):
            img_url = f"https://images.unsplash.com/photo-1506744038136-46273834b3fb?w={min_width}&auto=format&fit=crop&q=85"
        elif any(k in url_or_keyword.lower() for k in ["finance", "money", "business", "minimal"]):
            img_url = f"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w={min_width}&auto=format&fit=crop&q=85"
        else:
            # High-aesthetic modern architecture/minimalist texture
            img_url = f"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w={min_width}&auto=format&fit=crop&q=85"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    req = urllib.request.Request(img_url, headers=headers)
    ctx = get_ssl_context()
    with urllib.request.urlopen(req, context=ctx) as response, open(output_path, "wb") as f:
        f.write(response.read())
        
    return output_path

def crop_to_exact_aspect(image_path, target_width_in, target_height_in, output_path=None):
    """
    Crops image to exact aspect ratio without distortion.
    """
    if output_path is None:
        output_path = image_path
        
    target_ratio = target_width_in / target_height_in
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img_w, img_h = img.size
        img_ratio = img_w / img_h
        
        if img_ratio > target_ratio:
            new_w = int(img_h * target_ratio)
            left = (img_w - new_w) // 2
            box = (left, 0, left + new_w, img_h)
        else:
            new_h = int(img_w / target_ratio)
            top = (img_h - new_h) // 2
            box = (0, top, img_w, top + new_h)
            
        cropped = img.crop(box)
        cropped.save(output_path, quality=95)
        
    return output_path
