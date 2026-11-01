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
