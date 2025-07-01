# 🧪 HƯỚNG DẪN TEST THỦ CÔNG GAME HỆ THỐNG MÃ HÓA NGÂN HÀNG

## 📋 Tổng quan

Hướng dẫn này giúp bạn test thủ công tất cả các chức năng của game để đảm bảo mọi thứ hoạt động đúng trước khi báo cáo.

---

## 🚀 Bước 1: Khởi động và kiểm tra giao diện

### 1.1 Khởi động game

```bash
python mau.py
```

### 1.2 Kiểm tra giao diện chính

- [ ] **Header**: Logo 🏦, tiêu đề, phụ đề hiển thị đúng
- [ ] **Status bar**: Tên người chơi, cấp độ, điểm, điểm cao nhất, thời gian, số giao dịch
- [ ] **Panel trái**: Giao dịch mới với thông tin chi tiết
- [ ] **Panel phải**: Kết quả xử lý và phản hồi
- [ ] **Các nút**: Màu sắc đúng, hiệu ứng hover hoạt động

### 1.3 Kiểm tra theme và màu sắc

- [ ] Màu xanh đậm cho header
- [ ] Màu xanh nhạt cho status bar
- [ ] Các nút có màu phân biệt: xanh (AES), đỏ (RSA), cam (SHA), xanh lá (Hoàn tất)
- [ ] Hiệu ứng hover khi rê chuột vào nút

---

## 🔐 Bước 2: Test chức năng mã hóa AES

### 2.1 Test mã hóa giao dịch

1. **Nhấn nút "🔐 Mã hóa AES"**
   - [ ] Nút chuyển sang màu xanh lá và text "✅ AES Hoàn tất"
   - [ ] Nút "✍️ Xác thực RSA" được enable và chuyển sang màu đỏ
   - [ ] Panel phải hiển thị thông báo "🔐 MÃ HÓA AES THÀNH CÔNG!"
   - [ ] Hiển thị thông tin: khóa AES, IV, dữ liệu mã hóa

### 2.2 Kiểm tra logic

- [ ] Không thể nhấn RSA trước khi mã hóa AES
- [ ] Thông báo cảnh báo nếu thao tác sai thứ tự

---

## ✍️ Bước 3: Test chức năng xác thực RSA

### 3.1 Test xác thực giao dịch

1. **Nhấn nút "✍️ Xác thực RSA"**
   - [ ] Nút chuyển sang màu xanh lá và text "✅ RSA Hoàn tất"
   - [ ] Nút "🔍 Kiểm tra SHA" được enable và chuyển sang màu cam
   - [ ] Panel phải hiển thị thông báo "✍️ XÁC THỰC RSA THÀNH CÔNG!"
   - [ ] Hiển thị thông tin: thông điệp ký, chữ ký RSA, trạng thái xác thực

### 3.2 Kiểm tra logic

- [ ] Không thể nhấn SHA trước khi xác thực RSA
- [ ] Thông báo cảnh báo nếu thao tác sai thứ tự

---

## 🔍 Bước 4: Test chức năng kiểm tra SHA

### 4.1 Test kiểm tra toàn vẹn

1. **Nhấn nút "🔍 Kiểm tra SHA"**
   - [ ] Nút chuyển sang màu xanh lá và text "✅ SHA Hoàn tất"
   - [ ] Nút "✅ Hoàn tất giao dịch" được enable và chuyển sang màu xanh lá
   - [ ] Panel phải hiển thị thông báo "🔍 KIỂM TRA TÍNH TOÀN VẸN SHA THÀNH CÔNG!"
   - [ ] Hiển thị thông tin: hash SHA-256, trạng thái kiểm tra

### 4.2 Kiểm tra logic

- [ ] Không thể hoàn tất giao dịch trước khi kiểm tra SHA
- [ ] Thông báo cảnh báo nếu thao tác sai thứ tự

---

## ✅ Bước 5: Test hoàn tất giao dịch

### 5.1 Test hoàn tất

1. **Nhấn nút "✅ Hoàn tất giao dịch"**
   - [ ] Tất cả nút bị disable
   - [ ] Panel phải hiển thị thông báo "🎉 GIAO DỊCH HOÀN TẤT!"
   - [ ] Hiển thị điểm thưởng, tổng điểm, cấp độ
   - [ ] Status bar cập nhật điểm số và số giao dịch

### 5.2 Kiểm tra điểm số

- [ ] Điểm cơ bản: 100
- [ ] Thưởng cấp độ: Cấp độ × 50
- [ ] Thưởng hoàn thành: 200
- [ ] Tổng điểm được tính đúng

---

## ⏰ Bước 6: Test chức năng timer

### 6.1 Test countdown

1. **Tạo giao dịch mới**
   - [ ] Timer bắt đầu từ 30 giây (hoặc adaptive_timer)
   - [ ] Timer đếm ngược mỗi giây
   - [ ] Màu timer thay đổi: vàng → cam → đỏ khi sắp hết giờ

### 6.2 Test timeout

1. **Để timer hết giờ**
   - [ ] Hiển thị "⏰ HẾT GIỜ! Giao dịch bị hủy"
   - [ ] Tất cả nút bị disable
   - [ ] Không được cộng điểm
   - [ ] Giao dịch được lưu vào lịch sử với trạng thái "Hết giờ"

---

## 🏆 Bước 7: Test hệ thống thành tựu

### 7.1 Test achievement

