# Câu mẫu đề xuất (20 câu train, không có tiệm giữ riêng)

Nguồn: `questions.jsonl` + `answers.jsonl` của train. Loại biz_105, biz_118, biz_124. Mỗi câu chọn để phủ một kiểu đáp án hoặc một bẫy luật. **Chưa có code**: cần lấy từ lần chạy đúng của agent (hoặc viết tay, kiểm trên dữ liệu tiệm) rồi ghép thành bộ (câu hỏi, code, đáp án). Bản đầy đủ (kể cả đáp án dạng table) nằm trong `cau_mau_de_xuat.jsonl`.

| # | id | tiệm | as_of | câu hỏi | kiểu | đáp án | nhóm / kiểm tra điều gì |
|---|---|---|---|---|---|---|---|
| 1 | q_3f1616e84a29 | biz_121 | 2026-09-20 | xem giup trong thang 3/2025, ti le don huy la bn % ta | percent | 0.91 | **Tỉ lệ huỷ**: Mẫu số là MỌI đơn đặt trong kỳ (huỷ, trả, đang giao); percent 2 chữ số |
| 2 | q_8a6f40f8b51b | biz_129 | 2026-08-14 | dthu tháng 2/2026 tăng hay giảm bao nhiêu phần trăm so với tháng trước? | percent | -33.1 | **% so với tháng trước**: Giảm thì ra số âm; kỳ so là cả tháng liền trước |
| 3 | q_747ae991f1c1 | biz_103 | 2025-06-22 | ê tuần rồi dthu được bn | number | 33388800 | **Tuần rồi**: as_of là Chủ nhật 22/06/2025: tuần rồi = 09/06–15/06 (T2–CN), không phải 16–22/06 |
| 4 | q_9fd096dfdb84 | biz_128 | 2025-07-11 | Cho mình hỏi so với ca sáng, doanh thu ca chiều tuần trước chênh bao nhiêu %? | percent | 87.86 | **Ca chiều so với ca sáng**: Mốc là ca sáng; ca theo giờ tạo đơn; kỳ là tuần trước |
| 5 | q_cde1b334100f | biz_130 | 2026-08-29 | xem giup tu ngay 02/07/2026, com trang tang gia len 10.500đ. so 14 ngay ke tu ngay 02/07/2026 vs 14 ngay ngay truoc do, so phan ban ra thay doi bao nhieu phan tram | percent | 31.29 | **Tăng giá**: 14 ngày kể từ D (gồm D) so với 14 ngày ngay trước D; đơn vị cơ bản; bỏ đơn huỷ/trả |
| 6 | q_b0e965a3cb48 | biz_109 | 2026-08-05 | Tháng 4/2025 lãi gộp của cửa hàng là bao nhiêu? | number | 38056035 | **Lãi gộp**: Doanh thu trừ Σ(số lượng × giá vốn ghi trên dòng bán) |
| 7 | q_8659862171ab | biz_129 | 2026-08-14 | xem giúp top 5 khách có công nợ lớn nhất đến hết ngày 14/08/2026 và số nợ của từng người | table | {"columns": ["khach_hang", "so_tien_no"], "rows": [["Thân Th… | **Công nợ (table)**: Top 5 khách nợ đến hết ngày; bỏ COD/sàn; khách lẻ không có dòng; cột đầu là tên khách |
| 8 | q_1f99d93acad3 | biz_106 | 2025-07-26 | Giúp mình tính đến hết ngày 26/07/2025, khách còn nợ bao nhiêu ở nhóm tuổi nợ 0–7 ngày, 8–15 ngày và trên 15 ngày? | list | [403500, 857334, 229836] | **Tuổi nợ (list)**: Nhóm 0–7, 8–15, trên 15 (trên 15 không gồm 15); tuổi nợ tính từ ngày đặt |
| 9 | q_4deb7fd6f277 | biz_122 | 2026-07-17 | Cho hỏi cuối ngày hôm nay Savi Losartan 50mg hộp 3 vỉ x 10 viên còn mấy hộp chẵn, mấy viên lẻ? | list | [2, 22] | **Tồn đơn vị lớn (list)**: [số hộp nguyên, số viên lẻ]; phần lẻ tính bằng đơn vị cơ bản |
| 10 | q_02a70ea566f1 | biz_112 | 2026-07-31 | Top 3 sp bán nhiều nhất tháng 3 năm 2026 là những gì? | list | ["Cà phê sữa (M)", "Trà đào cam sả (M)", "Cà phê đen (M)"] | **Top bán chạy (list)**: Theo số lượng quy về đơn vị cơ bản; bỏ Phí phục vụ; hoà thì mã tăng dần |
| 11 | q_c6293f0e92c8 | biz_126 | 2026-06-06 | tháng 5/2025 ngày nào cửa hàng bán được nhìu tiền nhất | date | "2025-05-10" | **Ngày bán nhiều tiền nhất (date)**: Theo doanh thu đơn hợp lệ; trả về YYYY-MM-DD |
| 12 | q_a566c9b4142c | biz_123 | 2026-06-28 | thang 4/2026, hang nao co lai gop ca thang cao nhat z | string | "Blackmores Bio C 1000mg hộp 31 viên" | **Hàng lời nhất (string)**: Tổng lãi gộp theo mặt hàng; chép đúng tên mặt hàng, đủ dấu |
| 13 | q_3614b8c3f2b9 | biz_122 | 2026-07-17 | Doanh thu có tăng liên tục qua 3 tháng 12/2025, 1/2026, 2/2026 không? | boolean | false | **Doanh thu tăng liên tục (boolean)**: So doanh thu từng tháng liên tiếp; kiểu true/false |
| 14 | q_e35d8fac5233 | biz_117 | 2026-05-20 | Trong tháng 1 năm 2026, số khách mua ít nhất 3 đơn là bao nhiêu? | number | 128 | **Khách mua ít nhất N đơn**: 'Ít nhất 3' gồm 3; chỉ đơn hợp lệ; khách lẻ không đếm |
| 15 | q_8e3a17631a81 | biz_123 | 2026-06-28 | Giá trị trung bình một đơn tháng 3/2025 là bao nhiêu vậy? | number | 105122 | **Trung bình một đơn**: Nửa đồng làm tròn lên; doanh thu đơn hợp lệ ÷ số đơn hợp lệ |
| 16 | q_a666a74dcbea | biz_123 | 2026-06-28 | tinh den het ngay 28/06/2026, co may mat hang con lo ton sap het han trong 90 ngay toi, tuc han dung tu 28/06/2026 den het 26/09/2026 | number | 5 | **Nhà thuốc sắp hết hạn**: Lô còn tồn, hạn từ D đến hết D+N (28/06 → 26/09/2026) |
| 17 | q_a8008950c40b | biz_104 | 2026-06-02 | Tháng 11/2025 quán bán ra tổng cộng mấy ly size M, cộng tất cả các món nhỉ? | number | 2934 | **Cà phê size M**: Tên món kết thúc (M); cộng mọi món |
| 18 | q_0fbd522a4f2f | biz_106 | 2026-09-14 | Dịp Tết âm lịch 2026 có doanh thu hơn hay kém 17 ngày trước Tết bao nhiêu %? | percent | -41.86 | **Tết**: Tết 2026 = 10/02–26/02 (17 ngày); so với 17 ngày ngay trước 23 tháng Chạp |
| 19 | q_24ed0fa1deca | biz_103 | 2026-07-09 | Cuối ngày 09/07/2026, tổng giá trị hàng còn trong kho tính theo giá vốn là bao nhiêu tiền? | unanswerable | — | **Unanswerable (thiếu giá vốn?)**: Hỏi giá trị tồn theo giá vốn; đáp án chuẩn là unanswerable. Lý do là suy đoán, kiểm lại trên dữ liệu tiệm |
| 20 | q_03a446be8b75 | biz_121 | 2026-09-20 | trong thang 2/2025, ti le don huy la bao nhieu % | unanswerable | — | **Unanswerable (kỳ ngoài dữ liệu?)**: Tháng 2/2025 có thể nằm ngoài khoảng ngày có dữ liệu của tiệm. Lý do là suy đoán, kiểm lại trên dữ liệu tiệm |

Phủ kiểu đáp án: percent 5, number 6, table 1, list 3, date 1, string 1, boolean 1, unanswerable 2.

## Còn thiếu so với train
Train không có 3 ngành của public (Mẹ và bé, Sửa xe, Cửa hàng điện thoại), nên các ngành đó chưa có câu mẫu thật. Chỉ có rulebook mô tả luật. Khi cần, viết câu mẫu tự dựng từ luật, đừng lấy câu public.

## Tần suất họ câu hỏi trong train (đếm bằng từ khoá, các nhóm chồng lấn nhau)
Khách ~292, so với kỳ trước (%) ~212, trung bình một đơn ~136, tuần rồi/trước ~133, ngày nào/ngày bán nhiều nhất ~129, top/bán chạy ~129, size/topping ~118, công nợ ~116, nhập hàng ~113, ca sáng/chiều ~77, tăng giá ~70, cùng kỳ so ~66, tỉ lệ huỷ ~61, hoạt chất ~46, kê đơn ~44, tồn kho ~36, **Tết chỉ ~5 trên 3.000**. Ưu tiên soi lỗi ở các họ đông trước.
