# tom_tat_luat_-_get_periods
# Tóm tắt luật DataMate (cho prompt), bản 3 theo rulebook public. Sai luật = −1 điểm

**Hôm nay = `as_of_date`.** Bản ghi sau hôm nay coi như chưa xảy ra (riêng trạng thái huỷ/trả lấy theo trạng thái ghi trên đơn, kể cả khi phiếu trả ghi ngày sau hôm nay). Câu hỏi nói khác luật mặc định thì theo câu hỏi. Luật ngành khác luật chung thì theo luật ngành.

## 1. Đơn và doanh thu
- **Đơn hợp lệ** = không huỷ, không trả hàng. Trả hàng, **kể cả trả một phần**, bỏ **cả đơn**; đơn trả hàng sau kỳ (kể cả sau hôm nay) vẫn bị loại khỏi kỳ đặt. Đơn đang giao vẫn tính. Đơn trả hàng **không phải** đơn huỷ.
- **Doanh thu đơn** = tổng thành tiền các dòng (đã trừ giảm giá từng dòng). **Không** trừ giảm giá/voucher cả đơn, **không** cộng VAT, **không** gồm phí giao. "Bán được bao nhiêu tiền", "thu về", "tiền hàng", "tiền bán" = doanh thu, không phải tiền khách đã trả. *Vd: dòng 300k + 200k, voucher cả đơn −50k → doanh thu 500.000.*
- **Kỳ của đơn = ngày đặt** (không phải ngày giao, ngày thu tiền).
- Số đơn, số khách mua, số đơn có mặt hàng X: chỉ đếm đơn hợp lệ. **Khách đã mua** trong kỳ = có ≥ 1 đơn hợp lệ trong kỳ.
- **Tỉ lệ huỷ** = đơn huỷ ÷ **mọi** đơn đặt trong kỳ (cả huỷ, trả, đang giao) × 100, 2 chữ số thập phân.
- **% thay đổi** so với kỳ trước, giảm thì ra số âm. **Chênh lệch** (số, không %) = kỳ hỏi − kỳ so, ít hơn ra số âm.
- Theo hình thức thanh toán: theo hình thức **ghi trên đơn**; đơn ghi nợ không vào tiền mặt/chuyển khoản; COD là hình thức riêng.
- Theo nhóm khách: khách vãng lai không thuộc nhóm nào (kể cả nhóm "lẻ"); tỉ trọng chia cho doanh thu **cả shop**, gồm cả đơn vãng lai.
- **Báo cáo tiền mặt theo ca**: chỉ tiền mặt, theo **giờ thu tiền**, gồm cả tiền khách trả nợ. Doanh thu, số đơn thì tính từ đơn hàng (ngày, giờ đặt), không lấy từ báo cáo ca.

## 2. Thời gian
- Hôm nay/hôm qua/ngày X (số phát sinh: doanh thu, số đơn, giá bán…): chỉ trong ngày đó. **Đến hết ngày X / tính đến hôm nay** (số còn lại: nợ, tồn, còn hàng, chưa giao): tình trạng lúc hết ngày, cộng mọi phát sinh **từ đầu dữ liệu** (không phải "tháng này").
- Từ X đến Y: gồm cả X, Y. **N ngày gần nhất**: N ngày liền nhau, kể cả hôm nay. Quá/hơn/trên/dưới N: **không** gồm N; từ N trở lên: gồm N.
- **Tuần bắt đầu thứ Hai.** Tuần này: T2 → hết hôm nay. Tuần trước/rồi: **cả** tuần T2–CN liền trước.
- Tháng M/Y: cả tháng. **Tháng này**: ngày 1 → hết hôm nay; so với tháng trước thì lấy **cùng số ngày**: hôm nay 15/10 → 01–15/09; hôm nay 31/03 → so với cả tháng 2. Từ đầu năm: 01/01 → hết hôm nay.
- Tháng M / quý Q không ghi năm: năm nay nếu không sau hôm nay, nếu sau thì năm trước. Quý dương lịch (Q1 = tháng 1–3).
- **Tết năm Y** (dịp Tết, mùa Tết): 23 tháng Chạp (năm âm Y−1) → **hết** mùng 10 tháng Giêng (năm âm Y), tra `calendar.csv`. "So với trước Tết" = cùng số ngày ngay trước 23 tháng Chạp.
- Ca sáng 06:00–13:59, ca chiều 14:00–21:59 (giờ tạo đơn); so ca chiều với ca sáng thì mốc là ca sáng.
- **Trung bình mỗi ngày thứ X của kỳ**: chia cho số ngày thứ X trong kỳ, kể cả ngày không có đơn/phiếu.

