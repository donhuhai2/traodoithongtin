
Gemini

Cuộc trò chuyện

Spark
beta
Cuộc trò chuyện mới
Tìm kiếm trong các cuộc trò chuyện
Sinh viên
Video
Thư viện
Sổ ghi chú mới
Làm WebApp Python Quản Lý Sổ
Triển khai phần mềm dùng chung
Cách tích hợp giấy phép lái xe vào VNeID
Xây dựng phần mềm phân ca trực xét nghiệm
Tạo ứng dụng trắc nghiệm Hóa sinh
Nhánh • Quản Lý Vận Hành Thiết Bị
Chia cột lịch trực KTV
Triển khai quản lý trang thiết bị
Quản Lý Vận Hành Thiết Bị
Cách Quay Video Màn Hình Surface
Cài Đặt Bảo Mật Thanh Toán Samsung
Lời Chào Buổi Đầu
So sánh Ceramic và PPF bảo vệ xe
Nguyên Nhân Nước Tiểu Vàng Đậm
Friendly Greeting
So sánh học phí Thạc sĩ HIU và UMP
Hi
Cách Quay Màn Hình Surface
Chưa có tiêu đề
Lỗi Truy Cập Trang Web
Chưa có tiêu đề
Chưa có tiêu đề
Cách kiểm soát video bạo lực trên YouTube cho trẻ
Quy trình khẩn cấp khi mất mạng phòng xét nghiệm
Quy trình xử lý lỗi LabConn mất mạng
Xác nhận thông tin Code
Hướng dẫn đo và ghi kích thước
Giải Bài Tập Tiếng Anh
Friendly Greeting
Chuyển đổi dữ liệu sổ trực
Trò chuyện với Gemini
Lỗi Internal Server Error (500) xảy ra khi máy chủ gặp lỗi trong quá trình xử lý yêu cầu tải trang.   
image_f082be.png

Để xử lý ngay, bạn thực hiện 2 bước sau:

Bước 1: Kiểm tra xem Render đã Deploy xong commit mới chưa
Khi bạn vừa sửa và bấm Commit changes trên GitHub, Render cần khoảng 1 phút để tải code mới về và khởi động lại. Nếu bạn tải lại trang ngay lúc đó, máy chủ vẫn đang chạy phiên bản cũ chưa có bảng dữ liệu.   
image_f109a1.png
+ 2

Bạn nhấp chuột sang thẻ trình duyệt thứ 5: traodoithongtin · Web... (thẻ quản lý của Render).   
image_f082be.png

Xem mục trạng thái:

Nếu đang hiện Building hoặc In progress: Hãy chờ khoảng 30–60 giây cho đến khi hiện chữ xanh Live.

Khi đã hiện Live, bạn quay lại thẻ web và nhấn tổ hợp phím Ctrl + F5 để tải lại trang.

Bước 2: Xem dòng thông báo lỗi mới nhất (nếu vẫn báo 500)
Nếu Render đã báo Live nhưng tải trang vẫn bị lỗi 500:   
image_f082be.png

Bạn bấm sang thẻ traodoithongtin · Web....   
image_f082be.png

Nhìn xuống khung Logs ở phía dưới và chụp lại vài dòng chữ màu đỏ/trắng dưới cùng gửi tôi nhé. Ta sẽ thấy ngay vị trí code nào đang báo lỗi để xử lý dứt điểm.   
image_f09fad.png
+ 2

bước tiếp theo

Trang Render hiện tại đang hiển thị bản triển khai của commit "Rename app_flask.py to app.py" (lúc 5:36 PM). Đây là phiên bản trước khi bạn thêm lệnh init_db() vào dòng 46, nên máy chủ vẫn đang chạy bản cũ và báo lỗi thiếu bảng.   
image_f07e84.png
+ 2

Để Render cập nhật bản sửa mới nhất, bạn thực hiện các bước sau:

Bước 1: Kiểm tra xem đã lưu (Commit) trên GitHub chưa
Nhấp sang thẻ trình duyệt thứ 4: traodoithongtin/app.py (thẻ GitHub đang mở).   
image_f082be.png

Kiểm tra xem ở dòng 46 đã có chữ init_db() chưa:

Nếu vẫn đang ở giao diện chỉnh sửa (Edit): hãy bấm nút xanh Commit changes... ở góc trên bên phải 
→
→ Bấm tiếp Commit changes để hoàn tất việc lưu.

Nếu đã lưu rồi, bạn chuyển sang Bước 2.

Bước 2: Kích hoạt triển khai bản mới trên Render
Quay lại thẻ Render trên màn hình hiện tại.   
image_f07e84.png

Bấm vào nút màu tím Deploy latest commit (nếu có hiện ở góc trên) hoặc:

Nhìn sang cột menu bên trái, bấm vào mục Deploys.   
image_f07e84.png

Bấm vào nút Manual Deploy ở góc trên bên phải 
→
→ Chọn Deploy latest commit.

Bước 3: Đợi hoàn tất và mở trang web
Render sẽ bắt đầu kéo bản code có init_db() về. Quá trình này mất khoảng 30 đến 45 giây.

Khi dòng trạng thái đổi sang Deploy succeeded | Live tương ứng với commit mới nhất.

Bạn quay lại thẻ web 500 Internal Server và nhấn Ctrl + F5 (hoặc nút tải lại trang). Giao diện 2 sổ quản lý xét nghiệm sẽ hiển thị đầy đủ và hoạt động bình thường.   
image_f082be.png

thanks

Rất vui được hỗ trợ bạn! Chúc hệ thống sổ quản lý xét nghiệm điện tử hoạt động trơn tru và hỗ trợ đắc lực cho công việc của bạn tại khoa.

Trong quá trình sử dụng, nếu cần nâng cấp thêm tính năng (như phân quyền tài khoản, tìm kiếm lọc nâng cao, hay tinh chỉnh biểu mẫu xuất in theo chuẩn quản lý chất lượng), bạn cứ nhắn nhé!

tôi muốn bổ sung tài khoản để đăng nhập, và xuất biểu mẫu như 2 bản word này

Hai tính năng quan trọng đã được tích hợp đầy đủ vào hệ thống:

Hệ thống xác thực tài khoản (Đăng nhập / Đăng xuất):

Có màn hình đăng nhập chuyên nghiệp.

Tích hợp sẵn 2 tài khoản mặc định:

Quản trị viên: Tên đăng nhập admin | Mật khẩu: 123456

Kỹ thuật viên: Tên đăng nhập nhanvien | Mật khẩu: 123456

Tự động lấy họ tên của người đang đăng nhập điền vào ô Người báo cáo / Người gọi khi nhập liệu, tránh phải gõ lại nhiều lần.

Xuất file Word (.docx) chuẩn 100% theo 2 mẫu ISO của Bệnh viện Quân y 175:   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Sổ Theo Dõi Báo Cáo KQ Cảnh Báo (SP.01-QTQL.SH.37): Khổ ngang A4, góc trái tiêu ngữ BỘ QUỐC PHÒNG / BỆNH VIỆN QUÂN Y 175, khung tiêu đề chuẩn Mã số: SP.01-QTQL.SH.37, Lần ban hành: 01, Ngày hiệu lực: 02/01/2024, dòng quản lý sổ: CN. Phạm Minh Nhi, cùng bảng 10 cột có kẻ khung chuẩn chỉ.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx
+ 1

Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16): Khổ ngang A4, khung mã số SP.01-QTQL.SH.16, bảng 10 cột chuẩn quy cách (NGÀY/ GIỜ, NGƯỜI GỌI, NGƯỜI NGHE, HỌ TÊN BỆNH NHÂN, KHOA, NỘI DUNG TRAO ĐỔI, YÊU CẦU, KẾT QUẢ TRAO ĐỔI, GHI CHÚ).

Bộ file cập nhật mới
File mã nguồn cập nhật: 
Biểu tượng PY
app
 PY 
Biểu tượng PY
app
 PY 

File danh sách thư viện: 
Biểu tượng TXT
requirements
 TXT 

Gói nén trọn bộ: 
Biểu tượng ZIP
lab_records_update_word_auth
 ZIP 

Các bước cập nhật lên GitHub và Render
Bước 1: Cập nhật requirements.txt trên GitHub
Do chức năng xuất Word cần thêm thư viện xử lý tài liệu, bạn cập nhật file này trước:

Mở kho traodoithongtin trên GitHub, bấm vào file requirements.txt.   
image_f09c4b.png

Bấm vào biểu tượng cây bút chì để chỉnh sửa và dán nội dung sau:

Plaintext
Flask>=3.0.0
gunicorn>=21.2.0
python-docx>=1.1.0
werkzeug>=3.0.0
Bấm nút xanh Commit changes... để lưu lại.

Bước 2: Cập nhật app.py trên GitHub
Mở file app.py trên GitHub và bấm vào biểu tượng cây bút chì để chỉnh sửa.   
image_f09c4b.png

Xóa toàn bộ nội dung cũ trong khung soạn thảo, copy toàn bộ nội dung từ file 
 dán vào.

Bấm nút xanh Commit changes... để lưu lại.

Kết quả sau khi Render tự động Deploy xong
Khi truy cập vào link web ([https://traodoithongtin.onrender.com](https://traodoithongtin.onrender.com)), hệ thống sẽ yêu cầu đăng nhập trước. Bạn đăng nhập bằng tài khoản admin và mật khẩu 123456.   
image_f08da3.png
+ 1

Phía trên bảng danh sách của cả 2 sổ sẽ có thêm nút màu xanh dương: 📄 Xuất Word (SP.01-QTQL.SH.37) và 📄 Xuất Word (SP.01-QTQL.SH.16). Bấm vào nút này sẽ tải về file .docx định dạng sẵn đẹp mắt để ký duyệt và in ấn báo cáo ngay lập tức.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

sao lại có 2 app.py vậy

Lý do bạn thấy xuất hiện hai file (hoặc tên tương tự như app.py và app_2.py) là do hệ thống tự động đánh số thứ tự khi lưu bản code mới qua từng lần cập nhật:

File đầu tiên (app.py): Là phiên bản ban đầu chưa có tính năng đăng nhập và xuất Word.   
app.py
+ 1

File thứ hai (app_2.py): Là phiên bản nâng cấp mới nhất đã tích hợp:   
app.py

Chức năng xác thực tài khoản đăng nhập/đăng xuất (User Authentication).   
app.py

Nút xuất file Word (.docx) chuẩn mẫu theo quy trình SP.01-QTQL.SH.37 và SP.01-QTQL.SH.16 của Bệnh viện Quân y 175.   
app.py

Tự động lấy tên người đăng nhập làm người báo cáo.   
app.py

Cách xử lý trên máy và GitHub
Khi đưa lên GitHub hoặc chạy trên máy, bạn chỉ giữ lại 1 file duy nhất mang tên app.py:

Bạn lấy toàn bộ nội dung trong file mới nhất ([file-tag: code-generated-file-a2b3b3a4-1375-46fd-8c35-cec1e94ce32d] hoặc app_2.py) dán đè vào file app.py trên kho GitHub traodoithongtin.   
app.py
+ 1

Không cần tạo thêm file app_2.py trên GitHub để tránh làm máy chủ Render bị nhầm lẫn file khởi chạy.

cho mình bản app.py hoàn chỉnh đi

Bản app.py hoàn chỉnh duy nhất đã sẵn sàng:
[file-tag: code-generated-file-5d070b4f-ea2b-4fa8-a8bf-efec38d17ee5]

Tóm tắt các tính năng tích hợp trong file app.py này:
Khởi tạo cơ sở dữ liệu tự động (init_db()): Được gọi sẵn ở tầng module để khi chạy bằng gunicorn trên Render không bao giờ bị lỗi no such table.

Hệ thống đăng nhập bảo mật:

Trang đăng nhập chuyên nghiệp.

Tài khoản mặc định:

Quản trị: admin | Mật khẩu: 123456

Nhân viên trực: nhanvien | Mật khẩu: 123456

Tự động lấy tên người đăng nhập gán vào ô Người báo cáo / Người gọi.

Tự động liên thông 2 sổ (Auto Sync):

Người báo cáo 
→
→ Người gọi   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Người nhận 
→
→ Người nghe   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Tên bệnh nhân 
→
→ Họ tên bệnh nhân   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Khoa 
→
→ Khoa   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Kết quả cảnh báo 
→
→ Nội dung trao đổi   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Nội dung trao đổi 
→
→ Yêu cầu   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Ghi chú 
→
→ Kết quả trao đổi   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Có nút đồng bộ thủ công từng dòng cho các bản ghi cũ.   
app_flask.py

Xuất file Word (.docx) chuẩn quy cách Bệnh viện Quân y 175:   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Khổ giấy A4 xoay ngang (Landscape).

Đầy đủ tiêu ngữ: BỘ QUỐC PHÒNG / BỆNH VIỆN QUÂN Y 175.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Bảng tiêu đề quy trình chuẩn: Mã số, Lần ban hành, Ngày hiệu lực, Người quản lý sổ.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Kẻ bảng 10 cột viền đen sắc nét, tự động căn chỉnh độ rộng cột và in đậm kết quả báo động.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Cách đưa lên GitHub:
Mở file [file-tag: code-generated-file-5d070b4f-ea2b-4fa8-a8bf-efec38d17ee5] tải về, copy toàn bộ nội dung.

Mở kho donhuhai2/traodoithongtin trên GitHub, bấm vào file app.py 
→
→ bấm biểu tượng cây bút chì.   
image_f09c4b.png

Xóa toàn bộ nội dung cũ trong khung soạn thảo, dán nội dung mới vào rồi bấm Commit changes....

Đảm bảo file requirements.txt trên kho của bạn có đủ 4 dòng thư viện:

Plaintext
Flask>=3.0.0
gunicorn>=21.2.0
python-docx>=1.1.0
werkzeug>=3.0.0
(Render sẽ tự động kéo bản mới về và triển khai lại trong vòng 1 phút).

cho mình file

Dưới đây là các file hoàn chỉnh đã được cập nhật để bạn tải trực tiếp:

File mã nguồn chính (app.py): [file-tag: code-generated-file-5d070b4f-ea2b-4fa8-a8bf-efec38d17ee5]

File danh sách thư viện (requirements.txt): [file-tag: code-generated-file-ef50d543-2371-4a74-a1a9-01f8926945d5]

Gói nén trọn bộ (lab_records_update_word_auth.zip): [file-tag: code-generated-file-11df89ee-a295-4260-a6aa-94f7a817369d]

Hướng dẫn cập nhật nhanh lên GitHub:
Mở file [file-tag: code-generated-file-5d070b4f-ea2b-4fa8-a8bf-efec38d17ee5], sao chép toàn bộ nội dung.

Mở kho traodoithongtin trên GitHub, chọn file app.py 
→
→ bấm biểu tượng cây bút chì để sửa.   
image_f09c4b.png

Xóa hết code cũ, dán nội dung mới vào và bấm Commit changes....

Kiểm tra file requirements.txt trên GitHub đảm bảo có đủ 4 dòng sau:

Plaintext
Flask>=3.0.0
gunicorn>=21.2.0
python-docx>=1.1.0
werkzeug>=3.0.0
(Sau khi commit, Render sẽ tự động nhận diện và cập nhật ứng dụng sau khoảng 1 phút).

file đâu, làm sao tải xuống

Để bạn không cần phải tải file rồi upload thủ công phức tạp, bạn có thể copy và dán trực tiếp toàn bộ code vào GitHub theo hướng dẫn dưới đây (chỉ mất đúng 1 phút):

Bước 1: Cập nhật file requirements.txt trên GitHub
Truy cập vào kho GitHub của bạn: [https://github.com/donhuhai2/traodoithongtin](https://github.com/donhuhai2/traodoithongtin).   
image_f09c4b.png

Bấm vào file requirements.txt 
→
→ bấm vào biểu tượng cây bút chì (Edit this file).

Xóa hết nội dung cũ và dán 4 dòng này vào:

Plaintext
Flask>=3.0.0
gunicorn>=21.2.0
python-docx>=1.1.0
werkzeug>=3.0.0
Bấm nút xanh Commit changes... ở góc trên bên phải để lưu.

Bước 2: Cập nhật file app.py trên GitHub
Quay lại trang chủ kho GitHub, bấm vào file app.py.   
image_f09c4b.png

Bấm vào biểu tượng cây bút chì (Edit this file).

Chọn tất cả (Ctrl + A) xóa sạch code cũ, sau đó copy toàn bộ khối code bên dưới và dán vào:

Python
import sqlite3
import csv
import io
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template_string, request, redirect, url_for, Response, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

app = Flask(__name__)
app.secret_key = "lab_records_secret_bvqy175_auth_key"
DB_NAME = "lab_records.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT DEFAULT 'staff'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS canh_bao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ngay_gio TEXT,
                khoa TEXT,
                nguoi_bao_cao TEXT,
                nguoi_nhan TEXT,
                ten_benh_nhan TEXT,
                ma_benh_nhan TEXT,
                noi_dung TEXT,
                ket_qua TEXT,
                ghi_chu TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trao_doi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ngay_gio TEXT,
                nguoi_goi TEXT,
                nguoi_nghe TEXT,
                ten_benh_nhan TEXT,
                khoa TEXT,
                noi_dung TEXT,
                yeu_cau TEXT,
                ket_qua TEXT,
                ghi_chu TEXT
            )
        """)
        
        user = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
        if not user:
            default_pwd = generate_password_hash("123456")
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         ("admin", default_pwd, "Quản trị viên PXN", "admin"))
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         ("nhanvien", default_pwd, "Kỹ thuật viên Trực", "staff"))

# Khởi tạo bảng ngay khi load module cho gunicorn trên Render
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bc, nguoi_nhan, ten_bn, khoa, ket_qua_cb, noi_dung_cb, ghi_chu_cb):
    conn.execute("""
        INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ngay_gio,
        nguoi_bc,
        nguoi_nhan,
        ten_bn,
        khoa,
        ket_qua_cb,
        noi_dung_cb,
        ghi_chu_cb,
        "Đồng bộ từ Sổ Cảnh Báo"
    ))

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng nhập - Sổ Điện Tử BVQY 175</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #0d6efd 0%, #002b66 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Segoe UI', Tahoma, sans-serif; }
        .card-login { max-width: 420px; width: 100%; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); border: none; }
    </style>
