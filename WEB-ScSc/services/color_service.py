import hashlib


class ColorService:
    def __init__(self):
        self.color_cache = {}
    
    def get_color(self, subject_name):
        """
        Generate consistent colors for a subject
        Returns: (bg_color, fg_color) as hex strings
        """
        if subject_name in self.color_cache:
            return self.color_cache[subject_name]
        
        # Generate color from subject name hash
        hash_obj = hashlib.md5(subject_name.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Use first 6 characters for RGB
        r = int(hash_hex[0:2], 16)
        g = int(hash_hex[2:4], 16)
        b = int(hash_hex[4:6], 16)
        
        # Lighten the color for background (pastel effect)
        r = int(r + (255 - r) * 0.6)
        g = int(g + (255 - g) * 0.6)
        b = int(b + (255 - b) * 0.6)
        
        bg_color = f'#{r:02x}{g:02x}{b:02x}'
        
        # Determine foreground color based on luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        fg_color = '#000000' if luminance > 128 else '#FFFFFF'
        
        self.color_cache[subject_name] = (bg_color, fg_color)
        return bg_color, fg_color
    
    def clear_cache(self):
        """Clear the color cache"""
        self.color_cache = {}
