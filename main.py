import requests
import base64
import os
from PIL import Image
from io import BytesIO

RETRO_API_KEY = os.getenv("RETRO_API_KEY")

def generate_image(
        api_key: str = RETRO_API_KEY,
        output_image_path: str = "output/fox.gif",
        prompt: str = "a man with the head of a fox carrying a surfboard",
        prompt_style: str = "animation_four_angle_walking", # for gif animations, can be modified
        model: str = "RD_FLUX",
        width: int = 48,
        height: int = 48,
        num_images: int = 1,
):
	
	url = "https://api.retrodiffusion.ai/v1/inferences"
	method = "POST"
	headers = {
        "X-RD-Token": api_key,
    }
	payload = {
        "prompt": prompt,
        "prompt_style": prompt_style,
        "model": model,
        "width": width,
        "height": height,
        "num_images": num_images,
	}
    
	print(f"Generating image for prompt: '{prompt}'")
	response = requests.request(method, url, headers=headers, json=payload)
	
	if response.status_code == 200:
		data = response.json()
		
		print(f"Credit cost: {data.get('credit_cost', 'unknown')}")
		print(f"Remaining credits: {data.get('remaining_credits', 'unknown')}")
		
		base64_images = data.get("base64_images", [])
		
		if base64_images:
			
			with open(output_image_path, "wb") as out_file:
				out_file.write(base64.b64decode(base64_images[0]))
			print(f"Image generated and saved to {output_image_path}")
		else:
			print("No images returned by the API.")
	else:
		print(f"Request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
	generate_image()