</head>
<body>
<div class="card card-login p-4 bg-white">
    <div class="text-center mb-4">
        <h4 class="fw-bold text-primary mb-1"><i class="bi bi-hospital me-2"></i>BVQY 175</h4>
        <div class="text-uppercase small fw-bold text-muted">Hệ Thống Quản Lý Sổ Xét Nghiệm</div>
        <div class="badge bg-light text-dark border mt-2">ISO 15189 / QLCL</div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show py-2 small" role="alert">
            {{ message }}
            <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <form method="POST" action="/login">
        <div class="mb-3">
            <label class="form-label small fw-bold">Tên đăng nhập</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-person"></i></span>
                <input type="text" name="username" class="form-control" placeholder="admin hoặc nhanvien" required autofocus>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label small fw-bold">Mật khẩu</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                <input type="password" name="password" class="form-control" placeholder="••••••••" required>
            </div>
        </div>
        <button type="submit" class="btn btn-primary w-100 fw-bold py-2 mb-3">Đăng Nhập <i class="bi bi-box-arrow-in-right ms-1"></i></button>
    </form>
    
    <div class="alert alert-info py-2 small mb-0">
        <strong>Tài khoản mặc định:</strong><br>
        • Quản trị: <code>admin</code> / MK: <code>123456</code><br>
        • Nhân viên: <code>nhanvien</code> / MK: <code>123456</code>
    </div>
</div>
</body>
</html>
"""

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Sổ Điện Tử XN - BVQY 175</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .nav-tabs .nav-link { font-weight: 600; font-size: 1.05rem; }
        .nav-tabs .nav-link.active { color: #0d6efd; border-bottom: 3px solid #0d6efd; }
        .card { border-radius: 10px; border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
        .table-responsive { max-height: 540px; overflow-y: auto; }
        .table thead th { position: sticky; top: 0; background-color: #e9ecef; z-index: 1; }
    </style>
</head>
<body class="py-3">
<div class="container-fluid px-4">
    <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
        <div>
            <h4 class="text-primary fw-bold mb-1">🏥 HỆ THỐNG QUẢN LÝ SỔ ĐIỆN TỬ PHÒNG XÉT NGHIỆM</h4>
            <span class="text-muted small">Bệnh viện Quân y 175 — Chuẩn quản lý chất lượng ISO 15189</span>
        </div>
        <div class="d-flex align-items-center gap-3">
            <div class="text-end">
                <span class="fw-bold d-block">{{ session.get('full_name') }}</span>
                <span class="badge bg-secondary small">Quyền: {{ session.get('role') }}</span>
            </div>
            <a href="/logout" class="btn btn-outline-danger btn-sm fw-bold"><i class="bi bi-box-arrow-right me-1"></i>Đăng xuất</a>
        </div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show py-2" role="alert">
            {{ message }}
            <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <ul class="nav nav-tabs mb-3" id="labTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="tab-cb-btn" data-bs-toggle="tab" data-bs-target="#tab-cb" type="button">
                🚨 Sổ Báo Cáo KQ Cảnh Báo (SP.01-QTQL.SH.37)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-td-btn" data-bs-toggle="tab" data-bs-target="#tab-td" type="button">
                📞 Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16)
            </button>
        </li>
    </ul>

    <div class="tab-content" id="labTabsContent">
        <!-- TAB 1: CẢNH BÁO -->
        <div class="tab-pane fade show active" id="tab-cb" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-danger mb-3">➕ Thêm Báo Cáo Kết Quả Cảnh Báo</h6>
                        <form method="POST" action="/add_canh_bao">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ báo cáo</label>
                                    <input type="text" name="ngay_gio" class="form-control form-control-sm" value="{{ now_str }}" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: HSCC" required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người báo cáo</label>
                                    <input type="text" name="nguoi_bao_cao" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nhận</label>
                                    <input type="text" name="nguoi_nhan" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Tên bệnh nhân</label>
                                    <input type="text" name="ten_benh_nhan" class="form-control form-control-sm" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Mã số BN (PID)</label>
                                    <input type="text" name="ma_benh_nhan" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Kết quả báo cáo (Giá trị báo động)</label>
                                <input type="text" name="ket_qua" class="form-control form-control-sm text-danger fw-bold" placeholder="VD: K+ 7.2 mmol/L..." required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Nội dung trao đổi</label>
                                <textarea name="noi_dung" class="form-control form-control-sm" rows="2" placeholder="Nội dung cụ thể cần trao đổi / xử lý lâm sàng..."></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm" placeholder="Phản hồi từ khoa lâm sàng / xác nhận...">
                            </div>

                            <div class="form-check form-switch mb-3 p-2 bg-light rounded border">
                                <input class="form-check-input ms-0 me-2" type="checkbox" name="auto_sync" id="autoSyncCheck" checked>
                                <label class="form-check-label small fw-bold text-primary" for="autoSyncCheck">
                                    ⚡ Tự động đồng bộ sang Sổ trao đổi thông tin
                                </label>
                            </div>

                            <button type="submit" class="btn btn-danger w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Bản Ghi Cảnh Báo</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Danh Sách Kết Quả Cảnh Báo ({{ canh_bao_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2">
                                <a href="/export_word/canh_bao" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word (SP.01-QTQL.SH.37)</a>
                                <a href="/export/canh_bao" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Ngày/giờ</th>
                                        <th>Khoa</th>
                                        <th>Người BC</th>
                                        <th>Người nhận</th>
                                        <th>Bệnh nhân</th>
                                        <th>Mã BN</th>
                                        <th>Kết quả</th>
                                        <th>Nội dung</th>
                                        <th>Ghi chú</th>
                                        <th class="text-center">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in canh_bao_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.ngay_gio }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td>{{ row.nguoi_bao_cao }}</td>
                                        <td>{{ row.nguoi_nhan }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td>{{ row.ma_benh_nhan }}</td>
                                        <td class="text-danger fw-bold">{{ row.ket_qua }}</td>
                                        <td>{{ row.noi_dung }}</td>
                                        <td>{{ row.ghi_chu }}</td>
                                        <td class="text-center text-nowrap">
                                            <a href="/sync_one/{{ row.id }}" class="btn btn-sm btn-outline-primary py-0 px-2" title="Đồng bộ sang Sổ trao đổi">
                                                <i class="bi bi-arrow-repeat"></i> Đồng bộ
                                            </a>
                                        </td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="11" class="text-center text-muted py-3">Chưa có bản ghi nào.</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: TRAO ĐỔI THÔNG TIN -->
        <div class="tab-pane fade" id="tab-td" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-primary mb-3">➕ Thêm Nhật Ký Trao Đổi Thủ Công</h6>
                        <form method="POST" action="/add_trao_doi">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ</label>
                                    <input type="text" name="ngay_gio" class="form-control form-control-sm" value="{{ now_str }}" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: Ngoại..." required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người gọi</label>
                                    <input type="text" name="nguoi_goi" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nghe</label>
                                    <input type="text" name="nguoi_nghe" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Họ tên bệnh nhân</label>
                                <input type="text" name="ten_benh_nhan" class="form-control form-control-sm">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Nội dung trao đổi</label>
                                <textarea name="noi_dung" class="form-control form-control-sm" rows="2" required></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Yêu cầu</label>
                                <input type="text" name="yeu_cau" class="form-control form-control-sm" placeholder="VD: Lấy lại mẫu, bổ sung thông tin...">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Kết quả trao đổi</label>
                                <input type="text" name="ket_qua" class="form-control form-control-sm" placeholder="VD: Đã đồng ý gửi lại...">
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Cuộc Trao Đổi</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Nhật Ký Trao Đổi Thông Tin ({{ trao_doi_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2">
                                <a href="/export_word/trao_doi" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word (SP.01-QTQL.SH.16)</a>
                                <a href="/export/trao_doi" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Ngày/giờ</th>
                                        <th>Người gọi</th>
                                        <th>Người nghe</th>
                                        <th>Bệnh nhân</th>
                                        <th>Khoa</th>
                                        <th>Nội dung trao đổi</th>
                                        <th>Yêu cầu</th>
                                        <th>Kết quả trao đổi</th>
                                        <th>Ghi chú</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in trao_doi_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.ngay_gio }}</td>
                                        <td>{{ row.nguoi_goi }}</td>
                                        <td>{{ row.nguoi_nghe }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td class="text-danger fw-bold">{{ row.noi_dung }}</td>
                                        <td>{{ row.yeu_cau }}</td>
                                        <td>{{ row.ket_qua }}</td>
                                        <td>{{ row.ghi_chu }}</td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="10" class="text-center text-muted py-3">Chưa có bản ghi nào.</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
    if (window.location.hash === '#tab-td') {
        const tabTrigger = new bootstrap.Tab(document.querySelector('#tab-td-btn'));
        tabTrigger.show();
    }
</script>
</body>
</html>
"""

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(r'''<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders>''')
    tblPr.append(borders_xml)

