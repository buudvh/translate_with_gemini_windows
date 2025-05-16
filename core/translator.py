import requests

def create_prompt(text):
    return f"""Cho bạn đoạn văn bản: "{text}".
               Hãy dịch đoạn văn bản đó thành Tiếng Việt (Vietnamese) với các điều kiện sau:
               - Tuân thủ chặt chẽ bối cảnh và sắc thái ban đầu.
               - Sự lưu loát tự nhiên như người bản xứ.
               - Không có thêm giải thích/diễn giải.
               - Bảo toàn thuật ngữ 1:1 cho các thuật ngữ/danh từ riêng.
               Chỉ in ra bản dịch mà không có dấu ngoặc kép.
    """

def translate_with_gemini(text, api_key, retry=0):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    request_body = {
        "contents": [{"parts": [{"text": create_prompt(text)}]}]
    }

    print("🔄 Đang dịch...")

    try:
        response = requests.post(url, json=request_body, headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            raise Exception(f"Lỗi HTTP: {response.status_code}")

        result = response.json()
        print("✅ Kết quả API:", result)

        if result and "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return None

    except Exception as e:
        return None