## 3. Xếp hạng, đếm
- Món/hàng/sản phẩm = mặt hàng. Dòng **Phí phục vụ**: không xếp hạng, không đếm, nhưng vẫn tính vào doanh thu (kể cả mẫu số tỉ trọng nhóm). Nhóm hàng: đúng tên nhóm câu hỏi nêu, không gộp nhóm khác tên.
- **Bán chạy / nhiều nhất / hot nhất** = theo **số lượng quy về đơn vị cơ bản** (không theo số dòng, số tiền), bỏ đơn huỷ/trả. Mặt hàng khác đơn vị cơ bản vẫn xếp chung theo số quy đổi đó.
- **"Bán được bao nhiêu <đơn vị>"**: cộng số lượng quy đổi của các mặt hàng có đơn vị cơ bản đúng là đơn vị đó (kể cả dòng bán theo đơn vị lớn). Hệ số đọc ở bảng quy đổi/README; không có dòng quy đổi = đơn vị cơ bản, hệ số 1.
- **Khách**: có mã khách → mỗi mã một khách (hai mã trùng tên là hai khách); không có mã → theo tên trên đơn (chỉ khác cách viết = cùng khách; khác chữ hoặc khác số = hai khách). **Khách lẻ không đếm, không xếp hạng.** "Mua nhiều tiền nhất" theo doanh thu.
- Nhân viên bán giỏi nhất theo **doanh thu**, không theo số đơn. Hàng lời nhất theo tổng lãi gộp.
- **Danh hiệu theo kỳ**: *khách trung thành* = nhiều **ngày có mua** nhất; *khách sộp* = giá trị trung bình một đơn cao nhất, chỉ xét khách **từ 3 đơn** trở lên; *khách hay đổi ý* = nhiều **đơn huỷ** nhất; *mặt hàng được ưa chuộng* = có mặt trong **nhiều đơn nhất**; *ngày đắt khách* = ngày **nhiều đơn nhất**; *nhân viên/thợ chăm chỉ* = **nhiều ngày làm việc** nhất (ngày có ≥ 1 đơn, kể cả phiếu bảo hành, do người đó bán/làm); *giờ cao điểm* = khung một giờ tròn (theo giờ tạo đơn) nhiều đơn nhất, đáp án là **giờ bắt đầu khung**, type `number`.
- Bằng nhau → **mã tăng dần** (không mã: tên). Giá trị trung bình một đơn: về đồng, nửa đồng làm tròn lên.

## 4. Công nợ
- Tính đơn không huỷ; **đơn trả hàng vẫn tính** nếu còn nợ. Nợ một đơn tại ngày X = tổng đơn (đã trừ giảm giá cả đơn, **gồm phí giao**) − các khoản trả đến hết X; tổng nợ = cộng các đơn còn nợ > 0.
- Nợ theo khách: xác định khách như §3; đơn khách lẻ tính vào **tổng nợ** nhưng không có dòng trong bảng nợ theo khách.
- **COD và đơn sàn TMĐT không phải khách nợ**, bỏ khỏi công nợ và tuổi nợ (kể cả chưa thu được tiền). **Tuổi nợ** tính từ **ngày đặt**: đặt hôm nay = 0, hôm qua = 1.
- Trong kỳ (chỉ đơn **ghi nợ**, không huỷ): **nợ thêm** = phần tổng đơn chưa trả ngay trong ngày mua, của đơn đặt trong kỳ. **Trả/thu nợ** = khoản trả **sau ngày mua** có ngày trong kỳ, của mọi đơn ghi nợ (cả đơn kỳ trước, đơn trả hàng). Trả cùng ngày mua là trả lúc mua; hoàn tiền trả hàng không trừ.

