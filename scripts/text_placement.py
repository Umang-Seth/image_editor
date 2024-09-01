import cv2
import numpy as np

def get_text_size(text, font, font_scale, thickness):
    return cv2.getTextSize(text, font, font_scale, thickness)[0]

img = cv2.imread('../examples/Eagle_in_Flight.jpg', cv2.IMREAD_UNCHANGED)
image_text = img.copy()
image_height, image_width = img.shape[:2]

grid_height = image_height // 3
grid_width = image_width // 3

center_bottom_x1 = grid_width
center_bottom_y1 = 2 * grid_height

center_bottom_x2 = 2 * grid_width
center_bottom_y2 = image_height

text_region_width = grid_width
text_region_height = grid_height

text = 'DAY 356'
text_pr365 = '547.285580770870.1894.75.1628.0.1.3.168.30.10'
text_location = (10, 10)
font_thickness = 2
font_scale = 1
font = cv2.FONT_HERSHEY_SIMPLEX
font_color = (255, 255, 255)
line_spacing = 15 

text_lines = []
current_line = ""


for char in text_pr365:
    
    test_line = current_line + char
    text_width, _ = get_text_size(test_line, font, font_scale, font_thickness)
    
    
    if text_width <= text_region_width:
        current_line = test_line
    else:
        text_lines.append(current_line.strip())
        current_line = char


if current_line:
    text_lines.append(current_line.strip())

text_block_height = sum([get_text_size(line, font, font_scale, font_thickness)[1] for line in text_lines]) + line_spacing * (len(text_lines) - 1)


while text_block_height > text_region_height and font_scale > 0.1:
    font_scale -= 0.1
    text_block_height = sum([get_text_size(line, font, font_scale, font_thickness)[1] for line in text_lines]) + line_spacing * (len(text_lines) - 1)


y_offset = center_bottom_y2 - 10 

for line in reversed(text_lines): 
    
    text_width, text_height = get_text_size(line, font, font_scale, font_thickness)
    x_offset = center_bottom_x1 + (text_region_width - text_width) // 2
    
    cv2.putText(image_text, line, (x_offset, y_offset), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    
    y_offset -= text_height + line_spacing


(text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
print(text_width, text_height)

text_img = np.zeros((round((text_height + text_width)/1.414), text_width + round((text_height)/1.414), 3), dtype=np.uint8)


cv2.putText(text_img, text, (0, text_height), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)


point_of_rotation = (text_width, 0)
rotation_matrix = cv2.getRotationMatrix2D(point_of_rotation, 45, 1)


rotated_text_img = cv2.warpAffine(text_img, rotation_matrix, (text_img.shape[1], text_img.shape[0]))
cropped_img = rotated_text_img[0:round((text_height + text_width)/1.414),(text_width + round((text_height)/1.414)) - round((text_height + text_width)/1.414):text_width + round((text_height)/1.414)]

x_offset, y_offset = text_location


y1, y2 = y_offset, y_offset + cropped_img.shape[0]
x1, x2 = x_offset, x_offset + cropped_img.shape[1]
print(x1,x2,y1,y2)

if y2 <= image_text.shape[0] and x2 <= image_text.shape[1]:

    mask = cropped_img[:, :, 0] > 150
    image_text[y1:y2, x1:x2][mask] = cropped_img[mask]


cv2.imshow('Image', img)
cv2.imshow('Image with Rotated Text', image_text)

cv2.waitKey(0)
cv2.destroyAllWindows()