def generate_word_canh_bao(rows):
    doc = docx.Document()
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    p_header.paragraph_format.line_spacing = 1.0
    r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.name = "Times New Roman"

    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    
    cell_left = tbl_top.cell(0, 0)
    cell_left.width = Inches(7.0)
    p_title = cell_left.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("SỔ\nTHEO DÕI BÁO CÁO KẾT QUẢ CẢNH BÁO\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.name = "Times New Roman"
    r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: CN. Phạm Minh Nhi")
    r_t2.font.size = Pt(11)
    r_t2.italic = True
    r_t2.font.name = "Times New Roman"

    cell_right = tbl_top.cell(0, 1)
    cell_right.width = Inches(3.6)
    p_code = cell_right.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.37\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
    r_code.font.size = Pt(10)
    r_code.font.name = "Times New Roman"

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    headers = ["STT", "Ngày/giờ\nbáo cáo", "Khoa", "Người\nbáo cáo", "Người nhận\nbáo cáo", "Tên bệnh nhân", "Mã số\nbệnh nhân", "Nội dung\ntrao đổi", "Kết quả\nbáo cáo", "Ghi chú"]
    col_widths = [Inches(0.5), Inches(1.1), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.3), Inches(1.0), Inches(1.6), Inches(1.2), Inches(0.9)]
    
    tbl = doc.add_table(rows=len(rows) + 1, cols=10)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(title.replace("\\n", "\n"))
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Times New Roman"
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    for idx, r in enumerate(rows):
        row_cells = tbl.rows[idx + 1].cells
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["khoa"] or "",
            r["nguoi_bao_cao"] or "",
            r["nguoi_nhan"] or "",
            r["ten_benh_nhan"] or "",
            r["ma_benh_nhan"] or "",
            r["noi_dung"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 2, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            if c_idx == 8:
                run.bold = True
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def generate_word_trao_doi(rows):
    doc = docx.Document()
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    p_header.paragraph_format.line_spacing = 1.0
    r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.name = "Times New Roman"

    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    
    cell_left = tbl_top.cell(0, 0)
    cell_left.width = Inches(7.0)
    p_title = cell_left.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("SỔ TRAO ĐỔI THÔNG TIN\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.name = "Times New Roman"
    r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: …………………………………")
    r_t2.font.size = Pt(11)
    r_t2.italic = True
    r_t2.font.name = "Times New Roman"

    cell_right = tbl_top.cell(0, 1)
    cell_right.width = Inches(3.6)
    p_code = cell_right.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.16\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
    r_code.font.size = Pt(10)
    r_code.font.name = "Times New Roman"

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    headers = ["STT", "NGÀY/ GIỜ", "NGƯỜI GỌI", "NGƯỜI NGHE", "HỌ TÊN BỆNH NHÂN", "KHOA", "NỘI DUNG TRAO ĐỔI", "YÊU CẦU", "KẾT QUẢ TRAO ĐỔI", "GHI CHÚ"]
    col_widths = [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.4), Inches(0.9), Inches(1.6), Inches(1.3), Inches(1.2), Inches(0.5)]
    
    tbl = doc.add_table(rows=len(rows) + 1, cols=10)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Times New Roman"
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    for idx, r in enumerate(rows):
        row_cells = tbl.rows[idx + 1].cells
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["nguoi_goi"] or "",
            r["nguoi_nghe"] or "",
            r["ten_benh_nhan"] or "",
            r["khoa"] or "",
            r["noi_dung"] or "",
            r["yeu_cau"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["full_name"] = user["full_name"]
                session["role"] = user["role"]
                flash(f"Xin chào {user['full_name']}!", "success")
                return redirect(url_for("index"))
            else:
                flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất an toàn.", "info")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao ORDER BY id DESC").fetchall()
        td = conn.execute("SELECT * FROM trao_doi ORDER BY id DESC").fetchall()
    return render_template_string(MAIN_TEMPLATE, now_str=now_str, canh_bao_list=cb, trao_doi_list=td)

@app.route("/add_canh_bao", methods=["POST"])
@login_required
def add_canh_bao():
    ngay_gio = request.form.get("ngay_gio")
    khoa = request.form.get("khoa")
    nguoi_bao_cao = request.form.get("nguoi_bao_cao")
    nguoi_nhan = request.form.get("nguoi_nhan")
    ten_benh_nhan = request.form.get("ten_benh_nhan")
    ma_benh_nhan = request.form.get("ma_benh_nhan")
    noi_dung = request.form.get("noi_dung")
    ket_qua = request.form.get("ket_qua")
    ghi_chu = request.form.get("ghi_chu")
    auto_sync = request.form.get("auto_sync")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO canh_bao (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu))

        if auto_sync:
            sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, khoa, ket_qua, noi_dung, ghi_chu)
            flash("✅ Đã lưu vào Sổ Cảnh Báo VÀ tự động đồng bộ sang Sổ Trao Đổi Thông Tin!", "success")
        else:
            flash("✅ Đã lưu vào Sổ Cảnh Báo thành công!", "success")

    return redirect(url_for("index"))

@app.route("/sync_one/<int:cb_id>")
@login_required
def sync_one(cb_id):
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao WHERE id = ?", (cb_id,)).fetchone()
        if cb:
            sync_canh_bao_to_trao_doi(
                conn,
                cb["ngay_gio"],
                cb["nguoi_bao_cao"],
                cb["nguoi_nhan"],
                cb["ten_benh_nhan"],
                cb["khoa"],
                cb["ket_qua"],
                cb["noi_dung"],
                cb["ghi_chu"]
            )
            flash(f"✅ Đã đồng bộ bản ghi BN {cb['ten_benh_nhan']} sang Sổ Trao Đổi!", "info")
    return redirect(url_for("index") + "#tab-td")

@app.route("/add_trao_doi", methods=["POST"])
@login_required
def add_trao_doi():
    with get_db() as conn:
        conn.execute("""
            INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form.get("ngay_gio"),
            request.form.get("nguoi_goi"),
            request.form.get("nguoi_nghe"),
            request.form.get("ten_benh_nhan"),
            request.form.get("khoa"),
            request.form.get("noi_dung"),
            request.form.get("yeu_cau"),
            request.form.get("ket_qua"),
            request.form.get("ghi_chu")
        ))
        flash("✅ Đã lưu cuộc trao đổi thông tin thành công!", "success")
    return redirect(url_for("index") + "#tab-td")

@app.route("/export_word/<book_type>")
@login_required
def export_word(book_type):
    with get_db() as conn:
        if book_type == "canh_bao":
            rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            buf = generate_word_canh_bao(rows)
            filename = f"SP.01-QTQL.SH.37-So_theo_doi_bao_cao_KQ_canh_bao_{datetime.now().strftime('%Y%m%d')}.docx"
        else:
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            buf = generate_word_trao_doi(rows)
            filename = f"SP.01-QTQL.SH.16-So_trao_doi_thong_tin_{datetime.now().strftime('%Y%m%d')}.docx"

    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.route("/export/<book_type>")
@login_required
def export_csv(book_type):
    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    with get_db() as conn:
        if book_type == "canh_bao":
            writer.writerow(["STT", "Ngày/Giờ", "Khoa", "Người báo cáo", "Người nhận", "Tên bệnh nhân", "Mã số BN", "Nội dung trao đổi", "Kết quả báo cáo", "Ghi chú"])
            rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["khoa"], r["nguoi_bao_cao"], r["nguoi_nhan"], r["ten_benh_nhan"], r["ma_benh_nhan"], r["noi_dung"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Canh_Bao_SP01_QTQL_SH_37_{datetime.now().strftime('%Y%m%d')}.csv"
        else:
            writer.writerow(["STT", "Ngày/Giờ", "Người gọi", "Người nghe", "Tên bệnh nhân", "Khoa", "Nội dung trao đổi", "Yêu cầu", "Kết quả trao đổi", "Ghi chú"])
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["nguoi_goi"], r["nguoi_nghe"], r["ten_benh_nhan"], r["khoa"], r["noi_dung"], r["yeu_cau"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Trao_Doi_SP01_QTQL_SH_16_{datetime.now().strftime('%Y%m%d')}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    init_db()
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
Kéo lên góc trên bên phải, bấm nút xanh Commit changes... 
→
→ Bấm tiếp Commit changes để lưu.

Sau khi lưu:
Render sẽ tự động phát hiện code mới và triển khai lại ứng dụng[cite: 21, 27].

Sau khoảng 1 phút, bạn mở link [https://traodoithongtin.onrender.com](https://traodoithongtin.onrender.com) và đăng nhập bằng tài khoản:

Tên đăng nhập: admin

Mật khẩu: 123456

Nút tải file Word mẫu chuẩn sẽ hiển thị ngay trên bảng để bạn xuất tài liệu trực tiếp.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx
+ 1

bổ sung thêm mục quản lý mật khẩu các thành viên, tạo tài khoản cho thành viên mới và nút đổi mật khẩu cho mỗi tài khoản

Toàn bộ các tính năng quản lý tài khoản, mật khẩu và xuất mẫu Word theo yêu cầu đã được tích hợp đầy đủ.

Tải về bản cập nhật:

Biểu tượng PY
app
 PY 
Biểu tượng PY
app
 PY 

(Hoặc tải trọn bộ file nén kèm hướng dẫn: 
Biểu tượng ZIP
lab_records_v3_full
 ZIP 
)

Các tính năng mới được bổ sung trong bản này:
Tab "Quản Lý Thành Viên & Mật Khẩu":

Tạo tài khoản mới: Form tạo tài khoản cho nhân viên/kỹ thuật viên mới trong khoa (nhập họ tên, username, mật khẩu ban đầu và phân quyền: Kỹ thuật viên hoặc Quản trị viên).

Danh sách thành viên: Hiển thị bảng toàn bộ tài khoản trong hệ thống.

Nút đổi/reset mật khẩu cho từng tài khoản: Quản trị viên (admin) có nút bấm 🔑 Đổi MK ngay cạnh mỗi tài khoản để đặt lại mật khẩu khi có người quên mật khẩu.

Xóa tài khoản: Quản trị viên có thể xóa các tài khoản nhân viên cũ khi chuyển công tác (bảo vệ tài khoản admin gốc không bị xóa nhầm).

Nút "Đổi mật khẩu" cá nhân:

Nằm ngay góc trên bên phải thanh tiêu đề (cạnh tên người đang đăng nhập và nút Đăng xuất).

Bất kỳ thành viên nào (dù là Kỹ thuật viên hay Quản trị viên) đều có thể tự đổi mật khẩu cá nhân của mình bất kỳ lúc nào bằng cách xác nhận mật khẩu hiện tại.

Giữ nguyên vẹn các tính năng chuẩn trước đó:

Sổ Cảnh Báo (SP.01-QTQL.SH.37) và Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16).   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Tự động liên thông dữ liệu giữa 2 sổ (Auto Sync).

Nút xuất file Word (.docx) chuẩn mẫu biểu in ấn của Bệnh viện Quân y 175.   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx

Hướng dẫn cập nhật lên GitHub và Render:
Mở file 
 vừa tải về, copy toàn bộ nội dung bên trong.

Mở kho traodoithongtin trên GitHub, bấm vào file app.py 
→
→ chọn biểu tượng cây bút chì để sửa.   
image_f09c4b.png

Xóa hết code cũ, dán toàn bộ nội dung mới vào rồi bấm nút xanh Commit changes....

Render sẽ tự động phát hiện code mới và cập nhật trong khoảng 1 phút. Sau đó bạn tải lại trang web [https://traodoithongtin.onrender.com](https://traodoithongtin.onrender.com) để sử dụng ngay.   
image_f08da3.png
+ 1

cho bản app hoàn chỉnh đi

Toàn bộ mã nguồn hoàn chỉnh của file app.py bao gồm đầy đủ tính năng: đăng nhập/đăng xuất, đổi mật khẩu cá nhân, quản trị viên tạo/reset mật khẩu thành viên, tự động đồng bộ giữa hai sổ và xuất file Word .docx chuẩn mẫu ISO của Bệnh viện Quân y 175:   
SP.01-QTQL.SH.37-Sổ theo dõi báo cáo kết quả cảnh báo - Copy - Copy.docx
+ 1

Python
import sqlite3
import csv
import io
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template_string, request, redirect, url_for, Response, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

app = Flask(__name__)
app.secret_key = "lab_records_secret_bvqy175_auth_key_v3"
DB_NAME = "lab_records.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT DEFAULT 'staff'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS canh_bao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ngay_gio TEXT,
                khoa TEXT,
                nguoi_bao_cao TEXT,
                nguoi_nhan TEXT,
                ten_benh_nhan TEXT,
                ma_benh_nhan TEXT,
                noi_dung TEXT,
                ket_qua TEXT,
                ghi_chu TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trao_doi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ngay_gio TEXT,
                nguoi_goi TEXT,
                nguoi_nghe TEXT,
                ten_benh_nhan TEXT,
                khoa TEXT,
                noi_dung TEXT,
                yeu_cau TEXT,
                ket_qua TEXT,
                ghi_chu TEXT
            )
        """)
        
        user = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
        if not user:
            default_pwd = generate_password_hash("123456")
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         ("admin", default_pwd, "Quản trị viên PXN", "admin"))
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         ("nhanvien", default_pwd, "Kỹ thuật viên Trực", "staff"))

