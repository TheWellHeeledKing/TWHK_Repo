from PIL import Image

# Path to your image
input_path = r"C:\Users\Mike\Software\Python\TWHK_Repository\TWHK_logo.png"
output_path = r"C:\Users\Mike\Software\Python\TWHK_Repository\TWHK_logo_icon.png"

# Open the image
image = Image.open(input_path)

# Resize to 32x32 pixels using LANCZOS (previously ANTIALIAS)
resized_image = image.resize((32, 32), Image.Resampling.LANCZOS)

# Save the resized image
resized_image.save(output_path)

print(f"Image resized and saved at {output_path}")
