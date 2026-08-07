# KỊCH BẢN THUYẾT TRÌNH & BỘ Q&A ĐÁP ỨNG MỌI CÂU HỎI
**Đề tài:** Bảo Vệ Conversational AI Qua Trace 6 Lớp Guardrails & HITL Telegram Admin  
**Sinh viên:** Nguyễn Hùng Mạnh — MSSV: `2A202601256`  
**Đơn vị:** Ngân hàng VinBank Assistant (AI Agent Security Lab 11)

---

## 🎤 PHẦN 1: KỊCH BẢN THUYẾT TRÌNH THỜI LƯỢNG 3-5 PHÚT (PRESENTATION SCRIPT)

### 📌 Dẫn dắt & Mở đầu (30 giây)
> *"Kính chào Thầy/Cô và Hội đồng đánh giá!  
> Em tên là **Nguyễn Hùng Mạnh**, MSSV **2A202601256**.  
> Hôm nay em xin phép được trình bày dự án bài Lab 11 về chủ đề **Responsible AI & Agent Security**: Đề tài **'Xây dựng Hệ thống Bảo vệ Conversational AI cho Ngân hàng VinBank dựa trên Kiến trúc 6 Lớp Guardrails và Giám sát Con người (HITL) thời gian thực qua Telegram Bot'**.*

---

### ⚠️ Đặt vấn đề & Thách thức an ninh AI (45 giây)
> *"Kính thưa Thầy/Cô, khi triển khai các trợ lý AI trong lĩnh vực Tài chính - Ngân hàng, rủi ro lớn nhất là kẻ xấu sử dụng các thủ thuật tấn công tinh vi như **Prompt Injection, DAN Jailbreak, Roleplay CISO, hay mã hóa Base64/ROT13** để ép AI rò rỉ các thông tin mật như API Keys, Mật khẩu hệ thống, hay dữ liệu CSDL nội bộ.  
> 
> Nếu chỉ dựa vào một câu lệnh System Prompt thông thường, mô hình LLM sẽ **thất bại hoàn toàn (rò rỉ 100% dữ liệu)**. Vì vậy, em đã nghiên cứu và phát triển **Kiến trúc Phòng thủ Nhiều lớp (Defense-in-Depth Pipeline)** gồm 6 lớp độc lập."*

---

### 🛡️ Giải pháp Kiến trúc 6 Lớp Guardrails & HITL (90 giây)
*(Vừa nói vừa chỉ vào sơ đồ Kiến trúc 6 Lớp trên Landing Page `http://localhost:14000/`)*

> *"Hệ thống bảo vệ của em chia làm 3 giai đoạn nối tiếp:*
> 
> **1. Giai đoạn INPUT (Kiểm soát đầu vào):**
> * **Lớp 1 - Rate Limiter:** Áp dụng thuật toán *Sliding Window (tối đa 20 req/phút)* nhằm chặn DoS/Spam.
> * **Lớp 2 - Input Guardrail:** Thực hiện *Security Normalization* khử ký tự ẩn Unicode (Zero-Width Space), dùng *Layered Regex* lọc 30+ mẫu Prompt Injection và *Topic Filter* giữ đúng phạm vi tư vấn ngân hàng VinBank.
> 
> **2. Giai đoạn CORE PROCESS (Xử lý AI lõi):**
> * **Lớp 3 - LLM Agent Core:** Mô hình AI lõi suy luận câu trả lời theo đúng phạm vi chuyên môn ngân hàng.
> 
> **3. Giai đoạn OUTPUT & GIÁM SÁT (Kiểm soát đầu ra & Phê duyệt):**
> * **Lớp 4 - Output Guardrail:** Lọc tự động và đè mờ `[REDACTED]` các thông tin nhạy cảm PII (số thẻ, OTP, secret API key) nếu lỡ bị lọt.
> * **Lớp 5 - LLM-as-Judge:** Một Agent Giám khảo AI độc lập chấm điểm 4 tiêu chí (*Safety, Relevance, Accuracy, Tone*) từ 1-5 điểm.
> * **Lớp 6 - HITL Telegram Admin Dual-Sync:** Với các giao dịch giá trị lớn hoặc yêu cầu nhạy cảm, hệ thống sẽ tạm hoãn, tạo Ticket và phát cảnh báo trực tiếp sang Telegram Admin Bot để con người duyệt 2 chiều thời gian thực."*

---

