import requests
import json

def create_prompt(text, promptType = "0"):
    if promptType == "0": #TRANSLATE
        return f"""Role: You are a professional technical translator specialized in Software Development and IT Documentation.

Task: Translate the provided technical text from [Ngôn ngữ nguồn] into Vietnamese.

Instructions:

Accuracy & Logic: Preserve the exact technical logic, conditions (if-then), and functional requirements. Any ambiguity must be avoided.

Terminology Consistency: Maintain a 1:1 ratio for technical terms. Keep industry-standard English terms in parentheses if necessary (e.g., "Giao diện lập trình ứng dụng (API)"), or keep them in English if they are standard in Vietnamese IT context (e.g., Middleware, Backend, Refactoring).

Tone & Style: Use a formal, objective, and professional tone. The Vietnamese output must be concise and structured, suitable for developers and stakeholders.

Formatting: Strictly preserve all formatting elements such as Markdown, bullet points, tables, and code snippets. Do not translate code, variable names, or API endpoints.

No Commentary: Do not add explanations, notes, or personal opinions outside the translation.

Input (Technical Text): {text}

Expected Output (Vietnamese): Only the translated Vietnamese text that follows the requirements above."""
    else:
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
    
def translate_with_Megallm(text, api_key, promptType = "0"):
    url = "https://ai.megallm.io/v1/chat/completions"
    
    # Payload gửi đi
    payload = {
        "model": "deepseek-ai/deepseek-v3.1",
        "messages": [
            {
                "role": "user",
                "content": create_prompt(text, promptType)
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2048,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("🔄 Đang dịch...")

    try:
        # Gọi API (tương đương fetch trong JS)
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # Kiểm tra lỗi HTTP (tương đương !response.ok)
        response.raise_for_status() 

        result = response.json()

        print("✅ Kết quả API:", result)
        
        # Xử lý kết quả trả về
        if result and 'choices' in result and len(result['choices']) > 0:
            # Lấy nội dung từ lựa chọn đầu tiên
            translated_text = result['choices'][0]['message']['content']
            return translated_text
        else:
            print("Lỗi: API không trả về kết quả hợp lệ.")
            return None

    except requests.exceptions.HTTPError as err:
        print(f"Lỗi HTTP: {err}")
        return None
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        return None