1. **Hoàn thành 3 giao dịch liên tiếp**

   - [ ] Hiện popup "🏅 Thành tựu: 3 giao dịch liên tiếp thành công!"

2. **Đạt 1000 điểm**

   - [ ] Hiện popup "🏅 Thành tựu: Đạt 1000 điểm!"

3. **Lên cấp 5**
   - [ ] Hiện popup "🏅 Thành tựu: Lên cấp 5!"

---

## 🎮 Bước 8: Test mini-game

### 8.1 Test xuất hiện mini-game

1. **Hoàn thành 3 giao dịch**
   - [ ] Mini-game xuất hiện sau giao dịch thứ 3
   - [ ] Cửa sổ popup với câu hỏi bảo mật

### 8.2 Test trả lời câu hỏi

1. **Trả lời đúng**

   - [ ] Hiện thông báo "🎉 Đúng! Bạn được cộng 100 điểm!"
   - [ ] Điểm được cộng vào tổng điểm

2. **Trả lời sai**
   - [ ] Hiện thông báo "❌ Sai! Đáp án đúng là: [đáp án]"

---

## 📊 Bước 9: Test bảng xếp hạng

### 9.1 Test lưu điểm

1. **Hoàn thành một số giao dịch**
   - [ ] Điểm được lưu vào leaderboard.json
   - [ ] File được tạo với encoding UTF-8

### 9.2 Test hiển thị bảng xếp hạng

1. **Nhấn nút "🏆 Bảng xếp hạng"**
   - [ ] Hiện popup với top 5 người chơi
   - [ ] Hiển thị tên và điểm số đúng thứ tự

---

## 📋 Bước 10: Test lịch sử giao dịch

### 10.1 Test lưu lịch sử

1. **Hoàn thành một số giao dịch**
   - [ ] Giao dịch được lưu vào lich_su_giao_dich
   - [ ] Bao gồm đầy đủ thông tin: ID, số tiền, kết quả, điểm

### 10.2 Test xem lịch sử

1. **Nhấn nút "🗂 Lịch sử giao dịch"**
   - [ ] Hiện cửa sổ với danh sách giao dịch
   - [ ] Double-click để xem chi tiết từng giao dịch

---

## 🎯 Bước 11: Test adaptive difficulty

### 11.1 Test giảm độ khó

1. **Hoàn thành 3 giao dịch liên tiếp thành công**
   - [ ] adaptive_timer giảm 2 giây
   - [ ] Giao dịch tiếp theo có thời gian ngắn hơn

### 11.2 Test tăng độ khó

1. **Để hết giờ liên tục**
   - [ ] adaptive_timer tăng 2 giây
   - [ ] Giao dịch tiếp theo có thời gian dài hơn

---

## 🔄 Bước 12: Test giao dịch mới

### 12.1 Test tạo giao dịch mới

1. **Nhấn nút "🔄 Giao dịch mới"**
   - [ ] Giao dịch mới được tạo với thông tin khác
   - [ ] Timer reset về thời gian mới
   - [ ] Tất cả nút reset về trạng thái ban đầu
   - [ ] Panel trái hiển thị thông tin giao dịch mới

---

## ❓ Bước 13: Test hướng dẫn

### 13.1 Test hướng dẫn

1. **Nhấn nút "❓ Hướng dẫn"**
   - [ ] Hiện popup với hướng dẫn chi tiết
   - [ ] Bao gồm mục tiêu, các bước, hệ thống điểm, tips

---

## 📈 Bước 14: Test thăng cấp

### 14.1 Test thăng cấp

1. **Hoàn thành 3 giao dịch**
   - [ ] Hiện popup "🎉 Chúc mừng! Bạn đã lên cấp độ [số]!"
   - [ ] Cấp độ tăng lên trong status bar
   - [ ] Điểm thưởng cấp độ tăng theo

---

## 🧹 Bước 15: Test cleanup và lỗi

### 15.1 Test xử lý lỗi

1. **Thử các thao tác sai thứ tự**
   - [ ] Thông báo cảnh báo hiển thị đúng
   - [ ] Game không bị crash

### 15.2 Test đóng game

1. **Đóng cửa sổ game**
   - [ ] Game đóng an toàn
   - [ ] File leaderboard.json được lưu đúng

---

## 📊 Báo cáo kết quả test

### Kết quả tổng hợp

- [ ] **Tổng số test case**: 15 bước chính
- [ ] **Test case thành công**: \_\_\_/15
- [ ] **Test case thất bại**: \_\_\_/15
- [ ] **Tỷ lệ thành công**: \_\_\_%

### Các vấn đề phát hiện

1. **Vấn đề 1**: [Mô tả vấn đề]
2. **Vấn đề 2**: [Mô tả vấn đề]
3. **Vấn đề 3**: [Mô tả vấn đề]

### Đánh giá tổng thể

- [ ] **Giao diện**: Đẹp và dễ sử dụng
- [ ] **Chức năng**: Hoạt động đúng như thiết kế
- [ ] **Hiệu suất**: Mượt mà, không lag
- [ ] **Bảo mật**: Các thuật toán mã hóa hoạt động đúng
- [ ] **Trải nghiệm người dùng**: Tốt, có phản hồi rõ ràng

---

## 🎉 Kết luận

Game "Hệ thống mã hóa ngân hàng" đã được test toàn diện!

**Lưu ý**: Chạy test này trước khi báo cáo để đảm bảo mọi chức năng hoạt động hoàn hảo.
