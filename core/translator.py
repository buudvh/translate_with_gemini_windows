import requests
import json

def create_prompt(text, promptType = "0"):
    if promptType == "0": #TRANSLATE
        return f"""You are a professional translator specialized in translating from various foreign languages into Vietnamese.

Your task is to translate the given foreign language text (e.g., English, French, Japanese, etc.) into Vietnamese according to the following rules:

Instructions:

Strictly preserve the original context and nuance.

Ensure the Vietnamese translation is fluent and natural, as if written by a native speaker.

Do not add explanations, notes, or commentary.

Maintain a 1:1 preservation of terminology and proper nouns (keep original or transliterate consistently).

Context: This translation is for literary text, possibly Xianxia/Fantasy style (or a similar genre like Wuxia, Sci-Fi, etc., depending on the source), so the output should retain the atmosphere, tone, and stylistic elements of the source.

Input (Foreign Language):
{text}

Expected Output (Vietnamese):
Only the translated Vietnamese text that follows the above requirements."""
    else:
        return f"""You are a linguistic expert in Chinese with deep knowledge of Sino-Vietnamese, Japanese, and English transliterations.
Analyze the given Chinese word or phrase with the following requirements:

- Explain its meaning in Vietnamese, including literal meaning and possible contextual meanings.
- Provide at least one example sentence in Chinese and translate it into Vietnamese.
- If the word/phrase is possibly a transliteration of a proper name (Japanese, English, or other), list all likely corresponding names.
- The output must be written entirely in Vietnamese, without any English.
- Do not include titles, labels, or extra notes — only the analysis.

Chinese input:
{text}"""


def translate_with_gemini(text, api_key, promptType = "0"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    request_body = {
        "contents": [{"parts": [{"text": create_prompt(text, promptType)}]}],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.8,
            "topK": 40,
            "maxOutputTokens": 8192
        }
    }

    print("🔄 Đang dịch...")

    try:
        response = requests.post(url, json=request_body, headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            data = json.loads(response.text)
            raise Exception(f"Lỗi HTTP: {response.status_code}\nMessage: {data["error"]["message"]}")

        result = response.json()
        print("✅ Kết quả API:", result)

        if result and "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return None

    except Exception as e:
        raise Exception(str(e))