## 5. Kho, nhập hàng, giá vốn
- Tiền nhập trong kỳ = tổng phiếu nhập có **ngày phiếu** trong kỳ, bỏ phiếu huỷ ("nhập đầu kỳ" vẫn là phiếu nhập). **Nhà cung cấp nhập nhiều nhất** = tiền nhập cao nhất; **nhà cung cấp chính** = **nhiều phiếu nhập nhất** (bỏ phiếu huỷ), hai thứ khác nhau.
- Nhập trừ bán: phần bán là số lượng đơn hợp lệ, cùng đơn vị với phần nhập.
- Giá trị tồn kho = tồn hết hôm nay × giá vốn một đơn vị cơ bản ghi trong danh mục, chỉ hàng còn tồn.
- Hết hàng cuối ngày: hàng mua về để bán (không phải món pha chế/chế biến tại chỗ) có tồn 0 lúc **hết ngày** (hết giữa ngày nhưng nhập thêm trước cuối ngày thì không tính). Mặt hàng ế trong kỳ: đã bán trước kỳ (đơn hợp lệ) nhưng không có đơn hợp lệ nào trong kỳ.
- **Tăng giá**: lần tăng = ngày D giá mới cao hơn giá liền trước theo bảng giá (cùng một giá nhiều lần thì lấy lần đầu). So số lượng (đơn vị cơ bản) N ngày kể từ D (tính cả D) với N ngày ngay trước D; bỏ đơn huỷ/trả.
- Giá vốn là bình quân gia quyền theo lô nhập tại lúc bán (không FIFO). **Lãi gộp** = doanh thu − Σ(số lượng × giá vốn **ghi trên dòng bán**, tính cho một đơn vị bán, cùng đơn vị với đơn giá); không tự tính từ phiếu nhập hay lô. Lãi ròng tháng = lãi gộp − mọi khoản trong sổ chi phí tháng đó (kể cả sửa chữa, thay thiết bị).
- *(Còn trong rulebook train, public không nhắc, giữ lại)* Giá nhập bình quân tháng = bình quân **theo số lượng nhập** (không phải trung bình cộng các giá), theo đơn vị nhập, phiếu trong tháng, bỏ phiếu huỷ. Tồn theo đơn vị lớn → list `[số đơn vị lớn nguyên, số cơ bản lẻ]` (không lẻ thì 0; hàng nhiều cấp: phần lẻ tính bằng đơn vị cơ bản, không đổi sang đơn vị ở giữa). **Giá bán X ngày D** = đơn giá ghi trên dòng bán, **một đơn vị cơ bản**, **trước** chiết khấu dòng, tính cả đơn huỷ/trả.

