# Semester-1-project
                              Phân loại màu sắc hoa quả trong nông nghiệp
1. Giới Thiệu :
Lý do chọn đề tài :
Giới thiệu sản phẩm: Trong nông nghiệp hiện đại, việc phân loại màu sắc của nông sản như hoa quả và rau củ đóng vai trò quan trọng trong việc xác định chất lượng, phân loại . Phần mền phân loại màu sắc  này ứng dụng công nghệ xử lý hình ảnh và học máy để tự động phát hiện, phân loại các màu sắc cơ bản (đỏ, xanh, cam), giúp cải thiện tốc độ và độ chính xác trong việc kiểm tra chất lượng nông sản.

Mục tiêu dự án :
Phân loại và đếm số lượng các đối tượng dựa trên màu sắc: đỏ, xanh, cam.
 Tạo ra một hệ thống trực quan, dễ sử dụng thông qua giao diện người dùng (GUI).
2. Phạm vi và đối tượng :
 Phạm vi ứng dụng và đối tượng sử dụng  :
  Nông dân và nhà sản xuất nông sản : Giúp người nông dân  phân loại hoa quả theo màu sắc ngay tại nông trại hoặc cơ sở sản xuất , đồng thời đánh giá độ chín của nông sản dựa trên màu sắc để quyết định thời điểm thu hoạch hoặc xử lý tiếp theo.Nhằm tiết kiệm thời gian so với phương pháp thủ công , tăng độ chính xác cao 

 Doanh nghiệp chế biến và xuất khẩu  nông sản: Giúp các nhà doanh nghiệp kiểm tra chất lượng đầu vào trước khi đưa vào dây chuyền sản xuất hay xuất khẩu , cho ra những  sản phẩm đạt tiêu chuẩn về màu sắc khi phân phối đến siêu thị hoặc thị trường. Đảm bảo chất lượng sản phẩm đồng nhất , tăng sự hài long đối với khách hàng , tối ưu hoá quá trình kiểm tra và phân loại trước khi đóng gói .

Trong gia đình : Giúp kiểm tra chất lượng sản phẩm  khi sử dụng các mặt hàng mua từ chợ , giảm tránh tình trạng sử dụng những mặt hàng hỏng , không đảm bảo chất lượng .




3. Các chức năng chính :
Xử lý hình ảnh  :
Phần mền sử dụng web cam để lấy dữ liệu hình ảnh có độ chính xác cao.


Phân loại màu sắc chính xác  : 
Nhận diện và phân loại các màu đỏ, xanh lá cây, và cam từ hình ảnh thu được qua webcam.

Phân loại dựa trên giá trị màu sắc (Hue), độ bão hòa (Saturation), và độ sáng (Value) của từng điểm ảnh trong không gian màu HSV.

Kết hợp hiệu quả giữa phát hiện chuyển động và phân loại màu sắc  : 
Phát hiện chuyển động trong khung hình trước khi thực hiện phân tích màu sắc.

Chỉ phân tích màu sắc khi có chuyển động, giúp tối ưu hóa tài nguyên và giảm tải xử lý.

Đếm và hiển thị số lượng từng màu sắc phát hiện được 
Ghi nhận số lượng các màu sắc đã được phát hiện trong hình 

 Hiển thị kết quả theo thời gian thực trên giao diện người dùng.

Đếm và hiển thị số lượng từng màu sắc phát hiện được 
 Giao diện được thiết kế bằng Tkinter, hỗ trợ các thao tác như bắt đầu, dừng chương trình, và hiển thị kết quả.

  Khung hiển thị video trực tiếp từ webcam kèm hộp đánh dấu vùng phát hiện màu sắc.


4. Công nghệ sử dụng :
Ngôn ngữ lập trình :
Sử dụng ngôn ngữ lập trình python 

Thư viện và framework hỗ trợ:
Thư viện OpenCV: Đây là thư viện chủ yếu dùng để xử lý hình ảnh và video. Bạn sử dụng OpenCV để đọc video từ webcam, chuyển đổi giữa các không gian màu (BGR -> HSV), phát hiện chuyển động, và hiển thị khung hình.

Thư viện NumPY: Dùng để xử lý mảng và các phép toán với ảnh (hình ảnh trong OpenCV thường được lưu dưới dạng mảng NumPy). 

Thư Viện PIL (Pillow): Dùng để chuyển đổi ảnh từ OpenCV sang định dạng mà Tkinter có thể hiển thị.
 Thư viện tkinter: Thư viện tạo giao diện người dùng (GUI) cho ứng dụng, cho phép bạn hiển thị video, các nhãn để đếm màu sắc, và các nút bấm.
Thư viện threading: Dùng để tạo các luồng 
Thư viện threads : Dùng  để xử lý các tác vụ song song, ví dụ: xử lý video và giao diện người dùng đồng thời 
Thư viện time : Dùng để đo thời gian giữa các lần phát hiện chuyển động


5.  Hình ảnh giao diện và quy trình sử dụng :
Hình ảnh phần mền :

Quy trình sử dụng  :
1. Người dùng khởi động hệ thống qua nút Start 
2. Webcam phát hiện đối tượng trong vùng quan sát.
3. Hệ thống xử lý và phân tích màu sắc, hiển thị kết quả đếm theo thời gian thực.
4. Người dùng nhấn nút End để dừng hệ thống và xem kết quả tổng hợp
6. Kết quả đạt được :
Hỗ trợ giúp con người  phân loại hoa quả dựa trên màu sắc, ví dụ: xác định độ chín của trái cây như cam, ớt, táo, v.v.
Giảm sự phụ thuộc vào các phương pháp phân loại thủ công phương pháp không có hiệu quả cao , tăng năng suất lao động và độ đồng đều của sản phẩm.
Thay thế con người , giảm bớt nhân công , giảm bớt gánh nặng về nhân công cho các doanh nghiệp 
Thời gian phản hồi nhanh và cho ra kết quả chính xác nhất .
Đảm bảo hệ thống hoạt động ổn định ngay cả khi chạy liên tục trong thời gian dài không ngừng nghỉ 
7. Phát triển và cải tiến :
Phát triển và cải tiến  :
Mở rộng ứng dụng của phần mềm : Thêm các loại màu sắc và có thể áp dụng vào phân loại nhiều đối tượng khác.
Triển khai các thuật toán để nhận diện hình dạng , kích thước , loại quả nhằm phân loại ra những sản phẩm đồng đều.
Áp dụng các lĩnh vực khác ngoài nông nghiệp 