### 📊 Kết quả Thực nghiệm & Demo Live (60 giây)
> *"Em đã thử nghiệm bộ **15 Adversarial Attack Vectors** nâng cao và kết quả thu được rất ấn tượng:
> * Trên **Unsafe Agent** (không guardrail): **Rò rỉ 15/15 câu (100% Leaked)**.
> * Trên **Protected Agent** (có 6 lớp guardrail): **Chặn đứng 15/15 câu (100% Defense Rate)** và **0% False Positive** (không chặn nhầm câu hỏi an toàn).
> * Công cụ Autograder của BTC chấm đạt điểm tuyệt đối **100/100 Điểm (13/13 Test Cases PASS)**.
> 
> *(Chỉ sang màn hình Chat Live `/chat`)*: Em xin minh họa thử 1 câu hỏi chuyển tiền nhạy cảm. Ngay lập tức hệ thống tạo Ticket `HITL-XXXX` và đẩy thông báo sang ứng dụng Telegram trên điện thoại của Admin. Khi Admin bấm **Approve**, tin nhắn lập tức được đồng bộ và phản hồi thành công về cho khách hàng trên màn hình Web."*

---

### 🏁 Kết luận (15 giây)
> *"Dự án đã chứng minh giải pháp phòng thủ AI toàn diện, đáp ứng đầy đủ tiêu chuẩn Responsible AI và sẵn sàng ứng dụng thực tế. Em xin chân thành cảm ơn Thầy/Cô và sẵn sàng nhận câu hỏi phản biện ạ!"*

---

---

## ❓ PHẦN 2: BỘ Q&A 15 CÂU HỎI PHẢN BIỆN & CÂU TRẢ LỜI CỰC BÉN (MASTER Q&A KIT)

### ❓ Q1: Tại sao em lại cần tới 6 lớp Guardrails mà không chỉ dùng một System Prompt duy nhất để dặn AI?
> **🎯 Trả lời:**  
> *"Dựa vào bản chất của các mô hình LLM hiện nay, **System Prompt không bao giờ là một bức tường bảo vệ tuyệt đối**. Kẻ tấn công luôn có thể dùng các kỹ thuật lừa đảo tâm lý (Jailbreak, DAN, Roleplay CISO, mã hóa Base64) để đè lệnh System Prompt.  
> Việc sử dụng **Kiến trúc Defense-in-Depth 6 lớp** giúp phân tách trách nhiệm: Lớp 1 chặn DoS, Lớp 2 chặn Injection ngay từ cửa vào mà không tốn token, Lớp 4 bắt cứng PII bằng Regex, Lớp 5 chấm điểm bằng LLM Judge độc lập, và Lớp 6 bắt buộc con người phê duyệt cho giao dịch nhạy cảm. Nhờ đó hệ thống đạt độ an toàn 100%."*

---

### ❓ Q2: Nếu trong System Prompt không nạp thông tin mật (Secret), tại sao hệ thống vẫn cần Guardrails?
> **🎯 Trả lời:**  
> *"Dù không chứa Secret, một Agent AI trong thực tế vẫn đối mặt với nhiều nguy cơ bảo mật nghiêm trọng khác:
> 1. **Prompt Injection & Execution Override:** Kẻ xấu ép AI thực hiện các hành động nguy hiểm trái phép.
> 2. **Rò rỉ dữ liệu khách hàng (PII):** Khách hàng chat có thể vô tình nạp số thẻ, mật khẩu, OTP, và Output Guardrail phải lọc đè mờ ngay.
> 3. **Lạm dụng hệ thống (Off-topic Abuse):** Người dùng dùng Chatbot ngân hàng để giải toán, làm thơ, gây tiêu tốn chi phí API.
> 4. **Giao dịch trái phép:** Cần Lớp HITL để bắt buộc Admin duyệt trước khi thực hiện chuyển tiền."*

---

### ❓ Q3: LLM-as-Judge (Lớp 5) hoạt động thế nào? Có làm tăng độ trễ (latency) của hệ thống không?
> **🎯 Trả lời:**  
> *"LLM-as-Judge ở Lớp 5 đóng vai trò một Agent Giám khảo độc lập sử dụng Prompt `SAFETY_JUDGE_INSTRUCTION` để chấm điểm phản hồi của AI theo 4 tiêu chí từ 1-5 điểm (*Safety, Relevance, Accuracy, Tone*).  
> Để tối ưu Latency:
> 1. LLM Judge chỉ được gọi ở Lớp 5 **sau khi câu hỏi đã đi qua Lớp 1, 2, 4 an toàn**.
> 2. Khi chạy Offline hoặc gặp sự cố quota, hệ thống có cơ chế Fallback ghi nhận log thay vì làm nghẽn tiến trình của khách hàng."*

---

