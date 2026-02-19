import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_text_video(text, output_filename="output_video.mp4", duration_sec=5, fps=24):
    # Video settings
    width, height = 1920, 1080
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    # Create a base frame (Black background)
    # Using PIL to handle text because it supports better fonts/alignment than OpenCV
    img_pil = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img_pil)
    
    # Load a font (defaults to a basic one if path isn't found)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()

    # Calculate text position (Centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((width - text_width) // 2, (height - text_height) // 2)

    # Draw the text onto the image
    draw.text(position, text, font=font, fill=(255, 255, 255))

    # Convert PIL image to OpenCV format (numpy array)
    frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Write the frame to the video for the specified duration
    for _ in range(duration_sec * fps):
        video.write(frame)

    video.release()
    print(f"Success! Video saved as {output_filename}")

# Usage
user_input = input("Enter the text you want in the video: ")
create_text_video(user_input)