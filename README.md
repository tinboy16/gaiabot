


# Hướng dẫn chạy bot.py

## Yêu cầu
- Python đã được cài đặt (phiên bản >= 3.x)
- Cài đặt thư viện cần thiết bằng lệnh:
  ```bash
  pip install requests
  ```

## Cách chạy bot
1. Đảm bảo tất cả các dependencies đã được cài đặt.
2. Mở terminal hoặc command prompt.
3. Chạy bot bằng lệnh:
   ```bash
   python bot.py
   ```

## Ghi chú
- Kiểm tra log trong quá trình chạy để debug nếu có lỗi.
- Có thể điều chỉnh các thông số trong file cấu hình nếu cần.


# Hướng Dẫn Chạy Node Gaia AI  

Hướng dẫn này sẽ giúp bạn thiết lập và chạy một node Gaia AI với mô hình LLM nhẹ **Qwen2 0.5B Instruct** để kiếm **GaiaPoints** và nhận airdrop token Gaia trong tương lai!  

---

## **Gaia Dashboard**  
Trong chương trình Gaia XP, bạn tích lũy điểm bằng cách tương tác với Gaia AI Agents và chạy node Gaia.  

1. Kết nối ví của bạn với [Gaia Dashboard](https://gaianet.ai/reward?invite_code=R0S4GW) và hoàn tất đăng ký.  
2. Sử dụng mã mời này để nhận thêm XP: `R0S4GW`  
3. Hoàn thành các nhiệm vụ xã hội tại [Rewards Summary](https://www.gaianet.ai/reward-summary).  

---

## **Gaia Node**  
Hướng dẫn này sẽ giúp bạn kiếm **Node Points** và **User Points** trên dashboard bằng cách:  
- Cài đặt node.  
- Giữ node luôn trực tuyến và xử lý yêu cầu.  
- Tham gia một Domain.  
- Chat với AI Agent của domain đã tham gia.  

### **1. Yêu cầu hệ thống**  
Để chạy node Gaia với mô hình **Qwen2 0.5B Instruct**, cần có:  
- **CPU**: 4 core
- **RAM**: 8GB  
- **Lưu trữ**: 10GB  

**Dành cho Windows**:  
- Cần cài đặt Ubuntu bằng cách kích hoạt WSL trên Windows. Xem hướng dẫn [tại đây](https://github.com/tinboy16/wsl.git).  

**Dành cho Linux/VPS**:  
- Bạn có thể tiếp tục làm theo hướng dẫn.  

> Nếu bạn sử dụng VPS, hãy cài đặt Gaia Node trên cả Windows để tăng **GaiaPoints**. Càng giữ node online, kết nối với domain và chat với AI, bạn càng nhận nhiều **Node Points** & **User Points**.  

---

### **2. Cài đặt các gói cần thiết**  
Cập nhật hệ thống và cài đặt Python:  
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

---

### **3. Xóa node cũ (nếu đã cài trước đó)**  
```bash
gaianet stop
curl -sSfL 'https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/uninstall.sh' | bash
source /root/.bashrc
```

---

### **4. Cài đặt Gaia Node CLI**  
Chạy lệnh sau để cài đặt Gaia Node CLI:  
```bash
curl -sSfL 'https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh' | bash
```
Sau khi cài đặt, chạy lệnh:  
```bash
source /root/.bashrc
```
Hoặc khởi động lại terminal để kích hoạt `gaianet CLI`.  

---

### **5. Cấu hình Gaia Node**  
Tải xuống mô hình **Qwen2 0.5B Instruct** và khởi tạo node bằng lệnh:  
```bash
gaianet init --config https://raw.githubusercontent.com/GaiaNet-AI/node-configs/main/qwen2-0.5b-instruct/config.json
```

---

### **6. Chạy Gaia Node**  
Chạy lệnh sau để khởi động node:  
```bash
gaianet start
```
> Nếu cần dừng node, chạy lệnh: `gaianet stop`  

---

### **7. Đăng ký node trên Gaia Dashboard**  
1. Chạy lệnh sau để lấy **Node ID** và **Device ID**:  
   ```bash
   gaianet info
   ```
2. Truy cập [Node Settings](https://www.gaianet.ai/setting/nodes) và nhấn **Connect New Node**.  
3. Nhập **Node ID** và **Device ID** vào trang web, rồi nhấn **Join**.  

---

### **8. Tham gia một Domain**  
- Bạn cần tham gia domain và chat với AI để kiếm **Node Points**.  
- Chat với node của mình mà không vào domain sẽ không có tác dụng.  

1. Chạy các lệnh sau trong terminal:  
   ```bash
   gaianet stop
   gaianet config --domain gaia.domains
   gaianet init
   gaianet start
   ```
2. Truy cập [Node Settings](https://www.gaianet.ai/setting/nodes).  
3. Nhấn vào dấu ba chấm bên cạnh node đang hoạt động và chọn **Join Domain**.  
4. Nhấn **Next Step**.  
5. Tìm kiếm domain `pengu.gaia.domain`.  
6. Chọn domain và hoàn tất các bước tiếp theo.  

---

### **9. Chat với node của bạn**  
Truy cập [doge Gaia Domain](https://doge.gaia.domains) để chat với node và kiếm XP.  

- Bạn cần **Credit Balance** để chat với node.  
- Mỗi ngày, đổi **GaiaPoints** thành **Credit Balance**.  
- **GaiaPoints** sẽ không giảm sau khi đổi và bạn có thể đổi tối đa 1000 GaiaPoints/ngày.  

---

### **10. Chạy AutoChat Bot**  
1. **Tạo API Key**:  
   - Truy cập [Gaia API Keys](https://www.gaianet.ai/setting/gaia-api-keys) và tạo key mới.  
   - Lưu API key vì bạn sẽ không thể xem lại.  

2. **Tải xuống script AutoChat**:  
   ```bash
   curl -L -o dogebot.py https://raw.githubusercontent.com/tinboy16/gaiabot/refs/heads/main/dogebot.py
   ```

3. **Chạy bot tự động**:  
   - Mở một phiên `screen` để chạy bot trong nền:  
     ```bash
     screen -S dogebot
     ```
   - Chạy bot:  
     ```bash
     python3 dogebot.py
     ```
   - Nhập API Key khi được yêu cầu.  

- Để ẩn màn hình: Nhấn `Ctrl+A+D`  
- Để quay lại: `screen -r dogebot`  
- Để dừng bot: `CTRL+C`, sau đó chạy:  
  ```bash
  screen -XS dogebot quit
  ```

---

### **11. Kiếm điểm**  
Sau khi làm theo hướng dẫn, bạn sẽ bắt đầu kiếm điểm. Điểm sẽ cập nhật sau 24h hoặc lâu hơn.  

- **User Points**: Chat với domain của bạn hoặc domain khác.  
- **Node Points**: Giữ node hoạt động và chat với AI trong domain đã tham gia.  

Nếu bạn chạy node trên máy tính cá nhân (Windows hoặc Linux), chỉ cần khởi động lại **Node + ChatBot** mỗi ngày.