init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Chỉ quản trị viên mới có quyền thực hiện thao tác này!", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bc, nguoi_nhan, ten_bn, khoa, ket_qua_cb, noi_dung_cb, ghi_chu_cb):
    conn.execute("""
        INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ngay_gio,
        nguoi_bc,
        nguoi_nhan,
        ten_bn,
        khoa,
        ket_qua_cb,
        noi_dung_cb,
        ghi_chu_cb,
        "Đồng bộ từ Sổ Cảnh Báo"
    ))

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng nhập - Sổ Điện Tử BVQY 175</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #0d6efd 0%, #002b66 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Segoe UI', Tahoma, sans-serif; }
        .card-login { max-width: 420px; width: 100%; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); border: none; }
    </style>
</head>
<body>
<div class="card card-login p-4 bg-white">
    <div class="text-center mb-4">
        <h4 class="fw-bold text-primary mb-1"><i class="bi bi-hospital me-2"></i>BVQY 175</h4>
        <div class="text-uppercase small fw-bold text-muted">Hệ Thống Quản Lý Sổ Xét Nghiệm</div>
        <div class="badge bg-light text-dark border mt-2">ISO 15189 / QLCL</div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show py-2 small" role="alert">
            {{ message }}
            <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <form method="POST" action="/login">
        <div class="mb-3">
            <label class="form-label small fw-bold">Tên đăng nhập</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-person"></i></span>
                <input type="text" name="username" class="form-control" placeholder="admin hoặc nhanvien" required autofocus>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label small fw-bold">Mật khẩu</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                <input type="password" name="password" class="form-control" placeholder="••••••••" required>
            </div>
        </div>
        <button type="submit" class="btn btn-primary w-100 fw-bold py-2 mb-3">Đăng Nhập <i class="bi bi-box-arrow-in-right ms-1"></i></button>
    </form>
    
    <div class="alert alert-info py-2 small mb-0">
        <strong>Tài khoản mặc định:</strong><br>
        • Quản trị: <code>admin</code> / MK: <code>123456</code><br>
        • Nhân viên: <code>nhanvien</code> / MK: <code>123456</code>
    </div>
</div>
</body>
</html>
"""

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Sổ Điện Tử XN - BVQY 175</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .nav-tabs .nav-link { font-weight: 600; font-size: 1.02rem; }
        .nav-tabs .nav-link.active { color: #0d6efd; border-bottom: 3px solid #0d6efd; }
        .card { border-radius: 10px; border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
        .table-responsive { max-height: 540px; overflow-y: auto; }
        .table thead th { position: sticky; top: 0; background-color: #e9ecef; z-index: 1; }
    </style>
</head>
<body class="py-3">
<div class="container-fluid px-4">
    <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom flex-wrap gap-2">
        <div>
            <h4 class="text-primary fw-bold mb-1">🏥 HỆ THỐNG QUẢN LÝ SỔ ĐIỆN TỬ PHÒNG XÉT NGHIỆM</h4>
            <span class="text-muted small">Bệnh viện Quân y 175 — Chuẩn quản lý chất lượng ISO 15189</span>
        </div>
        <div class="d-flex align-items-center gap-2">
            <div class="text-end me-2">
                <span class="fw-bold d-block">{{ session.get('full_name') }}</span>
                <span class="badge bg-secondary small">Quyền: {{ session.get('role') }}</span>
            </div>
            <button class="btn btn-outline-primary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#changePassModal">
                <i class="bi bi-key me-1"></i>Đổi mật khẩu
            </button>
            <a href="/logout" class="btn btn-outline-danger btn-sm fw-bold"><i class="bi bi-box-arrow-right me-1"></i>Đăng xuất</a>
        </div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show py-2" role="alert">
            {{ message }}
            <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <ul class="nav nav-tabs mb-3" id="labTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="tab-cb-btn" data-bs-toggle="tab" data-bs-target="#tab-cb" type="button">
                🚨 Sổ Báo Cáo KQ Cảnh Báo (SP.01-QTQL.SH.37)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-td-btn" data-bs-toggle="tab" data-bs-target="#tab-td" type="button">
                📞 Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-users-btn" data-bs-toggle="tab" data-bs-target="#tab-users" type="button">
                👥 Quản Lý Thành Viên & Mật Khẩu
            </button>
        </li>
    </ul>

    <div class="tab-content" id="labTabsContent">
        <!-- TAB 1: CẢNH BÁO -->
        <div class="tab-pane fade show active" id="tab-cb" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-danger mb-3">➕ Thêm Báo Cáo Kết Quả Cảnh Báo</h6>
                        <form method="POST" action="/add_canh_bao">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ báo cáo</label>
                                    <input type="text" name="ngay_gio" class="form-control form-control-sm" value="{{ now_str }}" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: HSCC" required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người báo cáo</label>
                                    <input type="text" name="nguoi_bao_cao" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nhận</label>
                                    <input type="text" name="nguoi_nhan" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Tên bệnh nhân</label>
                                    <input type="text" name="ten_benh_nhan" class="form-control form-control-sm" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Mã số BN (PID)</label>
                                    <input type="text" name="ma_benh_nhan" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Kết quả báo cáo (Giá trị báo động)</label>
                                <input type="text" name="ket_qua" class="form-control form-control-sm text-danger fw-bold" placeholder="VD: K+ 7.2 mmol/L..." required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Nội dung trao đổi</label>
                                <textarea name="noi_dung" class="form-control form-control-sm" rows="2" placeholder="Nội dung cụ thể cần trao đổi / xử lý lâm sàng..."></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm" placeholder="Phản hồi từ khoa lâm sàng / xác nhận...">
                            </div>

                            <div class="form-check form-switch mb-3 p-2 bg-light rounded border">
                                <input class="form-check-input ms-0 me-2" type="checkbox" name="auto_sync" id="autoSyncCheck" checked>
                                <label class="form-check-label small fw-bold text-primary" for="autoSyncCheck">
                                    ⚡ Tự động đồng bộ sang Sổ trao đổi thông tin
                                </label>
                            </div>

                            <button type="submit" class="btn btn-danger w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Bản Ghi Cảnh Báo</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Danh Sách Kết Quả Cảnh Báo ({{ canh_bao_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2">
                                <a href="/export_word/canh_bao" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word (SP.01-QTQL.SH.37)</a>
                                <a href="/export/canh_bao" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Ngày/giờ</th>
                                        <th>Khoa</th>
                                        <th>Người BC</th>
                                        <th>Người nhận</th>
                                        <th>Bệnh nhân</th>
                                        <th>Mã BN</th>
                                        <th>Kết quả</th>
                                        <th>Nội dung</th>
                                        <th>Ghi chú</th>
                                        <th class="text-center">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in canh_bao_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.ngay_gio }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td>{{ row.nguoi_bao_cao }}</td>
                                        <td>{{ row.nguoi_nhan }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td>{{ row.ma_benh_nhan }}</td>
                                        <td class="text-danger fw-bold">{{ row.ket_qua }}</td>
                                        <td>{{ row.noi_dung }}</td>
                                        <td>{{ row.ghi_chu }}</td>
                                        <td class="text-center text-nowrap">
                                            <a href="/sync_one/{{ row.id }}" class="btn btn-sm btn-outline-primary py-0 px-2" title="Đồng bộ sang Sổ trao đổi">
                                                <i class="bi bi-arrow-repeat"></i> Đồng bộ
                                            </a>
                                        </td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="11" class="text-center text-muted py-3">Chưa có bản ghi nào.</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: TRAO ĐỔI THÔNG TIN -->
        <div class="tab-pane fade" id="tab-td" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-primary mb-3">➕ Thêm Nhật Ký Trao Đổi Thủ Công</h6>
                        <form method="POST" action="/add_trao_doi">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ</label>
                                    <input type="text" name="ngay_gio" class="form-control form-control-sm" value="{{ now_str }}" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: Ngoại..." required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người gọi</label>
                                    <input type="text" name="nguoi_goi" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nghe</label>
                                    <input type="text" name="nguoi_nghe" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Họ tên bệnh nhân</label>
                                <input type="text" name="ten_benh_nhan" class="form-control form-control-sm">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Nội dung trao đổi</label>
                                <textarea name="noi_dung" class="form-control form-control-sm" rows="2" required></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Yêu cầu</label>
                                <input type="text" name="yeu_cau" class="form-control form-control-sm" placeholder="VD: Lấy lại mẫu, bổ sung thông tin...">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Kết quả trao đổi</label>
                                <input type="text" name="ket_qua" class="form-control form-control-sm" placeholder="VD: Đã đồng ý gửi lại...">
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Cuộc Trao Đổi</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Nhật Ký Trao Đổi Thông Tin ({{ trao_doi_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2">
                                <a href="/export_word/trao_doi" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word (SP.01-QTQL.SH.16)</a>
                                <a href="/export/trao_doi" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Ngày/giờ</th>
                                        <th>Người gọi</th>
                                        <th>Người nghe</th>
                                        <th>Bệnh nhân</th>
                                        <th>Khoa</th>
                                        <th>Nội dung trao đổi</th>
                                        <th>Yêu cầu</th>
                                        <th>Kết quả trao đổi</th>
                                        <th>Ghi chú</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in trao_doi_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.ngay_gio }}</td>
                                        <td>{{ row.nguoi_goi }}</td>
                                        <td>{{ row.nguoi_nghe }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td class="text-danger fw-bold">{{ row.noi_dung }}</td>
                                        <td>{{ row.yeu_cau }}</td>
                                        <td>{{ row.ket_qua }}</td>
                                        <td>{{ row.ghi_chu }}</td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="10" class="text-center text-muted py-3">Chưa có bản ghi nào.</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: QUẢN LÝ THÀNH VIÊN & MẬT KHẨU -->
        <div class="tab-pane fade" id="tab-users" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-success mb-3"><i class="bi bi-person-plus-fill me-1"></i>Tạo Tài Khoản Thành Viên Mới</h6>
                        {% if session.get('role') == 'admin' %}
                        <form method="POST" action="/create_user">
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Họ và tên nhân viên</label>
                                <input type="text" name="full_name" class="form-control form-control-sm" placeholder="VD: CN. Nguyễn Văn A" required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Tên đăng nhập (username)</label>
                                <input type="text" name="username" class="form-control form-control-sm" placeholder="VD: nguyenvana (viết liền không dấu)" required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Mật khẩu khởi tạo</label>
                                <input type="password" name="password" class="form-control form-control-sm" placeholder="Tối thiểu 6 ký tự" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Vai trò / Quyền hạn</label>
                                <select name="role" class="form-select form-select-sm">
                                    <option value="staff">Kỹ thuật viên / Nhân viên (staff)</option>
                                    <option value="admin">Quản trị viên (admin)</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-success w-100 fw-bold"><i class="bi bi-check-circle me-1"></i>Tạo Tài Khoản</button>
                        </form>
                        {% else %}
                        <div class="alert alert-warning small mb-0">
                            <i class="bi bi-info-circle me-1"></i>Tính năng tạo tài khoản mới chỉ dành cho tài khoản <strong>Quản trị viên (admin)</strong>. Bạn đang đăng nhập bằng quyền nhân viên.
                        </div>
                        {% endif %}
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h6 class="fw-bold mb-0"><i class="bi bi-people-fill me-1"></i>Danh Sách Thành Viên ({{ users_list|length }} người)</h6>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Họ và tên</th>
                                        <th>Tên đăng nhập</th>
                                        <th>Vai trò</th>
                                        <th class="text-center">Quản lý mật khẩu & Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for u in users_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="fw-bold">{{ u.full_name }}</td>
                                        <td><code>{{ u.username }}</code></td>
                                        <td>
                                            {% if u.role == 'admin' %}
                                            <span class="badge bg-danger">Quản trị viên</span>
                                            {% else %}
                                            <span class="badge bg-info text-dark">Kỹ thuật viên</span>
                                            {% endif %}
                                        </td>
                                        <td class="text-center text-nowrap">
                                            {% if session.get('role') == 'admin' or session.get('username') == u.username %}
                                            <button class="btn btn-sm btn-outline-warning py-0 px-2" data-bs-toggle="modal" data-bs-target="#adminResetModal{{ u.id }}">
                                                <i class="bi bi-key-fill"></i> Đổi MK
                                            </button>
                                            {% endif %}
                                            {% if session.get('role') == 'admin' and u.username != 'admin' and u.username != session.get('username') %}
                                            <a href="/delete_user/{{ u.id }}" class="btn btn-sm btn-outline-danger py-0 px-2 ms-1" onclick="return confirm('Bạn có chắc chắn muốn xóa tài khoản {{ u.username }} không?');">
                                                <i class="bi bi-trash"></i>
                                            </a>
                                            {% endif %}
                                        </td>
                                    </tr>

                                    <div class="modal fade" id="adminResetModal{{ u.id }}" tabindex="-1">
                                        <div class="modal-dialog modal-dialog-centered modal-sm">
                                            <div class="modal-content">
                                                <div class="modal-header py-2">
                                                    <h6 class="modal-title fw-bold">Đổi MK: {{ u.full_name }}</h6>
                                                    <button type="button" class="btn-close py-2" data-bs-dismiss="modal"></button>
                                                </div>
                                                <form method="POST" action="/reset_user_password">
                                                    <div class="modal-body py-3">
                                                        <input type="hidden" name="user_id" value="{{ u.id }}">
                                                        <div class="mb-2">
                                                            <label class="form-label small fw-bold">Mật khẩu mới</label>
                                                            <input type="password" name="new_password" class="form-control form-control-sm" placeholder="Nhập MK mới..." required>
                                                        </div>
                                                    </div>
                                                    <div class="modal-footer py-2">
                                                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                                                        <button type="submit" class="btn btn-warning btn-sm fw-bold">Cập Nhật MK</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="changePassModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-primary text-white">
                <h6 class="modal-title fw-bold"><i class="bi bi-shield-lock me-1"></i>Đổi Mật Khẩu Cá Nhân</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="/change_own_password">
                <div class="modal-body py-3">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Mật khẩu hiện tại</label>
                        <input type="password" name="current_password" class="form-control" placeholder="Nhập mật khẩu đang dùng" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Mật khẩu mới</label>
                        <input type="password" name="new_password" class="form-control" placeholder="Tối thiểu 6 ký tự" required>
                    </div>
                    <div class="mb-2">
                        <label class="form-label small fw-bold">Xác nhận mật khẩu mới</label>
                        <input type="password" name="confirm_password" class="form-control" placeholder="Nhập lại mật khẩu mới" required>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-check-lg me-1"></i>Lưu Mật Khẩu Mới</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
    if (window.location.hash === '#tab-td') {
        const tabTrigger = new bootstrap.Tab(document.querySelector('#tab-td-btn'));
        tabTrigger.show();
    } else if (window.location.hash === '#tab-users') {
        const tabTrigger = new bootstrap.Tab(document.querySelector('#tab-users-btn'));
        tabTrigger.show();
    }
</script>
</body>
</html>
"""

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(r'''<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders>''')
    tblPr.append(borders_xml)

def generate_word_canh_bao(rows):
    doc = docx.Document()
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    p_header.paragraph_format.line_spacing = 1.0
    r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.name = "Times New Roman"

    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    
    cell_left = tbl_top.cell(0, 0)
    cell_left.width = Inches(7.0)
    p_title = cell_left.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("SỔ\nTHEO DÕI BÁO CÁO KẾT QUẢ CẢNH BÁO\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.name = "Times New Roman"
    r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: CN. Phạm Minh Nhi")
    r_t2.font.size = Pt(11)
    r_t2.italic = True
    r_t2.font.name = "Times New Roman"

    cell_right = tbl_top.cell(0, 1)
    cell_right.width = Inches(3.6)
    p_code = cell_right.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.37\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
    r_code.font.size = Pt(10)
    r_code.font.name = "Times New Roman"

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    headers = ["STT", "Ngày/giờ\nbáo cáo", "Khoa", "Người\nbáo cáo", "Người nhận\nbáo cáo", "Tên bệnh nhân", "Mã số\nbệnh nhân", "Nội dung\ntrao đổi", "Kết quả\nbáo cáo", "Ghi chú"]
    col_widths = [Inches(0.5), Inches(1.1), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.3), Inches(1.0), Inches(1.6), Inches(1.2), Inches(0.9)]
    
    tbl = doc.add_table(rows=len(rows) + 1, cols=10)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(title.replace("\\n", "\n"))
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Times New Roman"
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    for idx, r in enumerate(rows):
        row_cells = tbl.rows[idx + 1].cells
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["khoa"] or "",
            r["nguoi_bao_cao"] or "",
            r["nguoi_nhan"] or "",
            r["ten_benh_nhan"] or "",
            r["ma_benh_nhan"] or "",
            r["noi_dung"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 2, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            if c_idx == 8:
                run.bold = True
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def generate_word_trao_doi(rows):
    doc = docx.Document()
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    p_header.paragraph_format.line_spacing = 1.0
    r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.name = "Times New Roman"

    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    
    cell_left = tbl_top.cell(0, 0)
    cell_left.width = Inches(7.0)
    p_title = cell_left.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("SỔ TRAO ĐỔI THÔNG TIN\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.name = "Times New Roman"
    r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: …………………………………")
    r_t2.font.size = Pt(11)
    r_t2.italic = True
    r_t2.font.name = "Times New Roman"

    cell_right = tbl_top.cell(0, 1)
    cell_right.width = Inches(3.6)
    p_code = cell_right.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.16\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
    r_code.font.size = Pt(10)
    r_code.font.name = "Times New Roman"

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    headers = ["STT", "NGÀY/ GIỜ", "NGƯỜI GỌI", "NGƯỜI NGHE", "HỌ TÊN BỆNH NHÂN", "KHOA", "NỘI DUNG TRAO ĐỔI", "YÊU CẦU", "KẾT QUẢ TRAO ĐỔI", "GHI CHÚ"]
    col_widths = [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.4), Inches(0.9), Inches(1.6), Inches(1.3), Inches(1.2), Inches(0.5)]
    
    tbl = doc.add_table(rows=len(rows) + 1, cols=10)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Times New Roman"
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    for idx, r in enumerate(rows):
        row_cells = tbl.rows[idx + 1].cells
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["nguoi_goi"] or "",
            r["nguoi_nghe"] or "",
            r["ten_benh_nhan"] or "",
            r["khoa"] or "",
            r["noi_dung"] or "",
            r["yeu_cau"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ----------------- ROUTES -----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["full_name"] = user["full_name"]
                session["role"] = user["role"]
                flash(f"Xin chào {user['full_name']}!", "success")
                return redirect(url_for("index"))
            else:
                flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất an toàn.", "info")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao ORDER BY id DESC").fetchall()
        td = conn.execute("SELECT * FROM trao_doi ORDER BY id DESC").fetchall()
        users = conn.execute("SELECT id, username, full_name, role FROM users ORDER BY id ASC").fetchall()
    return render_template_string(MAIN_TEMPLATE, now_str=now_str, canh_bao_list=cb, trao_doi_list=td, users_list=users)

@app.route("/add_canh_bao", methods=["POST"])
@login_required
def add_canh_bao():
    ngay_gio = request.form.get("ngay_gio")
    khoa = request.form.get("khoa")
    nguoi_bao_cao = request.form.get("nguoi_bao_cao")
    nguoi_nhan = request.form.get("nguoi_nhan")
    ten_benh_nhan = request.form.get("ten_benh_nhan")
    ma_benh_nhan = request.form.get("ma_benh_nhan")
    noi_dung = request.form.get("noi_dung")
    ket_qua = request.form.get("ket_qua")
    ghi_chu = request.form.get("ghi_chu")
    auto_sync = request.form.get("auto_sync")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO canh_bao (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu))

        if auto_sync:
            sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, khoa, ket_qua, noi_dung, ghi_chu)
            flash("✅ Đã lưu vào Sổ Cảnh Báo VÀ tự động đồng bộ sang Sổ Trao Đổi Thông Tin!", "success")
        else:
            flash("✅ Đã lưu vào Sổ Cảnh Báo thành công!", "success")

    return redirect(url_for("index"))

@app.route("/sync_one/<int:cb_id>")
@login_required
def sync_one(cb_id):
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao WHERE id = ?", (cb_id,)).fetchone()
        if cb:
            sync_canh_bao_to_trao_doi(
                conn,
                cb["ngay_gio"],
                cb["nguoi_bao_cao"],
                cb["nguoi_nhan"],
                cb["ten_benh_nhan"],
                cb["khoa"],
                cb["ket_qua"],
                cb["noi_dung"],
                cb["ghi_chu"]
            )
            flash(f"✅ Đã đồng bộ bản ghi BN {cb['ten_benh_nhan']} sang Sổ Trao Đổi!", "info")
    return redirect(url_for("index") + "#tab-td")

@app.route("/add_trao_doi", methods=["POST"])
@login_required
def add_trao_doi():
    with get_db() as conn:
        conn.execute("""
            INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form.get("ngay_gio"),
            request.form.get("nguoi_goi"),
            request.form.get("nguoi_nghe"),
            request.form.get("ten_benh_nhan"),
            request.form.get("khoa"),
            request.form.get("noi_dung"),
            request.form.get("yeu_cau"),
            request.form.get("ket_qua"),
            request.form.get("ghi_chu")
        ))
        flash("✅ Đã lưu cuộc trao đổi thông tin thành công!", "success")
    return redirect(url_for("index") + "#tab-td")

# ----------------- QUẢN LÝ TÀI KHOẢN & MẬT KHẨU -----------------

@app.route("/create_user", methods=["POST"])
@login_required
@admin_required
def create_user():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()
    full_name = request.form.get("full_name", "").strip()
    role = request.form.get("role", "staff")

    if not username or not password or not full_name:
        flash("Vui lòng điền đầy đủ thông tin tài khoản!", "danger")
        return redirect(url_for("index") + "#tab-users")

    if len(password) < 6:
        flash("Mật khẩu phải có tối thiểu 6 ký tự!", "danger")
        return redirect(url_for("index") + "#tab-users")

    pwd_hash = generate_password_hash(password)
    try:
        with get_db() as conn:
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         (username, pwd_hash, full_name, role))
        flash(f"✅ Đã tạo tài khoản thành công cho {full_name} ({username})!", "success")
    except sqlite3.IntegrityError:
        flash(f"Tên đăng nhập '{username}' đã tồn tại, vui lòng chọn tên khác!", "danger")

    return redirect(url_for("index") + "#tab-users")

@app.route("/change_own_password", methods=["POST"])
@login_required
def change_own_password():
    current_pwd = request.form.get("current_password", "").strip()
    new_pwd = request.form.get("new_password", "").strip()
    confirm_pwd = request.form.get("confirm_password", "").strip()

    if new_pwd != confirm_pwd:
        flash("Mật khẩu mới và xác nhận mật khẩu không trùng khớp!", "danger")
        return redirect(url_for("index"))

    if len(new_pwd) < 6:
        flash("Mật khẩu mới phải có tối thiểu 6 ký tự!", "danger")
        return redirect(url_for("index"))

    user_id = session.get("user_id")
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user or not check_password_hash(user["password_hash"], current_pwd):
            flash("Mật khẩu hiện tại không chính xác!", "danger")
            return redirect(url_for("index"))

        new_hash = generate_password_hash(new_pwd)
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        flash("✅ Đã đổi mật khẩu cá nhân thành công!", "success")

    return redirect(url_for("index"))

@app.route("/reset_user_password", methods=["POST"])
@login_required
def reset_user_password():
    target_id = request.form.get("user_id")
    new_pwd = request.form.get("new_password", "").strip()

    if session.get("role") != "admin" and str(session.get("user_id")) != str(target_id):
        flash("Bạn không có quyền đổi mật khẩu của tài khoản này!", "danger")
        return redirect(url_for("index") + "#tab-users")

    if len(new_pwd) < 6:
        flash("Mật khẩu mới phải có ít nhất 6 ký tự!", "danger")
        return redirect(url_for("index") + "#tab-users")

    new_hash = generate_password_hash(new_pwd)
    with get_db() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, target_id))
        user = conn.execute("SELECT full_name FROM users WHERE id = ?", (target_id,)).fetchone()
        name = user["full_name"] if user else "thành viên"
        flash(f"✅ Đã cập nhật mật khẩu mới cho {name}!", "success")

    return redirect(url_for("index") + "#tab-users")

@app.route("/delete_user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    if user_id == session.get("user_id"):
        flash("Bạn không thể tự xóa tài khoản của chính mình!", "danger")
        return redirect(url_for("index") + "#tab-users")

    with get_db() as conn:
        user = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
        if user and user["username"] == "admin":
            flash("Không thể xóa tài khoản admin gốc!", "danger")
            return redirect(url_for("index") + "#tab-users")

        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        flash("Đã xóa tài khoản thành viên thành công!", "info")

    return redirect(url_for("index") + "#tab-users")

# ----------------- XUẤT WORD & CSV -----------------

@app.route("/export_word/<book_type>")
@login_required
def export_word(book_type):
    with get_db() as conn:
        if book_type == "canh_bao":
            rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            buf = generate_word_canh_bao(rows)
            filename = f"SP.01-QTQL.SH.37-So_theo_doi_bao_cao_KQ_canh_bao_{datetime.now().strftime('%Y%m%d')}.docx"
        else:
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            buf = generate_word_trao_doi(rows)
            filename = f"SP.01-QTQL.SH.16-So_trao_doi_thong_tin_{datetime.now().strftime('%Y%m%d')}.docx"

    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.route("/export/<book_type>")
@login_required
def export_csv(book_type):
    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    with get_db() as conn:
        if book_type == "canh_bao":
            writer.writerow(["STT", "Ngày/Giờ", "Khoa", "Người báo cáo", "Người nhận", "Tên bệnh nhân", "Mã số BN", "Nội dung trao đổi", "Kết quả báo cáo", "Ghi chú"])
            rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["khoa"], r["nguoi_bao_cao"], r["nguoi_nhan"], r["ten_benh_nhan"], r["ma_benh_nhan"], r["noi_dung"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Canh_Bao_SP01_QTQL_SH_37_{datetime.now().strftime('%Y%m%d')}.csv"
        else:
            writer.writerow(["STT", "Ngày/Giờ", "Người gọi", "Người nghe", "Tên bệnh nhân", "Khoa", "Nội dung trao đổi", "Yêu cầu", "Kết quả trao đổi", "Ghi chú"])
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["nguoi_goi"], r["nguoi_nghe"], r["ten_benh_nhan"], r["khoa"], r["noi_dung"], r["yeu_cau"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Trao_Doi_SP01_QTQL_SH_16_{datetime.now().strftime('%Y%m%d')}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    init_db()
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
Hướng dẫn cập nhật trong 1 phút:
Mở file app.py trên GitHub: Vào kho traodoithongtin, bấm vào app.py 
→
→ bấm biểu tượng cây bút chì.   
image_f09c4b.png

Dán code mới: Nhấn Ctrl + A để chọn toàn bộ code cũ, xóa đi và dán toàn bộ đoạn mã ở trên vào.

Lưu lại: Bấm nút xanh Commit changes... ở góc trên bên phải.

Kiểm tra requirements.txt: Đảm bảo file requirements.txt trên GitHub đã có 4 dòng này:

Plaintext
Flask>=3.0.0
gunicorn>=21.2.0
python-docx>=1.1.0
werkzeug>=3.0.0
Máy chủ Render sẽ tự động triển khai lại trong khoảng 1 phút. Bạn chỉ cần vào lại trang web [https://traodoithongtin.onrender.com](https://traodoithongtin.onrender.com) và đăng nhập bằng tài khoản admin / 123456.   
image_f09fad.png
+ 4

hướng dẫn xuất ra bản word giống y đúc như thế này

Để tạo ra file Word giống mẫu Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16), cấu trúc tài liệu cần đảm bảo các thông số sau:   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Khổ giấy & Căn lề: A4 xoay ngang (Landscape: 11.69 x 8.27 inch), lề 4 phía đều là 0.5 inch (1.27 cm).

Font chữ & Kích thước: Times New Roman toàn bộ.

Tiêu ngữ cơ quan: 11pt in đậm.

Tên sổ: 14pt in đậm, căn giữa.

Từ ngày / Người quản lý sổ: 11pt in nghiêng.

Khung mã số ISO: 10pt.

Bảng tiêu đề: Chia làm 2 cột không viền (Cột trái 7.0 inch, Cột phải 3.6 inch).

Bảng nội dung: Kẻ viền đen toàn bộ, chia 10 cột theo tỉ lệ chuẩn với tiêu đề in đậm 9.5pt căn giữa.   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Đoạn code Python tạo chuẩn xác mẫu Word
Nếu đang dùng Python (thư viện python-docx), đoạn code hoàn chỉnh sau sẽ tạo file Word theo đúng định dạng:

Python
import io
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Thiết lập padding trong ô để chữ không dính sát viền"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    """Kẻ viền đen chuẩn cho bảng dữ liệu"""
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(r'''<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders>''')
    tblPr.append(borders_xml)

def generate_word_trao_doi(data_rows, output_path="SP.01-QTQL.SH.16-So_trao_doi_thong_tin.docx"):
    doc = docx.Document()
    section = doc.sections[0]
    
    # 1. Khổ giấy ngang A4 & Lề 0.5 inch
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    # 2. Tiêu ngữ cơ quan
    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    p_header.paragraph_format.line_spacing = 1.0
    r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.name = "Times New Roman"

    # 3. Bảng phần đầu sổ (Tiêu đề + Mã quy trình ISO)
    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    
    # Cột trái: Tên sổ và ngày tháng
    cell_left = tbl_top.cell(0, 0)
    cell_left.width = Inches(7.0)
    p_title = cell_left.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("SỔ TRAO ĐỔI THÔNG TIN\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.name = "Times New Roman"
    r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: …………………………………")
    r_t2.font.size = Pt(11)
    r_t2.italic = True
    r_t2.font.name = "Times New Roman"

    # Cột phải: Mã số quy trình
    cell_right = tbl_top.cell(0, 1)
    cell_right.width = Inches(3.6)
    p_code = cell_right.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.16\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
    r_code.font.size = Pt(10)
    r_code.font.name = "Times New Roman"

    # Khoảng cách trước bảng
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 4. Bảng danh sách 10 cột
    headers = [
        "STT", "NGÀY/ GIỜ", "NGƯỜI GỌI", "NGƯỜI NGHE", 
        "HỌ TÊN BỆNH NHÂN", "KHOA", "NỘI DUNG TRAO ĐỔI", 
        "YÊU CẦU", "KẾT QUẢ TRAO ĐỔI", "GHI CHÚ"
    ]
    col_widths = [
        Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.1), 
        Inches(1.4), Inches(0.9), Inches(1.6), Inches(1.3), 
        Inches(1.2), Inches(0.5)
    ]
    
    # Tạo bảng: 1 hàng tiêu đề + N hàng dữ liệu
    tbl = doc.add_table(rows=len(data_rows) + 1, cols=10)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Điền hàng Header
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Times New Roman"
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    # Điền các dòng dữ liệu
    for idx, r in enumerate(data_rows):
        row_cells = tbl.rows[idx + 1].cells
        vals = [
            str(idx + 1),
            r.get("ngay_gio", ""),
            r.get("nguoi_goi", ""),
            r.get("nguoi_nghe", ""),
            r.get("ten_benh_nhan", ""),
            r.get("khoa", ""),
            r.get("noi_dung", ""),
            r.get("yeu_cau", ""),
            r.get("ket_qua", ""),
            r.get("ghi_chu", "")
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            # Căn giữa cho STT, Ngày/Giờ, Khoa; các cột còn lại căn trái
            if c_idx in [0, 1, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    doc.save(output_path)
    print(f"Đã xuất file thành công: {output_path}")

# --- Ví dụ chạy thử ---
if __name__ == "__main__":
    vi_du_du_lieu = [
        {
            "ngay_gio": "01/11/2026 14:30",
            "nguoi_goi": "Hải",
            "nguoi_nghe": "ĐD Lan",
            "ten_benh_nhan": "NGUYỄN VĂN A",
            "khoa": "HSCC",
            "noi_dung": "K+ = 7.2 mmol/L",
            "yeu_cau": "Báo động đỏ lâm sàng",
            "ket_qua": "Đã nhận tin & báo BS",
            "ghi_chu": "Mẫu chạy lại 2 lần"
        }
    ]
    generate_word_trao_doi(vi_du_du_lieu)
Tích hợp trực tiếp vào Flask WebApp
Hàm này được nối vào route Flask qua send_file:

Python
from flask import send_file
import io

@app.route("/xuat_word_trao_doi")
def xuat_word_trao_doi():
    # 1. Lấy dữ liệu từ database SQLite
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
    
    # 2. Tạo file Word vào bộ nhớ đệm BytesIO
    buf = io.BytesIO()
    # (Gọi hàm generate_word_trao_doi với buf thay vì lưu ra file ổ đĩa)
    doc.save(buf)
    buf.seek(0)
    
    return send_file(
        buf,
        as_attachment=True,
        download_name="SP.01-QTQL.SH.16-So_trao_doi_thong_tin.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
tích file này vô app được không?

Hoàn toàn tích hợp được.

Bạn muốn tích hợp file này vào app theo hướng nào:

Xuất ra file Word chuẩn mẫu này: Bổ sung nút bấm trên webapp để khi bấm xuất dữ liệu từ bảng ra, hệ thống sẽ tự động tạo file Word .docx có định dạng, tiêu đề và bảng kẻ y hệt như file mẫu này?

Nhập dữ liệu từ file Word vào webapp (Import): Tải file Word mẫu này lên webapp để hệ thống tự động đọc các hàng trong bảng và lưu vào cơ sở dữ liệu?

Mẫu sổ thứ 3 độc lập: Đây là một biểu mẫu mới cần thêm riêng 1 Tab quản lý mới trên webapp?

Bạn vui lòng gửi file hoặc tên biểu mẫu bạn muốn tích hợp để tôi viết code bổ sung ngay nhé!

Xuất ra file Word chuẩn mẫu này: Bổ sung nút bấm trên webapp để khi bấm xuất dữ liệu từ bảng ra, hệ thống sẽ tự động tạo file Word .docx có định dạng, tiêu đề và bảng kẻ y hệt như file mẫu này?

Tính năng này đã được tích hợp sẵn hoàn chỉnh ngay trên giao diện webapp của bạn.

1. Vị trí nút bấm trên WebApp
Khi truy cập vào webapp trên trình duyệt:

Chuyển sang Tab: 📞 Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16).   
app.py

Ngay góc trên bên phải của bảng danh sách, bạn sẽ thấy nút bấm màu xanh dương nổi bật:

📄 Xuất Word (SP.01-QTQL.SH.16)   
app.py

Chỉ cần nhấp chuột vào nút này, hệ thống sẽ tự động quét toàn bộ các bản ghi trong bảng và tải về máy file Word .docx hoàn chỉnh.   
app.py

2. Định dạng file Word xuất ra (Giống 100% mẫu quy định)
File Word tải về được lập trình tạo tự động với các thông số khớp chính xác với bản in:   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Khổ trang: A4 xoay ngang (Landscape), lề đều 0.5 inch (1.27 cm).   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Tiêu ngữ góc trái:

Plaintext
BỘ QUỐC PHÒNG
BỆNH VIỆN QUÂN Y 175
(Font Times New Roman, cỡ 11pt, in đậm).   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Bảng đầu sổ (chia 2 cột):

Cột trái (rộng 7.0 inch): Tên sổ SỔ TRAO ĐỔI THÔNG TIN (14pt, in đậm, căn giữa) kèm dòng Từ ngày: ……/……/20… Đến ngày: ……/……/20… / Người quản lý sổ: ………………………………… (11pt, in nghiêng).   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Cột phải (rộng 3.6 inch): Khung thông tin ISO:

Plaintext
Mã số            : SP.01-QTQL.SH.16
Lần ban hành : 01
Ngày hiệu lực : 02/01/2024
(10pt, căn lề trái).   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Bảng dữ liệu chính: Kẻ khung viền đen đầy đủ, chia đúng 10 cột theo chuẩn ISO của khoa:   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

STT	NGÀY/ GIỜ	NGƯỜI GỌI	NGƯỜI NGHE	HỌ TÊN BỆNH NHÂN	KHOA	NỘI DUNG TRAO ĐỔI	YÊU CẦU	KẾT QUẢ TRAO ĐỔI	GHI CHÚ
3. Kiểm tra thực tế
Nếu đã cập nhật code app.py mới nhất lên GitHub như hướng dẫn ở bước trước, bạn chỉ cần mở link web [https://traodoithongtin.onrender.com](https://traodoithongtin.onrender.com)[cite: 24, 26].

Nhập 1 hoặc 2 bản ghi thử nghiệm ở Tab Trao Đổi Thông Tin rồi bấm nút Xuất Word (SP.01-QTQL.SH.16) để tải về và mở trên Microsoft Word kiểm tra. Biểu mẫu đã sẵn sàng phục vụ lưu trữ hoặc in ấn ký duyệt.   
app.py

ý tôi là có thể lấy dữ liệu appweb nhảy vào bản word này không, không thay đổi cấu trúc của bản word này

Hoàn toàn được và rất dễ thực hiện. Phương pháp chuẩn nhất trong lập trình tài liệu là sử dụng chính file Word mẫu của bạn làm Template tĩnh (khung cố định):   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Giữ nguyên 100% cấu trúc gốc: Toàn bộ tiêu ngữ Bộ Quốc Phòng / Bệnh Viện Quân Y 175, bảng tiêu đề Sổ Trao Đổi Thông Tin, mã số quy trình SP.01-QTQL.SH.16, lề trang và kích thước từng cột đều được bảo tồn nguyên vẹn từ file mẫu gốc mà không bị lệch hay vẽ lại.   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx
+ 1

Dữ liệu webapp tự động nhảy vào: Khi bấm nút xuất, code sẽ mở file mẫu có sẵn, chỉ việc điền từng dòng từ CSDL vào bảng danh sách, sau đó gửi file đã điền về máy cho bạn tải xuống.   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Cách cấu hình để webapp đổ dữ liệu vào file Word mẫu
Bước 1: Đưa file Word mẫu lên kho GitHub
Đổi tên file Word mẫu bạn vừa tải lên thành: template_trao_doi.docx.   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Mở kho traodoithongtin trên GitHub.   
image_f09c4b.png

Bấm Add file 
→
→ chọn Upload files.   
image_f11142.png
+ 1

Kéo file template_trao_doi.docx thả vào và bấm nút xanh Commit changes để lưu vào cùng thư mục với app.py.   
image_f10d82.png

Bước 2: Cập nhật hàm xuất Word trong app.py
Mở file app.py trên GitHub (bấm biểu tượng cây bút chì để sửa), tìm đến hàm generate_word_trao_doi và thay bằng đoạn mã nạp trực tiếp từ template sau:   
image_f09c4b.png

Python
def generate_word_trao_doi(rows):
    template_path = "template_trao_doi.docx"
    
    # 1. Mở trực tiếp file Word mẫu gốc nếu có trên thư mục
    if os.path.exists(template_path):
        doc = docx.Document(template_path)
        table = doc.tables[1] # Bảng số 1 là bảng chứa 10 cột dữ liệu
    else:
        # Nếu chưa tìm thấy file template thì dùng hàm tạo khung dự phòng
        return generate_word_trao_doi_fallback(rows)

    # 2. Đổ từng dòng dữ liệu từ webapp vào bảng của file mẫu
    for idx, r in enumerate(rows):
        new_row = table.add_row()
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["nguoi_goi"] or "",
            r["nguoi_nghe"] or "",
            r["ten_benh_nhan"] or "",
            r["khoa"] or "",
            r["noi_dung"] or "",
            r["yeu_cau"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            cell = new_row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            # Căn giữa cho các cột STT, Ngày/giờ, Khoa; các cột khác căn trái
            if c_idx in [0, 1, 5]:
                p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.LEFT
            
            # Định dạng font chữ đồng bộ theo mẫu
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = docx.shared.Pt(9)

    # 3. Xuất file ra bộ nhớ để tải về
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf
Sau khi bấm Commit changes, bạn chỉ cần lên webapp bấm nút Xuất Word (SP.01-QTQL.SH.16). Toàn bộ dữ liệu bạn đã nhập sẽ tự động điền vào các dòng trong bảng của chính file mẫu này.   
app.py
+ 1

cho mình bản app hoàn chỉnh đi

bạn đâu rồi

Bản cập nhật hoàn chỉnh tích hợp cơ chế nạp trực tiếp dữ liệu vào mẫu Word gốc:

File mã nguồn cập nhật (app.py): 
Biểu tượng PY
app
 PY 
Biểu tượng PY
app
 PY 

File Word mẫu chuẩn (template_trao_doi.docx): 
Biểu tượng DOCX
template_trao_doi
 DOCX 
Biểu tượng DOCX
template_trao_doi
 DOCX 

Gói nén trọn bộ (bo_cai_dat_hoan_chinh.zip): 
Biểu tượng ZIP
bo_cai_dat_hoan_chinh
 ZIP 

Cơ chế hoạt động của bản cập nhật này:
Giữ nguyên 100% bản mẫu gốc: Hệ thống mở trực tiếp file template_trao_doi.docx trên máy chủ và chèn từng dòng bản ghi từ cơ sở dữ liệu vào đúng bảng 10 cột, không làm xê dịch bảng tiêu đề hay tiêu ngữ Bộ Quốc Phòng / Bệnh Viện Quân Y 175.

Cơ chế dự phòng (Fallback): Nếu chưa tải file template_trao_doi.docx lên thư mục, code sẽ tự động tạo khung Word tương đương để quá trình tải dữ liệu không bị gián đoạn.

Phân quyền & Tài khoản: Tích hợp trang quản lý tài khoản thành viên, chức năng đổi mật khẩu cá nhân và đặt lại mật khẩu cho nhân viên trực.

Hướng dẫn cập nhật lên GitHub (2 bước):
Tải file mẫu lên GitHub:

Tải file 
 về máy.

Truy cập kho donhuhai2/traodoithongtin trên GitHub, chọn Add file 
→
→ Upload files.   
app.py
+ 1

Kéo thả file template_trao_doi.docx vào và bấm Commit changes.   
SP.01-QTQL.SH.16-So_trao_doi_thong_tin_20261101.docx

Cập nhật app.py:

Mở file 
, copy toàn bộ mã nguồn.

Mở file app.py trên GitHub, bấm biểu tượng cây bút chì, dán đè toàn bộ nội dung mới và bấm Commit changes.

Sau khi cập nhật, Render sẽ tự động triển khai lại ứng dụng trong khoảng 1 phút. Khi bấm Xuất Word Chuẩn Mẫu (SP.01-QTQL.SH.16) trên web, dữ liệu sẽ được điền trực tiếp vào biểu mẫu Word gốc.







Gemini là một AI và có thể mắc sai sót.

Processed and analyzed in code
import sqlite3
import csv
import io
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template_string, request, redirect, url_for, Response, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

app = Flask(__name__)
app.secret_key = "lab_records_secret_bvqy175_auth_key_v4"
DB_NAME = "lab_records.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT DEFAULT 'staff'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS canh_bao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ngay_gio TEXT,
                khoa TEXT,
                nguoi_bao_cao TEXT,
                nguoi_nhan TEXT,
                ten_benh_nhan TEXT,
                ma_benh_nhan TEXT,
                noi_dung TEXT,
                ket_qua TEXT,
                ghi_chu TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trao_doi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ngay_gio TEXT,
                nguoi_goi TEXT,
                nguoi_nghe TEXT,
                ten_benh_nhan TEXT,
                khoa TEXT,
                noi_dung TEXT,
                yeu_cau TEXT,
                ket_qua TEXT,
                ghi_chu TEXT
            )
        """)
        
        user = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
        if not user:
            default_pwd = generate_password_hash("123456")
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         ("admin", default_pwd, "Quản trị viên PXN", "admin"))
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         ("nhanvien", default_pwd, "Kỹ thuật viên Trực", "staff"))

# Gọi tạo bảng ngay tại tầng module
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Chỉ quản trị viên mới có quyền thực hiện thao tác này!", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bc, nguoi_nhan, ten_bn, khoa, ket_qua_cb, noi_dung_cb, ghi_chu_cb):
    conn.execute("""
        INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ngay_gio,
        nguoi_bc,
        nguoi_nhan,
        ten_bn,
        khoa,
        ket_qua_cb,
        noi_dung_cb,
        ghi_chu_cb,
        "Đồng bộ từ Sổ Cảnh Báo"
    ))

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng nhập - Sổ Điện Tử BVQY 175</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #0d6efd 0%, #002b66 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Segoe UI', Tahoma, sans-serif; }
        .card-login { max-width: 420px; width: 100%; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); border: none; }
    </style>
</head>
<body>
<div class="card card-login p-4 bg-white">
    <div class="text-center mb-4">
        <h4 class="fw-bold text-primary mb-1"><i class="bi bi-hospital me-2"></i>BVQY 175</h4>
        <div class="text-uppercase small fw-bold text-muted">Hệ Thống Quản Lý Sổ Xét Nghiệm</div>
        <div class="badge bg-light text-dark border mt-2">ISO 15189 / QLCL</div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show py-2 small" role="alert">
            {{ message }}
            <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <form method="POST" action="/login">
        <div class="mb-3">
            <label class="form-label small fw-bold">Tên đăng nhập</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-person"></i></span>
                <input type="text" name="username" class="form-control" placeholder="admin hoặc nhanvien" required autofocus>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label small fw-bold">Mật khẩu</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                <input type="password" name="password" class="form-control" placeholder="••••••••" required>
            </div>
        </div>
        <button type="submit" class="btn btn-primary w-100 fw-bold py-2 mb-3">Đăng Nhập <i class="bi bi-box-arrow-in-right ms-1"></i></button>
    </form>
    
    <div class="alert alert-info py-2 small mb-0">
        <strong>Tài khoản mặc định:</strong><br>
        • Quản trị: <code>admin</code> / MK: <code>123456</code><br>
        • Nhân viên: <code>nhanvien</code> / MK: <code>123456</code>
    </div>
</div>
</body>
</html>
"""

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Sổ Điện Tử XN - BVQY 175</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .nav-tabs .nav-link { font-weight: 600; font-size: 1.02rem; }
        .nav-tabs .nav-link.active { color: #0d6efd; border-bottom: 3px solid #0d6efd; }
        .card { border-radius: 10px; border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
        .table-responsive { max-height: 540px; overflow-y: auto; }
        .table thead th { position: sticky; top: 0; background-color: #e9ecef; z-index: 1; }
    </style>
</head>
<body class="py-3">
<div class="container-fluid px-4">
    <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom flex-wrap gap-2">
        <div>
            <h4 class="text-primary fw-bold mb-1">🏥 HỆ THỐNG QUẢN LÝ SỔ ĐIỆN TỬ PHÒNG XÉT NGHIỆM</h4>
            <span class="text-muted small">Bệnh viện Quân y 175 — Chuẩn quản lý chất lượng ISO 15189</span>
        </div>
        <div class="d-flex align-items-center gap-2">
            <div class="text-end me-2">
                <span class="fw-bold d-block">{{ session.get('full_name') }}</span>
                <span class="badge bg-secondary small">Quyền: {{ session.get('role') }}</span>
            </div>
            <button class="btn btn-outline-primary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#changePassModal">
                <i class="bi bi-key me-1"></i>Đổi mật khẩu
            </button>
            <a href="/logout" class="btn btn-outline-danger btn-sm fw-bold"><i class="bi bi-box-arrow-right me-1"></i>Đăng xuất</a>
        </div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show py-2" role="alert">
            {{ message }}
            <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <ul class="nav nav-tabs mb-3" id="labTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="tab-cb-btn" data-bs-toggle="tab" data-bs-target="#tab-cb" type="button">
                🚨 Sổ Báo Cáo KQ Cảnh Báo (SP.01-QTQL.SH.37)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-td-btn" data-bs-toggle="tab" data-bs-target="#tab-td" type="button">
                📞 Sổ Trao Đổi Thông Tin (SP.01-QTQL.SH.16)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-users-btn" data-bs-toggle="tab" data-bs-target="#tab-users" type="button">
                👥 Quản Lý Thành Viên & Mật Khẩu
            </button>
        </li>
    </ul>

    <div class="tab-content" id="labTabsContent">
        <!-- TAB 1: CẢNH BÁO -->
        <div class="tab-pane fade show active" id="tab-cb" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-danger mb-3">➕ Thêm Báo Cáo Kết Quả Cảnh Báo</h6>
                        <form method="POST" action="/add_canh_bao">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ báo cáo</label>
                                    <input type="text" name="ngay_gio" class="form-control form-control-sm" value="{{ now_str }}" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: HSCC" required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người báo cáo</label>
                                    <input type="text" name="nguoi_bao_cao" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nhận</label>
                                    <input type="text" name="nguoi_nhan" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Tên bệnh nhân</label>
                                    <input type="text" name="ten_benh_nhan" class="form-control form-control-sm" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Mã số BN (PID)</label>
                                    <input type="text" name="ma_benh_nhan" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Kết quả báo cáo (Giá trị báo động)</label>
                                <input type="text" name="ket_qua" class="form-control form-control-sm text-danger fw-bold" placeholder="VD: K+ 7.2 mmol/L..." required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Nội dung trao đổi</label>
                                <textarea name="noi_dung" class="form-control form-control-sm" rows="2" placeholder="Nội dung cụ thể cần trao đổi / xử lý lâm sàng..."></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm" placeholder="Phản hồi từ khoa lâm sàng / xác nhận...">
                            </div>

                            <div class="form-check form-switch mb-3 p-2 bg-light rounded border">
                                <input class="form-check-input ms-0 me-2" type="checkbox" name="auto_sync" id="autoSyncCheck" checked>
                                <label class="form-check-label small fw-bold text-primary" for="autoSyncCheck">
                                    ⚡ Tự động đồng bộ sang Sổ trao đổi thông tin
                                </label>
                            </div>

                            <button type="submit" class="btn btn-danger w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Bản Ghi Cảnh Báo</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Danh Sách Kết Quả Cảnh Báo ({{ canh_bao_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2">
                                <a href="/export_word/canh_bao" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word (SP.01-QTQL.SH.37)</a>
                                <a href="/export/canh_bao" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Ngày/giờ</th>
                                        <th>Khoa</th>
                                        <th>Người BC</th>
                                        <th>Người nhận</th>
                                        <th>Bệnh nhân</th>
                                        <th>Mã BN</th>
                                        <th>Kết quả</th>
                                        <th>Nội dung</th>
                                        <th>Ghi chú</th>
                                        <th class="text-center">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in canh_bao_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.ngay_gio }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td>{{ row.nguoi_bao_cao }}</td>
                                        <td>{{ row.nguoi_nhan }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td>{{ row.ma_benh_nhan }}</td>
                                        <td class="text-danger fw-bold">{{ row.ket_qua }}</td>
                                        <td>{{ row.noi_dung }}</td>
                                        <td>{{ row.ghi_chu }}</td>
                                        <td class="text-center text-nowrap">
                                            <a href="/sync_one/{{ row.id }}" class="btn btn-sm btn-outline-primary py-0 px-2" title="Đồng bộ sang Sổ trao đổi">
                                                <i class="bi bi-arrow-repeat"></i> Đồng bộ
                                            </a>
                                        </td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="11" class="text-center text-muted py-3">Chưa có bản ghi nào.</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: TRAO ĐỔI THÔNG TIN -->
        <div class="tab-pane fade" id="tab-td" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-primary mb-3">➕ Thêm Nhật Ký Trao Đổi Thủ Công</h6>
                        <form method="POST" action="/add_trao_doi">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ</label>
                                    <input type="text" name="ngay_gio" class="form-control form-control-sm" value="{{ now_str }}" required>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: Ngoại..." required>
                                </div>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người gọi</label>
                                    <input type="text" name="nguoi_goi" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nghe</label>
                                    <input type="text" name="nguoi_nghe" class="form-control form-control-sm" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Họ tên bệnh nhân</label>
                                <input type="text" name="ten_benh_nhan" class="form-control form-control-sm">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Nội dung trao đổi</label>
                                <textarea name="noi_dung" class="form-control form-control-sm" rows="2" required></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Yêu cầu</label>
                                <input type="text" name="yeu_cau" class="form-control form-control-sm" placeholder="VD: Lấy lại mẫu, bổ sung thông tin...">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Kết quả trao đổi</label>
                                <input type="text" name="ket_qua" class="form-control form-control-sm" placeholder="VD: Đã đồng ý gửi lại...">
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Cuộc Trao Đổi</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Nhật Ký Trao Đổi Thông Tin ({{ trao_doi_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2">
                                <a href="/export_word/trao_doi" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word Chuẩn Mẫu (SP.01-QTQL.SH.16)</a>
                                <a href="/export/trao_doi" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Ngày/giờ</th>
                                        <th>Người gọi</th>
                                        <th>Người nghe</th>
                                        <th>Bệnh nhân</th>
                                        <th>Khoa</th>
                                        <th>Nội dung trao đổi</th>
                                        <th>Yêu cầu</th>
                                        <th>Kết quả trao đổi</th>
                                        <th>Ghi chú</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in trao_doi_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.ngay_gio }}</td>
                                        <td>{{ row.nguoi_goi }}</td>
                                        <td>{{ row.nguoi_nghe }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td class="text-danger fw-bold">{{ row.noi_dung }}</td>
                                        <td>{{ row.yeu_cau }}</td>
                                        <td>{{ row.ket_qua }}</td>
                                        <td>{{ row.ghi_chu }}</td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="10" class="text-center text-muted py-3">Chưa có bản ghi nào.</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: QUẢN LÝ THÀNH VIÊN & MẬT KHẨU -->
        <div class="tab-pane fade" id="tab-users" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-success mb-3"><i class="bi bi-person-plus-fill me-1"></i>Tạo Tài Khoản Thành Viên Mới</h6>
                        {% if session.get('role') == 'admin' %}
                        <form method="POST" action="/create_user">
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Họ và tên nhân viên</label>
                                <input type="text" name="full_name" class="form-control form-control-sm" placeholder="VD: CN. Nguyễn Văn A" required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Tên đăng nhập (username)</label>
                                <input type="text" name="username" class="form-control form-control-sm" placeholder="VD: nguyenvana (viết liền không dấu)" required>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Mật khẩu khởi tạo</label>
                                <input type="password" name="password" class="form-control form-control-sm" placeholder="Tối thiểu 6 ký tự" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Vai trò / Quyền hạn</label>
                                <select name="role" class="form-select form-select-sm">
                                    <option value="staff">Kỹ thuật viên / Nhân viên (staff)</option>
                                    <option value="admin">Quản trị viên (admin)</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-success w-100 fw-bold"><i class="bi bi-check-circle me-1"></i>Tạo Tài Khoản</button>
                        </form>
                        {% else %}
                        <div class="alert alert-warning small mb-0">
                            <i class="bi bi-info-circle me-1"></i>Tính năng tạo tài khoản mới chỉ dành cho tài khoản <strong>Quản trị viên (admin)</strong>. Bạn đang đăng nhập bằng quyền nhân viên.
                        </div>
                        {% endif %}
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h6 class="fw-bold mb-0"><i class="bi bi-people-fill me-1"></i>Danh Sách Thành Viên ({{ users_list|length }} người)</h6>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Họ và tên</th>
                                        <th>Tên đăng nhập</th>
                                        <th>Vai trò</th>
                                        <th class="text-center">Quản lý mật khẩu & Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for u in users_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="fw-bold">{{ u.full_name }}</td>
                                        <td><code>{{ u.username }}</code></td>
                                        <td>
                                            {% if u.role == 'admin' %}
                                            <span class="badge bg-danger">Quản trị viên</span>
                                            {% else %}
                                            <span class="badge bg-info text-dark">Kỹ thuật viên</span>
                                            {% endif %}
                                        </td>
                                        <td class="text-center text-nowrap">
                                            {% if session.get('role') == 'admin' or session.get('username') == u.username %}
                                            <button class="btn btn-sm btn-outline-warning py-0 px-2" data-bs-toggle="modal" data-bs-target="#adminResetModal{{ u.id }}">
                                                <i class="bi bi-key-fill"></i> Đổi MK
                                            </button>
                                            {% endif %}
                                            {% if session.get('role') == 'admin' and u.username != 'admin' and u.username != session.get('username') %}
                                            <a href="/delete_user/{{ u.id }}" class="btn btn-sm btn-outline-danger py-0 px-2 ms-1" onclick="return confirm('Bạn có chắc chắn muốn xóa tài khoản {{ u.username }} không?');">
                                                <i class="bi bi-trash"></i>
                                            </a>
                                            {% endif %}
                                        </td>
                                    </tr>

                                    <div class="modal fade" id="adminResetModal{{ u.id }}" tabindex="-1">
                                        <div class="modal-dialog modal-dialog-centered modal-sm">
                                            <div class="modal-content">
                                                <div class="modal-header py-2">
                                                    <h6 class="modal-title fw-bold">Đổi MK: {{ u.full_name }}</h6>
                                                    <button type="button" class="btn-close py-2" data-bs-dismiss="modal"></button>
                                                </div>
                                                <form method="POST" action="/reset_user_password">
                                                    <div class="modal-body py-3">
                                                        <input type="hidden" name="user_id" value="{{ u.id }}">
                                                        <div class="mb-2">
                                                            <label class="form-label small fw-bold">Mật khẩu mới</label>
                                                            <input type="password" name="new_password" class="form-control form-control-sm" placeholder="Nhập MK mới..." required>
                                                        </div>
                                                    </div>
                                                    <div class="modal-footer py-2">
                                                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                                                        <button type="submit" class="btn btn-warning btn-sm fw-bold">Cập Nhật MK</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="changePassModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-primary text-white">
                <h6 class="modal-title fw-bold"><i class="bi bi-shield-lock me-1"></i>Đổi Mật Khẩu Cá Nhân</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="/change_own_password">
                <div class="modal-body py-3">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Mật khẩu hiện tại</label>
                        <input type="password" name="current_password" class="form-control" placeholder="Nhập mật khẩu đang dùng" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Mật khẩu mới</label>
                        <input type="password" name="new_password" class="form-control" placeholder="Tối thiểu 6 ký tự" required>
                    </div>
                    <div class="mb-2">
                        <label class="form-label small fw-bold">Xác nhận mật khẩu mới</label>
                        <input type="password" name="confirm_password" class="form-control" placeholder="Nhập lại mật khẩu mới" required>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-check-lg me-1"></i>Lưu Mật Khẩu Mới</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
    if (window.location.hash === '#tab-td') {
        const tabTrigger = new bootstrap.Tab(document.querySelector('#tab-td-btn'));
        tabTrigger.show();
    } else if (window.location.hash === '#tab-users') {
        const tabTrigger = new bootstrap.Tab(document.querySelector('#tab-users-btn'));
        tabTrigger.show();
    }
</script>
</body>
</html>
"""

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(r"""<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders>""")
    tblPr.append(borders_xml)

def generate_word_canh_bao(rows):
    doc = docx.Document()
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)
    section.page_height = Inches(8.27)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    p_header.paragraph_format.line_spacing = 1.0
    r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.name = "Times New Roman"

    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    
    cell_left = tbl_top.cell(0, 0)
    cell_left.width = Inches(7.0)
    p_title = cell_left.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("SỔ\nTHEO DÕI BÁO CÁO KẾT QUẢ CẢNH BÁO\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.name = "Times New Roman"
    r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: CN. Phạm Minh Nhi")
    r_t2.font.size = Pt(11)
    r_t2.italic = True
    r_t2.font.name = "Times New Roman"

    cell_right = tbl_top.cell(0, 1)
    cell_right.width = Inches(3.6)
    p_code = cell_right.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.37\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
    r_code.font.size = Pt(10)
    r_code.font.name = "Times New Roman"

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    headers = ["STT", "Ngày/giờ\nbáo cáo", "Khoa", "Người\nbáo cáo", "Người nhận\nbáo cáo", "Tên bệnh nhân", "Mã số\nbệnh nhân", "Nội dung\ntrao đổi", "Kết quả\nbáo cáo", "Ghi chú"]
    col_widths = [Inches(0.5), Inches(1.1), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.3), Inches(1.0), Inches(1.6), Inches(1.2), Inches(0.9)]
    
    tbl = doc.add_table(rows=len(rows) + 1, cols=10)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(title.replace("\\n", "\n"))
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Times New Roman"
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    for idx, r in enumerate(rows):
        row_cells = tbl.rows[idx + 1].cells
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["khoa"] or "",
            r["nguoi_bao_cao"] or "",
            r["nguoi_nhan"] or "",
            r["ten_benh_nhan"] or "",
            r["ma_benh_nhan"] or "",
            r["noi_dung"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 2, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            if c_idx == 8:
                run.bold = True
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# Xuất Word sổ Trao Đổi: TỰ ĐỘNG NẠP TRỰC TIẾP TỪ TEMPLATE NẾU CÓ
def generate_word_trao_doi(rows):
    template_file = "template_trao_doi.docx"
    
    if os.path.exists(template_file):
        doc = docx.Document(template_file)
        tbl = doc.tables[1]
    else:
        # Nếu chưa upload file template, tạo động theo đúng quy cách
        doc = docx.Document()
        section = doc.sections[0]
        section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
        section.page_width = Inches(11.69)
        section.page_height = Inches(8.27)
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

        p_header = doc.add_paragraph()
        p_header.paragraph_format.space_after = Pt(2)
        p_header.paragraph_format.line_spacing = 1.0
        r1 = p_header.add_run("BỘ QUỐC PHÒNG\nBỆNH VIỆN QUÂN Y 175\n")
        r1.bold = True
        r1.font.size = Pt(11)
        r1.font.name = "Times New Roman"

        tbl_top = doc.add_table(rows=1, cols=2)
        tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_top.autofit = False
        
        cell_left = tbl_top.cell(0, 0)
        cell_left.width = Inches(7.0)
        p_title = cell_left.paragraphs[0]
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_t1 = p_title.add_run("SỔ TRAO ĐỔI THÔNG TIN\n")
        r_t1.bold = True
        r_t1.font.size = Pt(14)
        r_t1.font.name = "Times New Roman"
        r_t2 = p_title.add_run("Từ ngày: ……/……/20…   Đến ngày: ……/……/20…\nNgười quản lý sổ: …………………………………")
        r_t2.font.size = Pt(11)
        r_t2.italic = True
        r_t2.font.name = "Times New Roman"

        cell_right = tbl_top.cell(0, 1)
        cell_right.width = Inches(3.6)
        p_code = cell_right.paragraphs[0]
        p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_code = p_code.add_run("Mã số            : SP.01-QTQL.SH.16\nLần ban hành : 01\nNgày hiệu lực : 02/01/2024")
        r_code.font.size = Pt(10)
        r_code.font.name = "Times New Roman"

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

        headers = ["STT", "NGÀY/ GIỜ", "NGƯỜI GỌI", "NGƯỜI NGHE", "HỌ TÊN BỆNH NHÂN", "KHOA", "NỘI DUNG TRAO ĐỔI", "YÊU CẦU", "KẾT QUẢ TRAO ĐỔI", "GHI CHÚ"]
        col_widths = [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.4), Inches(0.9), Inches(1.6), Inches(1.3), Inches(1.2), Inches(0.5)]
        
        tbl = doc.add_table(rows=1, cols=10)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl)

        hdr_cells = tbl.rows[0].cells
        for i, title in enumerate(headers):
            hdr_cells[i].width = col_widths[i]
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(title)
            run.bold = True
            run.font.size = Pt(9.5)
            run.font.name = "Times New Roman"
            set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)

    # Đổ các dòng dữ liệu vào bảng
    col_widths = [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.4), Inches(0.9), Inches(1.6), Inches(1.3), Inches(1.2), Inches(0.5)]
    for idx, r in enumerate(rows):
        row_cells = tbl.add_row().cells
        vals = [
            str(idx + 1),
            r["ngay_gio"] or "",
            r["nguoi_goi"] or "",
            r["nguoi_nghe"] or "",
            r["ten_benh_nhan"] or "",
            r["khoa"] or "",
            r["noi_dung"] or "",
            r["yeu_cau"] or "",
            r["ket_qua"] or "",
            r["ghi_chu"] or ""
        ]
        for c_idx, val in enumerate(vals):
            row_cells[c_idx].width = col_widths[c_idx]
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = "Times New Roman"
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ----------------- ROUTES -----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["full_name"] = user["full_name"]
                session["role"] = user["role"]
                flash(f"Xin chào {user['full_name']}!", "success")
                return redirect(url_for("index"))
            else:
                flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất an toàn.", "info")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao ORDER BY id DESC").fetchall()
        td = conn.execute("SELECT * FROM trao_doi ORDER BY id DESC").fetchall()
        users = conn.execute("SELECT id, username, full_name, role FROM users ORDER BY id ASC").fetchall()
    return render_template_string(MAIN_TEMPLATE, now_str=now_str, canh_bao_list=cb, trao_doi_list=td, users_list=users)

@app.route("/add_canh_bao", methods=["POST"])
@login_required
def add_canh_bao():
    ngay_gio = request.form.get("ngay_gio")
    khoa = request.form.get("khoa")
    nguoi_bao_cao = request.form.get("nguoi_bao_cao")
    nguoi_nhan = request.form.get("nguoi_nhan")
    ten_benh_nhan = request.form.get("ten_benh_nhan")
    ma_benh_nhan = request.form.get("ma_benh_nhan")
    noi_dung = request.form.get("noi_dung")
    ket_qua = request.form.get("ket_qua")
    ghi_chu = request.form.get("ghi_chu")
    auto_sync = request.form.get("auto_sync")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO canh_bao (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu))

        if auto_sync:
            sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, khoa, ket_qua, noi_dung, ghi_chu)
            flash("✅ Đã lưu vào Sổ Cảnh Báo VÀ tự động đồng bộ sang Sổ Trao Đổi Thông Tin!", "success")
        else:
            flash("✅ Đã lưu vào Sổ Cảnh Báo thành công!", "success")

    return redirect(url_for("index"))

@app.route("/sync_one/<int:cb_id>")
@login_required
def sync_one(cb_id):
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao WHERE id = ?", (cb_id,)).fetchone()
        if cb:
            sync_canh_bao_to_trao_doi(
                conn,
                cb["ngay_gio"],
                cb["nguoi_bao_cao"],
                cb["nguoi_nhan"],
                cb["ten_benh_nhan"],
                cb["khoa"],
                cb["ket_qua"],
                cb["noi_dung"],
                cb["ghi_chu"]
            )
            flash(f"✅ Đã đồng bộ bản ghi BN {cb['ten_benh_nhan']} sang Sổ Trao Đổi!", "info")
    return redirect(url_for("index") + "#tab-td")

@app.route("/add_trao_doi", methods=["POST"])
@login_required
def add_trao_doi():
    with get_db() as conn:
        conn.execute("""
            INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form.get("ngay_gio"),
            request.form.get("nguoi_goi"),
            request.form.get("nguoi_nghe"),
            request.form.get("ten_benh_nhan"),
            request.form.get("khoa"),
            request.form.get("noi_dung"),
            request.form.get("yeu_cau"),
            request.form.get("ket_qua"),
            request.form.get("ghi_chu")
        ))
        flash("✅ Đã lưu cuộc trao đổi thông tin thành công!", "success")
    return redirect(url_for("index") + "#tab-td")

# ----------------- QUẢN LÝ TÀI KHOẢN & MẬT KHẨU -----------------

@app.route("/create_user", methods=["POST"])
@login_required
@admin_required
def create_user():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()
    full_name = request.form.get("full_name", "").strip()
    role = request.form.get("role", "staff")

    if not username or not password or not full_name:
        flash("Vui lòng điền đầy đủ thông tin tài khoản!", "danger")
        return redirect(url_for("index") + "#tab-users")

    if len(password) < 6:
        flash("Mật khẩu phải có tối thiểu 6 ký tự!", "danger")
        return redirect(url_for("index") + "#tab-users")

    pwd_hash = generate_password_hash(password)
    try:
        with get_db() as conn:
            conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                         (username, pwd_hash, full_name, role))
        flash(f"✅ Đã tạo tài khoản thành công cho {full_name} ({username})!", "success")
    except sqlite3.IntegrityError:
        flash(f"Tên đăng nhập '{username}' đã tồn tại, vui lòng chọn tên khác!", "danger")

    return redirect(url_for("index") + "#tab-users")

@app.route("/change_own_password", methods=["POST"])
@login_required
def change_own_password():
    current_pwd = request.form.get("current_password", "").strip()
    new_pwd = request.form.get("new_password", "").strip()
    confirm_pwd = request.form.get("confirm_password", "").strip()

    if new_pwd != confirm_pwd:
        flash("Mật khẩu mới và xác nhận mật khẩu không trùng khớp!", "danger")
        return redirect(url_for("index"))

    if len(new_pwd) < 6:
        flash("Mật khẩu mới phải có tối thiểu 6 ký tự!", "danger")
        return redirect(url_for("index"))

    user_id = session.get("user_id")
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user or not check_password_hash(user["password_hash"], current_pwd):
            flash("Mật khẩu hiện tại không chính xác!", "danger")
            return redirect(url_for("index"))

        new_hash = generate_password_hash(new_pwd)
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        flash("✅ Đã đổi mật khẩu cá nhân thành công!", "success")

    return redirect(url_for("index"))

@app.route("/reset_user_password", methods=["POST"])
@login_required
def reset_user_password():
    target_id = request.form.get("user_id")
    new_pwd = request.form.get("new_password", "").strip()

    if session.get("role") != "admin" and str(session.get("user_id")) != str(target_id):
        flash("Bạn không có quyền đổi mật khẩu của tài khoản này!", "danger")
        return redirect(url_for("index") + "#tab-users")

    if len(new_pwd) < 6:
        flash("Mật khẩu mới phải có ít nhất 6 ký tự!", "danger")
        return redirect(url_for("index"))

    new_hash = generate_password_hash(new_pwd)
    with get_db() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, target_id))
        user = conn.execute("SELECT full_name FROM users WHERE id = ?", (target_id,)).fetchone()
        name = user["full_name"] if user else "thành viên"
        flash(f"✅ Đã cập nhật mật khẩu mới cho {name}!", "success")

    return redirect(url_for("index") + "#tab-users")

@app.route("/delete_user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    if user_id == session.get("user_id"):
        flash("Bạn không thể tự xóa tài khoản của chính mình!", "danger")
        return redirect(url_for("index") + "#tab-users")

    with get_db() as conn:
        user = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
        if user and user["username"] == "admin":
            flash("Không thể xóa tài khoản admin gốc!", "danger")
            return redirect(url_for("index") + "#tab-users")

        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        flash("Đã xóa tài khoản thành viên thành công!", "info")

    return redirect(url_for("index") + "#tab-users")

# ----------------- XUẤT WORD & CSV -----------------

@app.route("/export_word/<book_type>")
@login_required
def export_word(book_type):
    with get_db() as conn:
        if book_type == "canh_bao":
            rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            buf = generate_word_canh_bao(rows)
            filename = f"SP.01-QTQL.SH.37-So_theo_doi_bao_cao_KQ_canh_bao_{datetime.now().strftime('%Y%m%d')}.docx"
        else:
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            buf = generate_word_trao_doi(rows)
            filename = f"SP.01-QTQL.SH.16-So_trao_doi_thong_tin_{datetime.now().strftime('%Y%m%d')}.docx"

    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.route("/export/<book_type>")
@login_required
def export_csv(book_type):
    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    with get_db() as conn:
        if book_type == "canh_bao":
            writer.writerow(["STT", "Ngày/Giờ", "Khoa", "Người báo cáo", "Người nhận", "Tên bệnh nhân", "Mã số BN", "Nội dung trao đổi", "Kết quả báo cáo", "Ghi chú"])
            rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["khoa"], r["nguoi_bao_cao"], r["nguoi_nhan"], r["ten_benh_nhan"], r["ma_benh_nhan"], r["noi_dung"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Canh_Bao_SP01_QTQL_SH_37_{datetime.now().strftime('%Y%m%d')}.csv"
        else:
            writer.writerow(["STT", "Ngày/Giờ", "Người gọi", "Người nghe", "Tên bệnh nhân", "Khoa", "Nội dung trao đổi", "Yêu cầu", "Kết quả trao đổi", "Ghi chú"])
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["nguoi_goi"], r["nguoi_nghe"], r["ten_benh_nhan"], r["khoa"], r["noi_dung"], r["yeu_cau"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Trao_Doi_SP01_QTQL_SH_16_{datetime.now().strftime('%Y%m%d')}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    init_db()
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
app.py
Đang hiển thị app.py.