## 6. Luật ngành (khác luật chung thì theo luật ngành)
- **Cà phê**: size M/L = tên món kết thúc `(M)`/`(L)`, không phân biệt hoa thường. Topping ghi chung ô với món là **hai** mặt hàng: số lượng, tiền topping tính vào mặt hàng topping (cùng mặt hàng với topping ghi dòng riêng), không tính vào món.
- **Nhà thuốc**: kê đơn = ghi kê đơn trong danh mục thuốc (còn lại là không kê đơn; tỉ lệ kê đơn theo doanh thu). Hết hạn trong N ngày tới (hôm nay D): lô **còn tồn** có hạn từ D đến hết D+N; tiền vốn = phần còn tồn × giá nhập **của chính lô đó** quy về đơn vị cơ bản (không theo giá vốn bình quân). Theo hoạt chất: đúng hoạt chất ghi trong danh mục; thuốc phối hợp là một loại riêng. Lô gần hết hạn nhất: lô còn tồn, chưa quá hạn, hạn sớm nhất.
- **Vật liệu xây dựng**: tính đến hết hôm nay. Số đợt giao trong tháng = số đợt có ngày giao trong tháng; mỗi đợt của mỗi đơn là một đợt, kể cả đơn sau đó trả hàng.
- **Mẹ và bé**: tiền giảm voucher, giảm nhờ dùng điểm, phí ship → trả **số dương**, cộng theo **ngày hoá đơn**, chỉ hoá đơn hợp lệ. Số sữa, size bỉm lấy theo cột Số/Size của danh mục (để trống thì không xếp vào số/size nào dù tên có số); phần trăm của một size/hãng chia cho tổng số bịch mọi hàng **bỉm tã** cùng kỳ. Khách thành viên mới trong tháng = số khách có **Ngày đăng ký** trong tháng, kể cả chưa mua lần nào.
- **Sửa xe**: mỗi dòng sổ = một **lượt xe** (phiếu), kể cả bảo hành; một xe tới hai lần là hai lượt. Số phiếu/lượt xe của tiệm hay của thợ **tính cả bảo hành**; tiền trung bình một phiếu chia cho số phiếu **có thu tiền**. Thợ làm nhiều nhất theo số lượt xe (kể cả bảo hành). Việc ghi ở ô Làm gì: lượt có làm việc đó = một lượt; `Nhớt` ghi trơn là nhớt máy (không phải nhớt láp); `ruột` ghi trơn là thay ruột mới (không phải vá); **Sửa điện** không gồm thay bóng đèn, thay ắc quy; phiếu bảo hành **không** tính là lượt làm việc đó. Dòng xe chỉ khác hoa/thường hoặc ghi tắt = cùng dòng. **Số xe** = số biển số khác nhau, tính cả xe chỉ tới bảo hành. **Tỉ lệ bảo hành** = số phiếu bảo hành có ngày trong kỳ ÷ số phiếu có thu tiền cùng kỳ (bảo hành của xe sửa từ kỳ trước vẫn tính). **Xe khách quen** = xe (theo biển số) có ≥ 2 phiếu **có thu tiền** trong kỳ (bảo hành không tính); câu hỏi "xe nào" trả biển số.
- **Cửa hàng điện thoại**: **khách phải trả** = tiền đơn sau bớt và sau trừ máy cũ, gồm cả phần còn nợ; tiền thu máy cũ **không** trừ vào doanh thu; tổng khách phải trả và tiền thu máy cũ chỉ tính đơn hợp lệ. **Trả góp** là đơn **ghi nợ**: phần góp chưa trả là nợ, tiền góp mỗi kỳ là trả nợ (vào thu nợ), **không** vào doanh thu (doanh thu đã tính đủ giá máy ngày mua); tiền trả trước không phải tiền góp. Câu về khách nợ, mua chịu, trả nợ, thu nợ gồm cả đơn trả góp dù sổ góp ghi riêng. Kỳ góp có hạn **trước** ngày hỏi mà chưa đủ là **quá hạn**; hạn đúng ngày hỏi thì chưa quá hạn. **Tỉ lệ bảo hành quý** = số **lượt** bảo hành có ngày nhận trong quý ÷ số máy bán trong quý (bỏ huỷ/trả); lượt của máy bán từ quý trước vẫn tính. **Dòng máy** = phần tên đứng trước dung lượng `…GB` (không có `…GB` thì cả tên; `Nokia 105 4G`: 4G là mạng). **Hãng** = chữ đầu tên hàng; `iPhone` là Apple. Máy khách mang tới đổi không phải máy bán.

