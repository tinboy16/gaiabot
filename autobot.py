import requests
import random
import time
import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://qwen7b.gaia.domains"
MODEL = "Qwen2.5-7B-Instruct-Q5_K_M"
MAX_RETRIES = 100  
RETRY_DELAY = 7  
QUESTION_DELAY = 1  
WIKI_API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/title"
NUM_QUESTIONS = 7  # Số câu hỏi chạy cùng lúc


def get_random_question() -> str:
    """Lấy tiêu đề bài viết ngẫu nhiên từ Wikipedia và chuyển thành câu hỏi."""
    try:
        response = requests.get(WIKI_API_URL, timeout=10)
        if response.status_code == 200:
            title = response.json().get("items", [{}])[0].get("title", "Unknown Topic")
            return f"{title} là gì?"
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
