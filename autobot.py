import requests
import random
import time
import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Cấu hình
BASE_URL = "https://qwen7b.gaia.domains"
MODEL = "Qwen2.5-7B-Instruct-Q5_K_M"
MAX_RETRIES = 100  
RETRY_DELAY = 5  
QUESTION_DELAY = 1  
WIKI_API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/title"
NUM_QUESTIONS = 5 # Số câu hỏi chạy cùng lúc


def get_random_question() -> str:
    """Lấy một đoạn tóm tắt từ Wikipedia và chuyển thành câu hỏi rất chi tiết."""
    try:
        # Lấy tiêu đề ngẫu nhiên
        response = requests.get(WIKI_API_URL, timeout=10)
        if response.status_code == 200:
            title = response.json().get("items", [{}])[0].get("title", "Unknown Topic")

            # Lấy nội dung tóm tắt từ Wikipedia dựa trên tiêu đề
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
            summary_response = requests.get(summary_url, timeout=10)

            if summary_response.status_code == 200:
                summary = summary_response.json().get("extract", "Không có thông tin.")
                return f"Chủ đề '{title}' là một khái niệm có tầm ảnh hưởng rộng rãi trong nhiều lĩnh vực khác nhau. Tuy nhiên, để có cái nhìn sâu sắc hơn về chủ đề này, bạn có thể cung cấp cho tôi các thông tin chi tiết sau đây: 1) Lịch sử hình thành và sự phát triển của chủ đề này qua các thời kỳ, đặc biệt là những sự kiện quan trọng đã thúc đẩy sự thay đổi của nó; 2) Các nhân vật lịch sử hay những tổ chức có ảnh hưởng lớn đến sự hình thành và phát triển của chủ đề này; 3) Tác động của chủ đề này đối với xã hội và các lĩnh vực khác như khoa học, nghệ thuật, chính trị, và văn hóa; 4) Những thay đổi đáng chú ý trong cách mà con người tiếp cận hoặc hiểu về chủ đề này theo thời gian, và liệu có sự thay đổi lớn nào trong tư duy hay phương pháp luận không; 5) Các ứng dụng thực tế của chủ đề này trong đời sống hàng ngày hay trong các ngành công nghiệp khác nhau; 6) Tình hình hiện tại và những tranh luận đang diễn ra liên quan đến chủ đề này, liệu có những quan điểm trái chiều nào không? Bạn có thể cung cấp thông tin chi tiết về các vấn đề này và giải thích thêm về những ảnh hưởng mà chủ đề này có thể mang lại cho tương lai không?"

            else:
                logging.warning(f"Wiki Summary API Error ({summary_response.status_code}): {summary_response.text}")

        else:
            logging.warning(f"Wiki API Error ({response.status_code}): {response.text}")

    except Exception as e:
        logging.error(f"Failed to fetch question from Wikipedia: {str(e)}")
    
    return "Câu hỏi ngẫu nhiên không thể tải được."

def chat_with_ai(api_key: str, question: str) -> str:
    """Gửi câu hỏi đến AI API và nhận câu trả lời."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    return "Không thể lấy câu trả lời từ AI."


def run_bot(api_key: str):
    while True:
        logging.info(f"Fetching {NUM_QUESTIONS} random questions...")

        # Lấy 5 câu hỏi từ Wikipedia
        with ThreadPoolExecutor() as executor:
            questions = list(executor.map(lambda _: get_random_question(), range(NUM_QUESTIONS)))


        logging.info("Generated questions:")
        for q in questions:
            logging.info(f"- {q}")

        # Gửi 5 câu hỏi đến AI song song
        responses = {}
        with ThreadPoolExecutor() as executor:
            future_to_question = {executor.submit(chat_with_ai, api_key, q): q for q in questions}

            for future in as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    responses[question] = future.result()
                except Exception as e:
                    logging.error(f"Failed to process question '{question}': {str(e)}")
                    responses[question] = "Lỗi khi nhận phản hồi."

        # In kết quả
        for question, response in responses.items():
            print(f"\n📌 Câu hỏi: {question}\n💡 Trả lời: {response}\n" + "-"*50)

        logging.info(f"Sleeping {QUESTION_DELAY} seconds before next batch...")
        time.sleep(QUESTION_DELAY)


def main():
    api_key = input("Nhập API key = ")
    run_bot(api_key)


if __name__ == "__main__":
    main()
