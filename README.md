# Hướng Dẫn Chạy Bot Python (`bot.py`)

## Yêu Cầu Hệ Thống

Trước khi chạy bot, hãy đảm bảo bạn đã cài đặt các thành phần sau:

- **Python** (phiên bản 3.8 trở lên)
- **pip** (trình quản lý gói Python)
- **Các thư viện phụ thuộc** (liệt kê trong `requirements.txt` nếu có)

## Cài Đặt Môi Trường

### 1. Cài Đặt Python

Kiểm tra xem Python đã được cài đặt chưa:
```sh
python --version
```
Nếu chưa có, hãy tải xuống và cài đặt từ [python.org](https://www.python.org/downloads/).

### 2. Tạo Virtual Environment (Tuỳ chọn nhưng khuyến khích)

```sh
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate    # Trên Windows
```

### 3. Cài Đặt Các Gói Phụ Thuộc

Nếu dự án có tệp `requirements.txt`, chạy lệnh sau:
```sh
pip install -r requirements.txt
```

Nếu không, bạn có thể cài đặt các thư viện cần thiết bằng lệnh:
```sh
pip install <tên_thư_viện>
```

## Cấu Hình Bot (Nếu Cần)

Nếu bot yêu cầu file cấu hình (ví dụ: `.env`, `config.json`), hãy đảm bảo file đó có đủ thông tin cần thiết.

## Chạy Bot

Sau khi hoàn tất cài đặt, chạy bot bằng lệnh:
```sh
python bot.py
```

Nếu sử dụng virtual environment:
```sh
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate    # Trên Windows
python bot.py
```

## Xử Lý Lỗi Thông Thường

- **Lỗi thiếu thư viện**: Chạy `pip install -r requirements.txt`.
- **Python không nhận diện**: Thử `python3` thay vì `python`.
- **Lỗi quyền hạn**: Thêm `sudo` trước lệnh (trên Linux/macOS).

## Chạy Bot Ở Nền (Background)

Nếu muốn bot chạy liên tục ngay cả khi đóng terminal:
```sh
nohup python bot.py &
```
Hoặc trên Windows:
```sh
start /b python bot.py
```

## Kết Luận

Bạn đã thiết lập và chạy thành công bot Python (`bot.py`). Nếu có lỗi, hãy kiểm tra kỹ môi trường cài đặt và file cấu hình!

