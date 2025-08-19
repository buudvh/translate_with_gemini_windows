import requests

def create_prompt(text, promptType = "0"):
    if promptType == "0": #TRANSLATE
        return f"""Cho bạn đoạn văn bản: "{text}".
                Hãy dịch đoạn văn bản đó thành Tiếng Việt (Vietnamese) với các điều kiện sau:
                - Tuân thủ chặt chẽ bối cảnh và sắc thái ban đầu.
                - Sự lưu loát tự nhiên như người bản xứ.
                - Không có thêm giải thích/diễn giải.
                - Bảo toàn thuật ngữ 1:1 cho các thuật ngữ/danh từ riêng.
                Chỉ in ra bản dịch mà không có dấu ngoặc kép.
        """
    else:
        return f""" Bạn là một chuyên gia ngôn ngữ chuyên về tiếng Trung, tiếng Việt, tiếng Nhật và tiếng Anh. 
          Nhiệm vụ của bạn là phân tích cụm từ tiếng Trung được cung cấp và đưa ra một giải thích toàn diện bằng tiếng Việt,
          tập trung vào sắc thái và bối cảnh văn hóa của nó.

          Phân tích cụm từ tiếng Trung sau: "{text}"

          Phân tích của bạn *phải* bao gồm những điều sau, được định dạng chính xác như sau:

          1.  **Ý nghĩa và cách sử dụng trong tiếng Việt:**
              *   Cung cấp một giải thích *ngắn gọn và thành ngữ* về ý nghĩa của cụm từ trong tiếng Việt. Cân nhắc các biến thể vùng miền nếu có.
              *   Mô tả *các ngữ cảnh thực tế, điển hình* mà cụm từ được sử dụng trong giao tiếp hoặc văn bản tiếng Việt.

          2.  **Ví dụ (nếu có):**
              *   Cung cấp *một* câu ví dụ *liên quan* bằng tiếng Trung có chứa cụm từ đó.
              *   Cung cấp một bản dịch tiếng Việt *tự nhiên và chính xác* của câu ví dụ đó.

          3.  **Danh từ riêng (nếu có):**
              *   Nếu cụm từ đại diện cho một danh từ riêng nước ngoài được phiên âm (ví dụ: tiếng Nhật hoặc tiếng Anh), hãy xác định cẩn thận (các) thuật ngữ gốc.
              * Hoặc giả định nếu nó là phiên âm tên riêng nước ngoài (tiếng Nhật, tiếng Anh) hãy cho tôi cách đọc của nó được viết bằng Romanji
              *   Đối với mỗi danh từ riêng đã xác định:
                  *   Liệt kê các thuật ngữ gốc tiếng Nhật và dạng Romanji *Hepburn tiêu chuẩn* của nó.
                  *   Liệt kê các thuật ngữ gốc tiếng Anh.
              * Chỉ liệt kê tên mà không cần giải thích gì thêm

          Định dạng câu trả lời của bạn một cách rõ ràng và ngắn gọn bằng tiếng Việt, *sử dụng mẫu được chỉ định bên dưới*. Tuân thủ nghiêm ngặt định dạng này:

          Ý nghĩa:
          [Diễn giải ngắn gọn, tự nhiên về ý nghĩa của cụm từ]
          Ngữ cảnh:
          [Mô tả ngữ cảnh thực tế mà cụm từ thường được sử dụng]

          Ví dụ (nếu có):
          - "[Câu tiếng Trung chứa cụm từ]"
          - "[Bản dịch tiếng Việt tự nhiên và chính xác]"

          Danh sách các danh từ riêng (nếu có):
          * Danh từ riêng: [Cụm từ tiếng Trung]
              - [Tên tiếng Nhật 1 viết bằng Romanji theo hệ Hepburn]
              - [Tên tiếng Nhật 2 viết bằng Romanji theo hệ Hepburn]
              ...........
              - [Tên tiếng Anh]
              - [Tên tiếng Anh - không có thì không hiển thị dòng này]
              ...........
            """


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
            raise Exception(f"Lỗi HTTP: {response.status_code}")

        result = response.json()
        print("✅ Kết quả API:", result)

        if result and "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return None

    except Exception as e:
        return None