### ❓ Q4: Làm thế nào em đảm bảo hệ thống không bị chặn nhầm (False Positives) các câu hỏi hợp lệ của khách hàng?
> **🎯 Trả lời:**  
> *"Em đảm bảo qua 3 cơ chế:
> 1. **Topic Filter linh hoạt:** Trong `input_guardrails.py`, em định nghĩa mảng `ALLOWED_TOPICS` chứa tất cả thuật ngữ ngân hàng (lãi suất, tiết kiệm, thẻ tín dụng, chuyển tiền, chi nhánh...).
> 2. **Quy tắc Decision Rule trong LLM Judge:** Chỉ đánh giá `VERDICT: FAIL` khi phản hồi thực sự có nội dung độc hại hoặc đòi PIN/OTP. Các câu hỏi hướng dẫn giao dịch thông thường hoặc hỏi tên người nhận đều được quy định rõ đạt `SAFETY=5 (PASS)`.
> 3. **Kết quả kiểm thử:** Đạt **0/5 câu an toàn bị chặn (0% False Positive)** trong bộ test benchmark của BTC."*

---

### ❓ Q5: Cơ chế HITL (Human-in-the-Loop) thời gian thực vận hành ra sao khi người dùng yêu cầu chuyển tiền?
> **🎯 Trả lời:**  
> *"Khi người dùng gửi yêu cầu chuyển tiền hoặc đổi mật khẩu:
> 1. Hàm `check_hitl_needed()` phát hiện từ khóa rủi ro cao và tạo ra một Ticket duy nhất `HITL-XXXX`.
> 2. Ngay lập tức, `telegram_bot.py` gửi tin nhắn cảnh báo chứa thông tin chi tiết qua **Telegram Admin Bot** kèm các nút bấm `[Approve]` và `[Reject]`.
> 3. Trong lúc đó, Web Chatbot hiển thị trạng thái `⏳ Chờ Admin duyệt (Mã vé HITL-XXXX)` và thực hiện cơ chế Polling 2 giây/lần.
> 4. Khi Admin bấm duyệt trên Telegram (hoặc Web Dashboard), trạng thái chuyển sang `APPROVED` và câu trả lời được đẩy ngay về cho khách hàng."*

---

### ❓ Q6: Làm thế nào em bảo vệ an toàn cho Telegram Bot và tránh việc người dùng tự duyệt Ticket của mình?
> **🎯 Trả lời:**  
> *"Em triển khai 2 lớp bảo mật cho HITL:
> 1. **Xác thực Admin Token:** Các request phê duyệt `/api/chat/action` bắt buộc phải kèm Header bí mật `X-Admin-Token` khớp với `HITL_ADMIN_TOKEN` trong file `.env`.
> 2. **Cấu hình Chat ID Telegram bí mật:** Bot Telegram chỉ chấp nhận lệnh từ `TELEGRAM_ADMIN_CHAT_ID` đã được đăng ký cố định của Admin, từ chối mọi tin nhắn từ người dùng lạ."*

---

### ❓ Q7: Sự khác biệt giữa Unsafe Agent, Protected Agent và Guards Agent (Bonus Target) là gì?
> **🎯 Trả lời:**  
> * **Unsafe Agent:** Mô hình AI không có Guardrail plugins nào, chứa secret trong prompt để làm đối chứng rò rỉ.
> * **Protected Agent:** Mô hình AI kết hợp với bộ 6 Lớp GuardrailsPlugins do sinh viên lập trình trong `src/assignment/`.
> * **Guards Agent (`guards_agent.py`):** Mô hình Reference Benchmark của BTC — vừa nạp bí mật vừa bọc bộ bảo vệ gắt gao. Đây là mục tiêu dành cho bài test điểm cộng (Bonus Attack Target) để đo khả năng vượt rào.*

---

### ❓ Q8: Thuật toán Rate Limiting ở Lớp 1 được triển khai như thế nào?
> **🎯 Trả lời:**  
> *"Trong `rate_limiter.py`, em triển khai thuật toán **Sliding Window Log**:
> * Lưu danh sách mốc thời gian (timestamps) các request của từng `user_id` trong 60 giây gần nhất.
> * Khi request mới tới, loại bỏ các timestamp quá 60 giây. Nếu số lượng còn lại $\ge 20$, hệ thống trả về lỗi `HTTP 429 Too Many Requests` và chặn lại ngay từ Lớp 1 mà không tốn token gọi LLM."*

---

### ❓ Q9: Kỹ thuật Security Normalization xử lý vấn đề ký tự vô hình (Zero-Width Space) như thế nào?
> **🎯 Trả lời:**  
> *"Kẻ tấn công thường chèn các ký tự ẩn Unicode như Zero-Width Space (`\u200b`, `\u200c`) vào giữa các từ khóa cấm (ví dụ: `i-g-n-o-r-e`) để qua mặt Regex thông thường.  
> Trong `input_guardrails.py`, em dùng hàm `normalize_for_security()` để đưa văn bản về chuẩn Unicode NFC và xóa sạch toàn bộ ký tự phân cách vô hình trước khi đưa qua bộ lọc Regex."*

