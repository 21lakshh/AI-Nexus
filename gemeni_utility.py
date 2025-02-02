import os 
import json
import google.generativeai as genai

working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, 'config.json')
config_data = json.load(open(config_path))

# loading api key 
api_key = config_data["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

def load_gemeni_pro_model():
    gemeni_pro_model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

    return gemeni_pro_model

def load_gemeni_pro_vision_model(prompt, image):
    gemeni_pro_vision_model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = gemeni_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
