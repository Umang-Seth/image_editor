import cv2
import numpy as np

def adjust_white_point(image, white_point):
    """
    Adjusts the white point by scaling the brighter pixels.
    """
    # Increase the intensity of the bright areas
    scale = 1 + (white_point / 100.0)
    img_float = image.astype(np.float32) * scale
    return np.clip(img_float, 0, 255).astype(np.uint8)

def adjust_highlights(image, highlight_value):
    """
    Adjust the highlights in the image. Affects the brighter areas without overblowing whites.
    """
    highlight_scale = 1 + (highlight_value / 100.0)
    highlights_mask = image > 128  # Only affect bright areas
    img_highlighted = image.copy().astype(np.float32)
    img_highlighted[highlights_mask] *= highlight_scale
    return np.clip(img_highlighted, 0, 255).astype(np.uint8)

def adjust_shadows(image, shadow_value):
    """
    Adjust the shadows by brightening or darkening the darker pixels.
    """
    shadow_scale = 1 + (shadow_value / 100.0)
    shadows_mask = image < 128  # Only affect dark areas
    img_shadowed = image.copy().astype(np.float32)
    img_shadowed[shadows_mask] *= shadow_scale
    return np.clip(img_shadowed, 0, 255).astype(np.uint8)

def adjust_black_point(image, black_point):
    """
    Adjusts the black point by making dark pixels darker.
    """
    black_point_shift = black_point * 2.55  # Scale from [0, 100] to [0, 255]
    img_adjusted = np.clip(image.astype(np.float32) - black_point_shift, 0, 255)
    return img_adjusted.astype(np.uint8)

def apply_curve_adjustment(image, scale):
    """
    Applies a smooth curve adjustment for highlights and shadows.
    scale > 0 brightens the image (shadows)
    scale < 0 darkens the image (highlights)
    """
    scale = scale / 100.0
    lut = np.array([((i / 255.0) ** (1.0 + scale) * 255) for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, lut)

def adjust_highlights(image, highlight_value):
    """
    Adjust highlights using a tone-mapping approach (S-curve adjustment).
    """
    if highlight_value >= 0:
        return image
    return apply_curve_adjustment(image, highlight_value)

def adjust_shadows(image, shadow_value):
    """
    Adjust shadows using a tone-mapping approach (S-curve adjustment).
    """
    if shadow_value <= 0:
        return image
    return apply_curve_adjustment(image, shadow_value)
def on_trackbar_change(val):
    pass  # No action needed for trackbar callback

# Load image
img = cv2.imread('../examples/Eagle_in_Flight.jpg')

# Create window for the trackbars
cv2.namedWindow('Image Editor')

# Create trackbars for white point, highlights, shadows, and black point
cv2.createTrackbar('White Point', 'Image Editor', 50, 100, on_trackbar_change)
cv2.createTrackbar('Highlights', 'Image Editor', 50, 100, on_trackbar_change)
cv2.createTrackbar('Shadows', 'Image Editor', 50, 100, on_trackbar_change)
cv2.createTrackbar('Black Point', 'Image Editor', 50, 100, on_trackbar_change)

while True:
    # Get current positions of trackbars
    white_point = cv2.getTrackbarPos('White Point', 'Image Editor') - 50
    highlights = cv2.getTrackbarPos('Highlights', 'Image Editor') - 50
    shadows = cv2.getTrackbarPos('Shadows', 'Image Editor') - 50
    black_point = cv2.getTrackbarPos('Black Point', 'Image Editor') - 50

    # Apply adjustments
    adjusted_img = adjust_white_point(img.copy(), white_point)
    adjusted_img = adjust_highlights(adjusted_img, highlights)
    adjusted_img = adjust_shadows(adjusted_img, shadows)
    adjusted_img = adjust_black_point(adjusted_img, black_point)

    # Display the adjusted image
    cv2.imshow('Image Editor', adjusted_img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()