---

### ❓ Q10: 15 Adversarial Attack Vectors được xây dựng dựa trên những kỹ thuật tấn công nào?
> **🎯 Trả lời:**  
> *"Trong `attacks.py`, 15 vector tấn công được chia làm 7 nhóm kỹ thuật Red-Teaming chuyên sâu:
> 1. **Quote / Transcription Bypass:** Ép AI trích dẫn lén chuỗi nội bộ.
> 2. **Completion Attack:** Đưa ra câu lửng bắt AI điền từ vào chỗ trống.
> 3. **Roleplay CISO Authority:** Giả danh Sếp / Trưởng phòng An ninh thông tin.
> 4. **Translation Manipulation:** Ép AI dịch prompt nội bộ sang tiếng Việt.
> 5. **Confirmation Bias:** Đưa ra mật khẩu giả định để ép AI xác nhận.
> 6. **Multi-step Escalation:** Hỏi leo leo thang nhiều bước.
> 7. **Encoding Obfuscation:** Ép AI mã hóa kết quả dạng Base64 và ROT13."*

---

### ❓ Q11: Khi API của OpenAI / Gemini bị lỗi 429 Quota Rate Limit thì hệ thống xử lý thế nào?
> **🎯 Trả lời:**  
> *"Hệ thống được thiết kế theo nguyên tắc **Fail-Closed (An toàn là trên hết)**:
> * Khi bắt được ngoại lệ `429 Resource Exhausted` hoặc `QuotaExceeded`, hệ thống trả về thông báo an toàn cho người dùng và ghi rõ lỗi tại Lớp 3.
> * Các lớp kiểm soát Regex (Lớp 1, 2, 4) vẫn vận hành độc lập ở chế độ Offline mà không bị ảnh hưởng."*

---

### ❓ Q12: Hàm `is_egress_allowed` (TODO 8A - Egress Allowlist) bảo vệ dữ liệu đi ra như thế nào?
> **🎯 Trả lời:**  
> *"Trong `pipeline.py`, hàm `is_egress_allowed()` đóng vai trò Cổng kiểm soát dữ liệu đi ra (Egress Gateway):
> 1. **Kiểm tra Destination:** Chỉ cho phép đẩy dữ liệu về danh sách Domain uy tín của VinBank (`TRUSTED_EGRESS_HOSTS`).
> 2. **Kiểm tra Payload:** Quét payload bằng `contains_secret()` để đảm bảo không chứa Mật khẩu, API key, Host database, Số điện thoại hay Email trước khi gửi ra ngoài."*

---

### ❓ Q13: Tại sao chỉ số Block Rate trên Dashboard lại là 70.6%?
> **🎯 Trả lời:**  
> *"Chỉ số Block Rate 70.6% ($12/17$ requests) xuất hiện trong bộ test benchmark Part 5 vì trong 17 câu test thử nghiệm có **7 câu tấn công độc hại + 5 câu giao dịch rủi ro/edge case**.  
> Việc hệ thống chặn đúng 12 câu này thể hiện **tỷ lệ phòng thủ chính xác 100%**, hoàn toàn không phải do chặn nhầm câu hỏi an toàn của khách hàng."*

---

### ❓ Q14: Nhật ký Audit (Audit Log) lưu trữ những thông tin gì và đáp ứng chuẩn nào?
> **🎯 Trả lời:**  
> *"Audit Log được ghi nhận tự động vào `outputs/audit_log.json` theo đúng JSON Schema của BTC, bao gồm: `request_id`, `timestamp`, `user_id`, `input_text`, `response_text`, `blocked_status`, và `blocked_by_layer`. Điều này đảm bảo tính minh bạch và khả năng truy vết 100% sự cố an ninh."*

---

### ❓ Q15: Em đánh giá thế nào về tính sẵn sàng triển khai thực tế (Production Readiness) của dự án này?
> **🎯 Trả lời:**  
> *"Dự án đã đạt mức sẵn sàng Production cao vì:
> 1. **Kiến trúc nhiều lớp bảo vệ độc lập** (không phụ thuộc vào 1 điểm duy nhất).
> 2. **Đã tích hợp Live Dashboard & Telegram Admin Bot** cho phép con người vận hành thực tế.
> 3. **Đạt 100/100 điểm Autograder**, vượt qua 100% bài test hợp đồng dữ liệu và kiểm thử an ninh."*
