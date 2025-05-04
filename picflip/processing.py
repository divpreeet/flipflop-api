import io
from PIL import Image
from rembg import remove

try:
    import cairosvg
    _SVG_ENABLED = True
except ImportError:
    _SVG_ENABLED = False

def remove_background_bytes(input_bytes: bytes) -> bytes:
    """
    Remove background from image bytes and return new image bytes.
    """
    return remove(input_bytes)

def convert_image_bytes(input_bytes: bytes, fmt: str) -> bytes:
    """
    Convert an image (as bytes) to a new format and return the bytes.
    """
    fmt = fmt.lower()
    supported_formats = {'png', 'jpg', 'jpeg', 'webp'}

    if fmt not in supported_formats:
        raise ValueError(f"Unsupported format: {fmt}")

    # SVG handling
    if _SVG_ENABLED and b'<svg' in input_bytes[:500]:
        png_bytes = cairosvg.svg2png(bytestring=input_bytes)
        if fmt != 'png':
            img = Image.open(io.BytesIO(png_bytes))
            buf = io.BytesIO()
            img.save(buf, format=fmt.upper())
            return buf.getvalue()
        return png_bytes

    # Regular image
    img = Image.open(io.BytesIO(input_bytes))
    if fmt in ('jpg', 'jpeg') and img.mode == 'RGBA':
        img = img.convert('RGB')

    buf = io.BytesIO()
    img.save(buf, format=fmt.upper())
    return buf.getvalue()
