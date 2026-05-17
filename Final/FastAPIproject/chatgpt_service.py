import json
import os
from openai import OpenAI

# The API key provided by the user
API_KEY = "sk-ayYW7yrMMRZiYNlmvtSKPRVGj9kJmnJlY7YGUE5RkOioI39M"

def get_crop_market_insights(district, taluk, crops_list):
    """
    Given a list of crops and a location, query the ChatGPT API to get recent
    sales trends and current approximate market prices.
    Returns a dictionary mapping crop names to dictionaries with 'sales_trend' and 'market_price'.
    If the API call fails, returns an empty dictionary.
    """
    if not crops_list:
        return {}

    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.chatanywhere.tech/v1"
        )
        
        # Enforce JSON output mode by specifying the schema structure implicitly
        prompt_content = f"""
        Provide agricultural market insights for the following crops specifically in the region of {taluk}, {district}, India (or generally in India if region-specific data is absent). For each crop, provide:
        - A brief 1-2 sentence summary of recent sales trends over the past few years.
        - An approximate current market price (e.g., in INR per quintal or ton).
        
        Crops:
        {', '.join(crops_list)}
        
        Output valid JSON exactly matching this format:
        {{
            "crop_insights": [
                {{
                    "crop": "CROP_NAME",
                    "sales_trend": "Trend description...",
                    "market_price": "Price estimate..."
                }}, ...
            ]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Using 3.5 turbo to be faster and cheaper, or gpt-4 if needed. The user didn't specify, standard is 3.5.
            messages=[
                {"role": "system", "content": "You are an expert agricultural economist providing precise data formatted as JSON."},
                {"role": "user", "content": prompt_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        raw_json = response.choices[0].message.content
        data = json.loads(raw_json)
        
        insights_map = {}
        if "crop_insights" in data:
            for item in data["crop_insights"]:
                # Normalizing the crop name case to match easily
                crop_name = item.get("crop", "").upper().strip()
                insights_map[crop_name] = {
                    "sales_trend": item.get("sales_trend", "Data unavailable"),
                    "market_price": item.get("market_price", "Data unavailable")
                }
                
        return insights_map
        
    except Exception as e:
        print(f"Failed to fetch market insights from ChatGPT: {e}")
        return {}

def get_crop_growing_info(crops_list):
    """
    Given a list of crops, query the ChatGPT API to get growing instructions
    and the best seed sowing time for each crop in India.
    Returns a dictionary mapping crop names to growing info.
    """
    if not crops_list:
        return {}

    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.chatanywhere.tech/v1"
        )

        prompt_content = f"""
        For each of the following crops commonly grown in India, provide:
        1. A brief description of how it is grown (2-3 sentences).
        2. The best time to sow seeds (e.g., month or season).

        Crops: {', '.join(crops_list)}

        Output valid JSON exactly in this format:
        {{
            "crop_info": [
                {{
                    "crop": "CROP_NAME",
                    "how_to_grow": "Brief growing description...",
                    "sowing_time": "Best sowing month/season..."
                }}
            ]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Indian agricultural advisor. Provide concise, accurate crop info as JSON."},
                {"role": "user", "content": prompt_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        raw_json = response.choices[0].message.content
        data = json.loads(raw_json)

        info_map = {}
        if "crop_info" in data:
            for item in data["crop_info"]:
                crop_name = item.get("crop", "").strip()
                info_map[crop_name.upper()] = {
                    "how_to_grow": item.get("how_to_grow", "Information unavailable"),
                    "sowing_time": item.get("sowing_time", "Information unavailable")
                }

        return info_map

    except Exception as e:
        print(f"Failed to fetch crop growing info from ChatGPT: {e}")
        return {}
