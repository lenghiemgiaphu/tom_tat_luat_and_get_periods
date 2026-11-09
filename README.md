# README.md
1) tom_tat_luat.md: bản tóm tắt luật bản 3, đã hợp nhất rulebook train + public (thêm 3 ngành Mẹ và bé, Sửa xe, Điện thoại; thêm danh hiệu như khách sộp, giờ cao điểm) và mục 9 "Bẫy thường gặp" kèm ví dụ. T làm hơi dài xíu, để ý token prompt. 

2) get_periods.py + test_get_periods.py: hàm kỳ thời gian theo rulebook §2 (hôm nay/qua, tuần, tháng, quý, N ngày gần nhất, Tết và trước Tết, ca sáng/chiều). Chỉ cần pandas. Mọi kỳ là (start, end) gồm cả hai đầu; lọc bằng in_period(series, period), đừng tự so <= end vì sẽ mất đơn có giờ của ngày cuối. Chạy test: python -m unittest test_get_periods -v (cần calendar.csv cạnh file test, đã có trong repo; mình chạy ra 32 test OK). Khi chạy thật phải đọc calendar trong /data của từng bộ, không ghi cứng.

3) cau_mau_de_xuat.md / .jsonl: 20 câu train để làm câu mẫu, đã loại biz_105, biz_118, biz_124, phủ đủ 8 kiểu đáp án. Chưa có code. Chạy agent trên đúng 20 id này rồi gửi mình lần chạy đúng để ghép thành bộ (câu hỏi, code, đáp án).

4) answers.jsonl, calendar.csv: dữ liệu train. Ai dùng answers.jsonl nhớ loại 3 tiệm giữ riêng.

Chưa làm: "cùng kỳ năm ngoái", "quý này", kỳ so của "tuần này" (rulebook không định nghĩa). Gặp các câu này thì theo chữ câu hỏi hoặc abstain.

Hai việc cần nhóm quyết:
- Giao diện agent ↔ hàm: agent import các hàm này, hay đọc file thô bằng pandas? Thịnh chờ chốt trước khi sinh data finetune.
- Đề xuất: lúc chạy, nạp thêm rulebook.md của bộ đang chạy (khoảng 24 KB) vào prompt cùng bản tóm tắt, để private có ngành mới thì luật tự vào. Bản giải pháp khoá 23:59 ngày 16/11, trước khi private phát, nên không vá tay được.
