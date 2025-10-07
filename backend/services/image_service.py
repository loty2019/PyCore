"""
Image management service
"""
import os
from PIL import Image
from typing import Optional, Tuple
from backend.core.logging import logger
from backend.config import get_settings

settings = get_settings()


class ImageService:
    """Service for image processing and storage"""

    @staticmethod
    def create_thumbnail(image_path: str, thumbnail_path: str = None) -> Optional[str]:
        """
        Create a thumbnail from an image.

        Args:
            image_path: Path to the source image
            thumbnail_path: Optional path for thumbnail (auto-generated if None)

        Returns:
            Path to created thumbnail or None on error
        """
        try:
            # Create thumbnails directory if it doesn't exist
            os.makedirs(settings.THUMBNAILS_PATH, exist_ok=True)

            # Generate thumbnail path if not provided
            if thumbnail_path is None:
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                thumbnail_filename = f"thumb_{name}{ext}"
                thumbnail_path = os.path.join(settings.THUMBNAILS_PATH, thumbnail_filename)

            # Open image
            with Image.open(image_path) as img:
                # Calculate thumbnail size maintaining aspect ratio
                img.thumbnail((settings.THUMBNAIL_SIZE, settings.THUMBNAIL_SIZE), Image.Resampling.LANCZOS)

                # Save thumbnail
                img.save(thumbnail_path, "JPEG", quality=85)

            logger.info(f"Thumbnail created: {thumbnail_path}")
            return thumbnail_path

        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            return None

    @staticmethod
    def get_image_info(image_path: str) -> Optional[dict]:
        """
        Get information about an image file.

        Args:
            image_path: Path to the image

        Returns:
            Dictionary with image info or None on error
        """
        try:
            with Image.open(image_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "file_size": os.path.getsize(image_path)
                }
        except Exception as e:
            logger.error(f"Error getting image info: {e}")
            return None

    @staticmethod
    def delete_image(image_path: str, thumbnail_path: str = None) -> bool:
        """
        Delete an image and its thumbnail.

        Args:
            image_path: Path to the image
            thumbnail_path: Path to thumbnail (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete main image
            if os.path.exists(image_path):
                os.remove(image_path)
                logger.info(f"Image deleted: {image_path}")

            # Delete thumbnail
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                logger.info(f"Thumbnail deleted: {thumbnail_path}")

            return True
        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            return False


# Global image service instance
image_service = ImageService()