## 7. Không trả lời được → `{"type":"unanswerable","reason":"..."}`
- Shop không ghi loại thông tin cần (vd hỏi lãi gộp mà không có giá vốn), hoặc kỳ nằm **hoàn toàn** ngoài khoảng ngày có dữ liệu → **unanswerable, không phải 0**. Không suy từ cột khác (trừ khi rulebook ghi cách lấy), không dùng hiểu biết ngoài. Kỳ chỉ một phần trong khoảng có dữ liệu → tính phần có dữ liệu.
- `reason` nếu có phải là **chuỗi** (không phải chuỗi thì dòng tính như bỏ trống).

## 8. Định dạng đáp án (sai format = sai)
- `number`: JSON number, tiền là số nguyên VND, không đơn vị/dấu phân cách (không `"4.820.000"`, không `"4820000"`). `percent`: `12.4` cho 12,4% (không `"12,4%"`, không `0.124`). `date`: `"YYYY-MM-DD"`, câu hỏi theo tháng `"YYYY-MM"`. `boolean`: `true`/`false`.
- `string`: chép nguyên văn tên trong dữ liệu (hoặc mã), đủ dấu, không kèm tên cột/nhãn nhóm, không bọc mảng. Khi chấm: bỏ hoa/thường, dấu câu đổi thành khoảng trắng, nhiều khoảng trắng gộp một, nhưng **giữ dấu tiếng Việt và khoảng trắng giữa các từ** (`330 ml` ≠ `330ml`); nhận mọi cách viết tên có trong file, mã, hoặc tên kèm số điện thoại như trong file.
- `list`: mảng có thứ tự (một phần tử vẫn là mảng); nhiều số thì theo thứ tự câu hỏi. `table`: `{"columns":[...],"rows":[[...]]}`, mỗi dòng một đối tượng, cột đầu là tên đối tượng, cột sau theo thứ tự câu hỏi, ô số là number; cột so theo tên, không khớp thì theo vị trí.
- **Làm tròn**: tiền lẻ → về đồng (trung bình một khoản tiền cũng là tiền); phần trăm và trung bình khác → 2 chữ số thập phân, trừ khi luật khác ghi khác.
- **Thứ tự**: top k giảm dần theo tiêu chí. "Liệt kê" có số đo: giảm dần, bằng nhau thì mã tăng dần; theo hạn dùng: hạn sớm nhất của mặt hàng trước, cùng hạn thì mã tăng dần; chỉ lọc điều kiện: mã tăng dần. Bằng nhau ở tiêu chí → mã tăng dần (không mã: tên); câu hỏi một đối tượng thì lấy đối tượng đứng đầu theo thứ tự đó.
- **Không chắc → `{"type":"abstain"}` (0 điểm), tốt hơn đoán sai (−1).**

---
## Phụ lục (chỉ cần nếu agent đọc file thô, không dùng loader)
- Ô trống ở các dòng sau của cùng một nhóm dòng = giống dòng đầu nhóm (khách, ghi chú, trạng thái áp cho mọi dòng của đơn); không phải thiếu dữ liệu, không có nghĩa là khách lẻ hay đơn hoàn thành.
- Mỗi đơn có đúng một trong bốn trạng thái: hoàn thành, huỷ, trả hàng, đang giao (mỗi shop viết một kiểu). Sổ không có cột trạng thái thì trạng thái nằm ở cột Ghi chú; ghi chú không nhắc trạng thái = hoàn thành. Tên gọi cùng chỉ một thứ là một thứ; file có mã thì theo mã.
- Hai dòng giống nhau ở mọi ô của **cùng một đơn** = lỗi xuất file, tính một lần; của hai đơn khác nhau = tính cả hai. Bảng không ghi theo đơn: mỗi dòng là một lần ghi, trùng vẫn tính cả hai.
- Ngày không ghi năm = năm của sheet chứa dòng đó.
- Cẩn thận dữ liệu bẩn: dòng tiêu đề không ở dòng đầu, dòng tổng không có số lượng, tiền viết `396k` / `1,156tr` (dấu phẩy trước `tr`/`k` là dấu thập phân: 1,156 triệu = 1.156.000), số lượng `1 bao 25kg` (số đầu là số lượng).
