import requests
import random
import time
import logging
from typing import List

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
BASE_URL = "https://llama32.gaia.domains"
MODEL = "Llama-3.2-3B-Instruct-Q5_K_M"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
"No-code là gì?",  
"Sự khác biệt giữa no-code và lập trình truyền thống là gì?",  
"Tại sao ngày càng nhiều người chọn no-code?",  
"No-code mang lại những lợi ích gì khi thiết kế website?",  
"Những lĩnh vực nào có thể áp dụng no-code hiệu quả?",  
"Các nền tảng no-code phổ biến nhất để tạo website là gì?",  
"Làm thế nào để tìm được nền tảng no-code phù hợp?",  
"No-code có thể xử lý các dự án lớn không?",  
"Có thể sử dụng no-code để tự động hóa quy trình không?",  
"No-code đang thay đổi ngành phát triển web như thế nào?",  
"Làm thế nào để xây dựng website bằng no-code?",  
"Những tính năng quan trọng của nền tảng no-code là gì?",  
"Các bước cơ bản để bắt đầu với no-code là gì?",  
"No-code có thể tạo được website chuyên nghiệp không?",  
"Website làm bằng no-code có tốc độ nhanh không?",  
"Làm thế nào để thêm trang mới vào website no-code?",  
"No-code có hỗ trợ tạo trang web đa ngôn ngữ không?",  
"Làm sao để thiết kế giao diện website với no-code?",  
"Có thể tích hợp plugin vào website no-code không?",  
"Làm thế nào để làm website no-code thân thiện với di động?",  
"No-code có hỗ trợ thiết kế giao diện kéo thả không?",  
"Làm sao để xuất bản website bằng no-code?",  
"No-code có thể xây dựng website thương mại điện tử không?",  
"Những hạn chế của nền tảng no-code là gì?",  
"Làm sao để tối ưu SEO cho website no-code?",  
"Có thể sử dụng Google Analytics trên website no-code không?",  
"No-code có thể tạo website bán hàng không?",  
"Những yếu tố cần chú ý khi tối ưu hiệu suất website no-code?",  
"Website no-code có thể sử dụng tên miền riêng không?",  
"Cách tốt nhất để bảo mật website no-code là gì?",  
"No-code có thể hỗ trợ hệ thống thành viên không?",  
"Làm thế nào để tạo biểu mẫu liên hệ trên website no-code?",  
"No-code có thể tích hợp thanh toán trực tuyến không?",  
"Làm sao để thêm giỏ hàng vào website no-code?",  
"Làm thế nào để quản lý dữ liệu khách hàng trên website no-code?",  
"Những nền tảng no-code hỗ trợ tích hợp email marketing?",  
"Làm sao để theo dõi hành vi người dùng trên website no-code?",  
"No-code có thể xây dựng trang web doanh nghiệp không?",  
"Làm thế nào để thêm blog vào website no-code?",  
"Có thể tùy chỉnh font chữ trên website no-code không?",  
"Làm thế nào để tối ưu tốc độ tải trang cho website no-code?",  
"No-code có thể giúp tạo portfolio cá nhân không?",  
"Làm sao để thêm Google Maps vào website no-code?",  
"Cách tốt nhất để thêm mạng xã hội vào website no-code?",  
"No-code có thể giúp tạo website phi lợi nhuận không?",  
"Làm sao để thêm chức năng tìm kiếm vào website no-code?",  
"Cách đảm bảo website no-code luôn an toàn?",  
"Làm sao để thêm favicon vào website no-code?",  
"No-code có thể giúp tạo landing page không?",  
"Làm thế nào để thêm đánh giá khách hàng vào website no-code?",  
"No-code có thể giúp tạo website cộng đồng không?",  
"Có thể dùng no-code để tạo diễn đàn không?",  
"Làm sao để nhúng video vào website no-code?",  
"No-code có hỗ trợ quản lý tập tin không?",  
"Làm thế nào để thêm hệ thống đăng ký thành viên vào website no-code?",  
"Có thể thêm chatbot vào website no-code không?",  
"Làm sao để cài đặt email marketing trên website no-code?",  
"No-code có thể giúp tạo ứng dụng web không?",  
"Những nền tảng no-code nào hỗ trợ phát triển ứng dụng?",  
"Làm sao để quản lý cơ sở dữ liệu trong ứng dụng no-code?",  
"No-code có thể hỗ trợ quản lý người dùng không?",  
"Làm thế nào để bảo mật ứng dụng no-code?",  
"Có thể tích hợp API vào ứng dụng no-code không?",  
"Làm sao để xác thực người dùng trong ứng dụng no-code?",  
"No-code có hỗ trợ kiểm thử ứng dụng không?",  
"Làm thế nào để triển khai ứng dụng no-code?",  
"No-code có thể tạo ứng dụng di động không?",  
"Làm sao để thêm tính năng thanh toán vào ứng dụng no-code?",  
"Có thể sử dụng no-code để tạo ứng dụng nội bộ không?",  
"Làm sao để gửi thông báo đẩy trong ứng dụng no-code?",  
"No-code có thể giúp tạo ứng dụng theo thời gian thực không?",  
"Làm thế nào để theo dõi hiệu suất của ứng dụng no-code?",  
"Làm sao để xử lý lỗi trong ứng dụng no-code?",  
"Có thể thêm phân tích dữ liệu vào ứng dụng no-code không?",  
"No-code có thể giúp tạo hệ thống quản lý công việc không?",  
"Làm thế nào để tích hợp CRM vào ứng dụng no-code?",  
"Có thể thêm AI vào ứng dụng no-code không?",  
"No-code có hỗ trợ tạo ứng dụng SaaS không?",  
"Làm thế nào để quản lý phân quyền người dùng trong ứng dụng no-code?",  
"No-code có thể giúp xây dựng ứng dụng doanh nghiệp không?",  
"Làm sao để đảm bảo bảo mật dữ liệu trong ứng dụng no-code?",  
"No-code có hỗ trợ tích hợp các công cụ marketing automation không?",  
"Làm thế nào để tối ưu UX/UI cho ứng dụng no-code?",  
"No-code có thể giúp tạo chatbot không?",  
"Làm sao để thêm bộ lọc và tìm kiếm nâng cao vào ứng dụng no-code?",  
"Làm thế nào để sao lưu dữ liệu trong ứng dụng no-code?",  
"No-code có thể giúp xây dựng hệ thống đặt lịch hẹn không?",  
"Có thể tích hợp mạng xã hội vào ứng dụng no-code không?",  
"Làm sao để cá nhân hóa trải nghiệm người dùng trong ứng dụng no-code?",  
"Cách tốt nhất để tạo onboarding cho ứng dụng no-code?",  
"No-code có thể giúp phát triển MVP nhanh chóng không?",  
"Làm thế nào để thu hút người dùng cho ứng dụng no-code?",  
"Có thể kết hợp no-code với lập trình truyền thống không?",  
"No-code có phù hợp để phát triển game không?",  
"Làm sao để quản lý file trong ứng dụng no-code?",  
"Làm thế nào để đảm bảo tuân thủ luật bảo vệ dữ liệu trong ứng dụng no-code?",  
"No-code có hỗ trợ phân tích dữ liệu trực quan không?",  
"Làm thế nào để duy trì và cập nhật ứng dụng no-code?",  
"Có thể sử dụng no-code để phát triển ứng dụng blockchain không?",  
"No-code có hỗ trợ triển khai trên cloud không?",  
"Làm thế nào để tạo dashboard quản trị trong ứng dụng no-code?",  
"No-code có phù hợp với các doanh nghiệp lớn không?",  
"Làm sao để tạo quy trình tự động trong ứng dụng no-code?",  
"No-code có thể giúp tạo hệ thống quản lý học tập không?",  
"Làm thế nào để tích hợp IoT với ứng dụng no-code?",  
"No-code có thể giúp tạo ứng dụng thương mại điện tử không?",  
"Cách tốt nhất để tối ưu chi phí khi sử dụng no-code?",  
"No-code có thể hỗ trợ quản lý kho hàng không?",  
"Làm sao để kết hợp AI với no-code để tạo chatbot?",  
"No-code có thể hỗ trợ quản lý nhân sự không?",  
"Làm sao để tạo hệ thống booking trực tuyến bằng no-code?",  
"Làm thế nào để kết nối ứng dụng no-code với ERP?",  
"Có thể xây dựng hệ thống loyalty với no-code không?",  
"No-code có thể giúp tạo hệ thống quản lý nội dung không?",  
"Làm sao để tích hợp blockchain vào no-code?",  
"No-code có thể giúp phát triển ứng dụng tài chính không?",  
"Cách tốt nhất để tối ưu hiệu suất ứng dụng no-code?",  
"Những xu hướng phát triển no-code trong tương lai là gì?"
]

def chat_with_ai(api_key: str, question: str) -> str:
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

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    api_key = input("nhap key")
    run_bot(api_key)

if __name__ == "__main__":
    main()
