import sqlite3
import csv
import io
import os
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2 import IntegrityError as PGIntegrityError
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    PGIntegrityError = Exception
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import Flask, render_template_string, request, redirect, url_for, Response, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

app = Flask(__name__)
app.secret_key = "lab_records_secret_bvqy175_auth_key_v13"
DB_NAME = "lab_records.db"

# Múi giờ chuẩn Việt Nam (UTC+7 / GMT+7)
VN_TZ = timezone(timedelta(hours=7))

def get_now_vn():
    return datetime.now(VN_TZ)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_cleaned_db_url(url):
    if not url:
        return None
    url = url.strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    # Loại bỏ tham số ?pgbouncer=true của Prisma vì driver libpq/psycopg2 không hỗ trợ tham số này
    import re
    url = re.sub(r'[\?\&]pgbouncer=[^&]*', '', url)
    if url.endswith("?"):
        url = url[:-1]
    return url

class UnifiedDB:
    def __init__(self):
        cleaned_url = get_cleaned_db_url(DATABASE_URL)
        if cleaned_url and psycopg2:
            try:
                self.conn = psycopg2.connect(cleaned_url, cursor_factory=RealDictCursor)
                self.is_pg = True
                return
            except Exception as e:
                print("⚠️ Không thể kết nối PostgreSQL Supabase, tự động chuyển về SQLite dự phòng:", e)
        
        # Dùng SQLite nội bộ nếu không có PostgreSQL hoặc kết nối thất bại
        self.is_pg = False
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

    def execute(self, query, params=None):
        if self.is_pg:
            pg_query = query.replace('?', '%s')
            cur = self.conn.cursor()
            cur.execute(pg_query, params or ())
            return cur
        else:
            if params is not None:
                return self.conn.execute(query, params)
            return self.conn.execute(query)

def get_db():
    return UnifiedDB()

def init_db():
    try:
        with get_db() as conn:
            id_type = "SERIAL PRIMARY KEY" if conn.is_pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS users (
                    id {id_type},
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT DEFAULT 'staff'
                )
            """)
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS canh_bao (
                    id {id_type},
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
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS trao_doi (
                    id {id_type},
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
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS tu_choi (
                    id {id_type},
                    thoi_gian TEXT,
                    ten_benh_nhan TEXT,
                    nam_sinh_nam TEXT,
                    nam_sinh_nu TEXT,
                    khoa TEXT,
                    ly_do TEXT,
                    cach_xu_ly TEXT,
                    nguoi_nhan TEXT,
                    nguoi_gui TEXT,
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
    except Exception as e:
        print("Lỗi khởi tạo DB:", e)

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
        ngay_gio, nguoi_bc, nguoi_nhan, ten_bn, khoa, ket_qua_cb, noi_dung_cb, ghi_chu_cb, "Đồng bộ từ Sổ Cảnh Báo"
    ))

def parse_date_str(val):
    if not val:
        return None
    val = str(val).strip()
    for fmt in (
        "%d/%m/%y %H:%M:%S", "%d/%m/%y %H:%M", "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M", "%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%m-%Y"
    ):
        try:
            return datetime.strptime(val.split()[0], fmt.split()[0]).date()
        except Exception:
            continue
    return None

def filter_records_by_date(rows, from_date_str, to_date_str, date_field="ngay_gio"):
    if not from_date_str and not to_date_str:
        return rows
    d_from = datetime.strptime(from_date_str, "%Y-%m-%d").date() if from_date_str else None
    d_to = datetime.strptime(to_date_str, "%Y-%m-%d").date() if to_date_str else None
    
    filtered = []
    for r in rows:
        d_val = parse_date_str(r[date_field])
        if d_val:
            if d_from and d_val < d_from:
                continue
            if d_to and d_val > d_to:
                continue
        filtered.append(r)
    return filtered

def format_cell_value(v):
    if pd.isna(v):
        return ""
    if isinstance(v, (datetime, pd.Timestamp)):
        return v.strftime("%d/%m/%y %H:%M:%S")
    return str(v).strip()

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
        .btn-set-now { cursor: pointer; }
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
                {% if session.get('role') == 'admin' %}
                <span class="badge bg-danger small">Quyền: Quản trị viên</span>
                {% else %}
                <span class="badge bg-secondary small">Quyền: Kỹ thuật viên</span>
                {% endif %}
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
                🚨 Sổ KQ Cảnh Báo (SP.01-QTQL.SH.37)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-td-btn" data-bs-toggle="tab" data-bs-target="#tab-td" type="button">
                📞 Sổ Trao Đổi TT (SP.01-QTQL.SH.16)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-tc-btn" data-bs-toggle="tab" data-bs-target="#tab-tc" type="button">
                🚫 Sổ Từ Chối Mẫu (SP.02-QTQL.SH.35)
            </button>
        </li>
        {% if session.get('role') == 'admin' %}
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="tab-users-btn" data-bs-toggle="tab" data-bs-target="#tab-users" type="button">
                👥 Quản Lý Thành Viên & Mật Khẩu
            </button>
        </li>
        {% endif %}
    </ul>

    <div class="tab-content" id="labTabsContent">
        <!-- TAB 1: CẢNH BÁO -->
        <div class="tab-pane fade show active" id="tab-cb" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-danger mb-3">➕ Thêm Báo Cáo KQ Cảnh Báo</h6>
                        <form method="POST" action="/add_canh_bao">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ báo cáo</label>
                                    <div class="input-group input-group-sm">
                                        <input type="text" name="ngay_gio" id="cb_ngay_gio" class="form-control auto-time-input" value="{{ now_str }}" required>
                                        <button class="btn btn-outline-secondary btn-set-now" type="button" title="Lấy giờ hiện tại của máy tính" onclick="setNowInput('cb_ngay_gio')">
                                            <i class="bi bi-clock-history"></i>
                                        </button>
                                    </div>
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
                        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Danh Sách Kết Quả Cảnh Báo ({{ canh_bao_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2 flex-wrap">
                                <button class="btn btn-danger btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#exportWordModalCB">
                                    <i class="bi bi-file-earmark-word me-1"></i>Xuất Word
                                </button>
                                {% if session.get('role') == 'admin' %}
                                <a href="/download_template/canh_bao" class="btn btn-outline-secondary btn-sm fw-bold">
                                    <i class="bi bi-file-earmark-arrow-down me-1"></i>Mẫu Excel
                                </a>
                                <button class="btn btn-outline-primary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#importModalCB">
                                    <i class="bi bi-file-earmark-arrow-up me-1"></i>Nạp Excel
                                </button>
                                {% endif %}
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
                        <h6 class="fw-bold text-primary mb-3">➕ Thêm Nhật Ký Trao Đổi</h6>
                        <form method="POST" action="/add_trao_doi">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Ngày/Giờ</label>
                                    <div class="input-group input-group-sm">
                                        <input type="text" name="ngay_gio" id="td_ngay_gio" class="form-control auto-time-input" value="{{ now_str }}" required>
                                        <button class="btn btn-outline-secondary btn-set-now" type="button" title="Lấy giờ hiện tại của máy tính" onclick="setNowInput('td_ngay_gio')">
                                            <i class="bi bi-clock-history"></i>
                                        </button>
                                    </div>
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
                                <input type="text" name="yeu_cau" class="form-control form-control-sm" placeholder="VD: Lấy lại mẫu...">
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
                        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Nhật Ký Trao Đổi Thông Tin ({{ trao_doi_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2 flex-wrap">
                                <button class="btn btn-primary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#exportWordModalTD">
                                    <i class="bi bi-file-earmark-word me-1"></i>Xuất Word
                                </button>
                                {% if session.get('role') == 'admin' %}
                                <a href="/download_template/trao_doi" class="btn btn-outline-secondary btn-sm fw-bold">
                                    <i class="bi bi-file-earmark-arrow-down me-1"></i>Mẫu Excel
                                </a>
                                <button class="btn btn-outline-primary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#importModalTD">
                                    <i class="bi bi-file-earmark-arrow-up me-1"></i>Nạp Excel
                                </button>
                                {% endif %}
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

        <!-- TAB 3: TỪ CHỐI MẪU -->
        <div class="tab-pane fade" id="tab-tc" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-warning text-dark mb-3">➕ Thêm Bản Ghi Từ Chối Mẫu</h6>
                        <form method="POST" action="/add_tu_choi">
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label small fw-bold">Thời gian</label>
                                    <div class="input-group input-group-sm">
                                        <input type="text" name="thoi_gian" id="tc_thoi_gian" class="form-control auto-time-input" value="{{ now_str }}" required>
                                        <button class="btn btn-outline-secondary btn-set-now" type="button" title="Lấy giờ hiện tại của máy tính" onclick="setNowInput('tc_thoi_gian')">
                                            <i class="bi bi-clock-history"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="col-5">
                                    <label class="form-label small fw-bold">Khoa/Phòng</label>
                                    <input type="text" name="khoa" class="form-control form-control-sm" placeholder="VD: C1-3" required>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Họ và tên bệnh nhân</label>
                                <input type="text" name="ten_benh_nhan" class="form-control form-control-sm" required>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Giới tính</label>
                                    <select name="gioi_tinh" class="form-select form-select-sm">
                                        <option value="Nam">Nam</option>
                                        <option value="Nữ">Nữ</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Năm sinh</label>
                                    <input type="text" name="nam_sinh" class="form-control form-control-sm" placeholder="VD: 1985">
                                </div>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Lý do mẫu không đạt</label>
                                <textarea name="ly_do" class="form-control form-control-sm" rows="2" placeholder="VD: Mẫu tán huyết, sai tỷ lệ chống đông..." required></textarea>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small fw-bold">Cách xử lý</label>
                                <textarea name="cach_xu_ly" class="form-control form-control-sm" rows="2" placeholder="VD: Đã liên hệ khoa đề nghị lấy lại mẫu..."></textarea>
                            </div>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người nhận</label>
                                    <input type="text" name="nguoi_nhan" class="form-control form-control-sm" value="{{ session.get('full_name') }}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label small fw-bold">Người gửi</label>
                                    <input type="text" name="nguoi_gui" class="form-control form-control-sm" placeholder="Điều dưỡng gửi">
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Ghi chú</label>
                                <input type="text" name="ghi_chu" class="form-control form-control-sm">
                            </div>
                            <button type="submit" class="btn btn-warning w-100 fw-bold text-dark"><i class="bi bi-save me-1"></i>Lưu Bản Ghi Từ Chối Mẫu</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0">📜 Danh Sách Mẫu Bị Từ Chối ({{ tu_choi_list|length }} bản ghi)</h6>
                            <div class="d-flex gap-2 flex-wrap">
                                <button class="btn btn-warning text-dark btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#exportWordModalTC">
                                    <i class="bi bi-file-earmark-word me-1"></i>Xuất Word (SP.02-QTQL.SH.35)
                                </button>
                                {% if session.get('role') == 'admin' %}
                                <a href="/download_template/tu_choi" class="btn btn-outline-secondary btn-sm fw-bold">
                                    <i class="bi bi-file-earmark-arrow-down me-1"></i>Mẫu Excel
                                </a>
                                <button class="btn btn-outline-primary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#importModalTC">
                                    <i class="bi bi-file-earmark-arrow-up me-1"></i>Nạp Excel
                                </button>
                                {% endif %}
                                <a href="/export/tu_choi" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>CSV</a>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>TT</th>
                                        <th>Thời gian</th>
                                        <th>Họ tên bệnh nhân</th>
                                        <th>Năm sinh Nam</th>
                                        <th>Năm sinh Nữ</th>
                                        <th>Khoa/Phòng</th>
                                        <th>Lý do không đạt</th>
                                        <th>Cách xử lý</th>
                                        <th>Người nhận</th>
                                        <th>Người gửi</th>
                                        <th>Ghi chú</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in tu_choi_list %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td class="text-nowrap">{{ row.thoi_gian }}</td>
                                        <td class="fw-bold">{{ row.ten_benh_nhan }}</td>
                                        <td class="text-center">{{ row.nam_sinh_nam }}</td>
                                        <td class="text-center">{{ row.nam_sinh_nu }}</td>
                                        <td>{{ row.khoa }}</td>
                                        <td class="text-danger">{{ row.ly_do }}</td>
                                        <td>{{ row.cach_xu_ly }}</td>
                                        <td>{{ row.nguoi_nhan }}</td>
                                        <td>{{ row.nguoi_gui }}</td>
                                        <td>{{ row.ghi_chu }}</td>
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

        <!-- TAB 4: QUẢN LÝ THÀNH VIÊN (CHỈ ADMIN) -->
        {% if session.get('role') == 'admin' %}
        <div class="tab-pane fade" id="tab-users" role="tabpanel">
            <div class="row">
                <div class="col-lg-4 mb-3">
                    <div class="card p-3">
                        <h6 class="fw-bold text-success mb-3"><i class="bi bi-person-plus-fill me-1"></i>Tạo Tài Khoản Mới</h6>
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
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                            <h6 class="fw-bold mb-0"><i class="bi bi-people-fill me-1"></i>Danh Sách Thành Viên ({{ users_list|length }} người)</h6>
                            <div class="d-flex gap-2">
                                <a href="/download_template/users" class="btn btn-outline-secondary btn-sm fw-bold">
                                    <i class="bi bi-file-earmark-arrow-down me-1"></i>Mẫu Excel
                                </a>
                                <button class="btn btn-outline-success btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#importModalUsers">
                                    <i class="bi bi-file-earmark-arrow-up me-1"></i>Nạp Excel
                                </button>
                            </div>
                        </div>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm align-middle small">
                                <thead>
                                    <tr>
                                        <th>STT</th>
                                        <th>Họ và tên</th>
                                        <th>Tên đăng nhập</th>
                                        <th>Vai trò</th>
                                        <th class="text-center">Thao tác</th>
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
                                            <button class="btn btn-sm btn-outline-warning py-0 px-2" data-bs-toggle="modal" data-bs-target="#adminResetModal{{ u.id }}">
                                                <i class="bi bi-key-fill"></i> Đổi MK
                                            </button>
                                            {% if u.username != 'admin' and u.username != session.get('username') %}
                                            <a href="/delete_user/{{ u.id }}" class="btn btn-sm btn-outline-danger py-0 px-2 ms-1" onclick="return confirm('Bạn có chắc muốn xóa {{ u.username }}?');">
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
                                                        <button type="submit" class="btn btn-warning btn-sm fw-bold">Cập Nhật</button>
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
        {% endif %}
    </div>
</div>

<!-- Modal Xuất Word Sổ Cảnh Báo -->
<div class="modal fade" id="exportWordModalCB" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-danger text-white">
                <h6 class="modal-title fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word - Sổ Cảnh Báo (SP.01-QTQL.SH.37)</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="GET" action="/export_word/canh_bao">
                <div class="modal-body py-3">
                    <p class="small text-muted mb-3">Chọn khoảng thời gian (để trống nếu muốn xuất toàn bộ):</p>
                    <div class="row g-2 mb-2">
                        <div class="col-6">
                            <label class="form-label small fw-bold">Từ ngày</label>
                            <input type="date" name="from_date" class="form-control form-control-sm">
                        </div>
                        <div class="col-6">
                            <label class="form-label small fw-bold">Đến ngày</label>
                            <input type="date" name="to_date" class="form-control form-control-sm">
                        </div>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-danger btn-sm fw-bold"><i class="bi bi-download me-1"></i>Tải File Word</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modal Xuất Word Sổ Trao Đổi -->
<div class="modal fade" id="exportWordModalTD" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-primary text-white">
                <h6 class="modal-title fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word - Sổ Trao Đổi (SP.01-QTQL.SH.16)</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="GET" action="/export_word/trao_doi">
                <div class="modal-body py-3">
                    <p class="small text-muted mb-3">Chọn khoảng thời gian (để trống nếu muốn xuất toàn bộ):</p>
                    <div class="row g-2 mb-2">
                        <div class="col-6">
                            <label class="form-label small fw-bold">Từ ngày</label>
                            <input type="date" name="from_date" class="form-control form-control-sm">
                        </div>
                        <div class="col-6">
                            <label class="form-label small fw-bold">Đến ngày</label>
                            <input type="date" name="to_date" class="form-control form-control-sm">
                        </div>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-primary btn-sm fw-bold"><i class="bi bi-download me-1"></i>Tải File Word</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modal Xuất Word Sổ Từ Chối -->
<div class="modal fade" id="exportWordModalTC" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-warning text-dark">
                <h6 class="modal-title fw-bold"><i class="bi bi-file-earmark-word me-1"></i>Xuất Word - Sổ Từ Chối Mẫu (SP.02-QTQL.SH.35)</h6>
                <button type="button" class="btn-close py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="GET" action="/export_word/tu_choi">
                <div class="modal-body py-3">
                    <p class="small text-muted mb-3">Chọn khoảng thời gian (để trống nếu muốn xuất toàn bộ):</p>
                    <div class="row g-2 mb-2">
                        <div class="col-6">
                            <label class="form-label small fw-bold">Từ ngày</label>
                            <input type="date" name="from_date" class="form-control form-control-sm">
                        </div>
                        <div class="col-6">
                            <label class="form-label small fw-bold">Đến ngày</label>
                            <input type="date" name="to_date" class="form-control form-control-sm">
                        </div>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-warning btn-sm fw-bold text-dark"><i class="bi bi-download me-1"></i>Tải File Word</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modals Nạp Excel Admin -->
<div class="modal fade" id="importModalCB" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-danger text-white">
                <h6 class="modal-title fw-bold">Nạp Excel - Sổ Cảnh Báo</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="/import_data/canh_bao" enctype="multipart/form-data">
                <div class="modal-body py-3">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Chọn file Excel (.xlsx) hoặc file .csv</label>
                        <input type="file" name="file" class="form-control form-control-sm" accept=".xlsx, .xls, .csv" required>
                    </div>
                    <div class="form-check form-switch mb-2 p-2 bg-light rounded border">
                        <input class="form-check-input ms-0 me-2" type="checkbox" name="auto_sync" id="importSyncCB" checked>
                        <label class="form-check-label small fw-bold text-primary" for="importSyncCB">
                            ⚡ Tự động đồng bộ sang Sổ Trao Đổi Thông Tin
                        </label>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-danger btn-sm fw-bold">Nạp Dữ Liệu</button>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="modal fade" id="importModalTD" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-primary text-white">
                <h6 class="modal-title fw-bold">Nạp Excel - Sổ Trao Đổi</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="/import_data/trao_doi" enctype="multipart/form-data">
                <div class="modal-body py-3">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Chọn file Excel (.xlsx) hoặc file .csv</label>
                        <input type="file" name="file" class="form-control form-control-sm" accept=".xlsx, .xls, .csv" required>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-primary btn-sm fw-bold">Nạp Dữ Liệu</button>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="modal fade" id="importModalTC" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-warning text-dark">
                <h6 class="modal-title fw-bold">Nạp Excel - Sổ Từ Chối Mẫu</h6>
                <button type="button" class="btn-close py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="/import_data/tu_choi" enctype="multipart/form-data">
                <div class="modal-body py-3">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Chọn file Excel (.xlsx) hoặc file .csv</label>
                        <input type="file" name="file" class="form-control form-control-sm" accept=".xlsx, .xls, .csv" required>
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-warning btn-sm fw-bold text-dark">Nạp Dữ Liệu</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modal Nạp Excel Tài Khoản (Admin) -->
<div class="modal fade" id="importModalUsers" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header py-2 bg-success text-white">
                <h6 class="modal-title fw-bold"><i class="bi bi-file-earmark-arrow-up me-1"></i>Nạp Danh Sách Tài Khoản từ Excel</h6>
                <button type="button" class="btn-close btn-close-white py-2" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="/import_data/users" enctype="multipart/form-data">
                <div class="modal-body py-3">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Chọn file Excel (.xlsx) hoặc file .csv</label>
                        <input type="file" name="file" class="form-control form-control-sm" accept=".xlsx, .xls, .csv" required>
                    </div>
                    <div class="small text-muted mb-2">
                        • Các cột yêu cầu: <strong>Họ và tên, Tên đăng nhập (username), Mật khẩu, Vai trò (staff/admin)</strong><br>
                        • Mật khẩu sẽ tự động được mã hóa an toàn.<br>
                        • Nếu tên đăng nhập đã tồn tại, hệ thống sẽ tự động bỏ qua để tránh trùng lặp.
                    </div>
                    <div class="alert alert-light border small py-2 mb-0">
                        Chưa có file mẫu? Bấm <a href="/download_template/users" class="fw-bold text-success">Tải Mẫu Excel</a> để điền thông tin nhanh chóng.
                    </div>
                </div>
                <div class="modal-footer py-2">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Hủy</button>
                    <button type="submit" class="btn btn-success btn-sm fw-bold"><i class="bi bi-upload me-1"></i>Nạp Tài Khoản Ngay</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Modal đổi mật khẩu cá nhân -->
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
    // Hàm lấy ngày giờ thực tế của máy tính người dùng định dạng dd/mm/yyyy hh:mm
    function getCurrentDateTimeStr() {
        const now = new Date();
        const day = String(now.getDate()).padStart(2, '0');
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const year = now.getFullYear();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }

    // Hàm gắn giờ hiện tại vào ô input cụ thể khi bấm nút đồng hồ
    function setNowInput(inputId) {
        const el = document.getElementById(inputId);
        if (el) {
            el.value = getCurrentDateTimeStr();
        }
    }

    // Tự động kiểm tra và đồng bộ ngày giờ máy tính thực tế khi vừa tải trang
    document.addEventListener("DOMContentLoaded", function() {
        const timeInputs = document.querySelectorAll(".auto-time-input");
        const clientNow = getCurrentDateTimeStr();
        timeInputs.forEach(input => {
            // Cập nhật ngay giờ của máy tính thực tế
            input.value = clientNow;
        });
    });

    if (window.location.hash === '#tab-td') {
        new bootstrap.Tab(document.querySelector('#tab-td-btn')).show();
    } else if (window.location.hash === '#tab-tc') {
        new bootstrap.Tab(document.querySelector('#tab-tc-btn')).show();
    } else if (window.location.hash === '#tab-users' && document.querySelector('#tab-users-btn')) {
        new bootstrap.Tab(document.querySelector('#tab-users-btn')).show();
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

# ----------------- HÀM XUẤT WORD CHO 3 SỔ (KHÔI PHỤC NGƯỜI QUẢN LÝ SỔ + CỠ 18 BOLD) -----------------

def generate_word_canh_bao(rows, from_str="", to_str=""):
    template_path = "template_canh_bao.docx"
    doc = docx.Document(template_path) if os.path.exists(template_path) else None
    if not doc:
        return io.BytesIO()

    table = doc.tables[1]
    range_text = f"Từ ngày: {from_str}  Đến ngày: {to_str}" if from_str and to_str else (
        f"Từ ngày: {from_str}" if from_str else (
            f"Đến ngày: {to_str}" if to_str else "Từ ngày:……/……./20…  Đến ngày:…../…../20…"
        )
    )

    for p in doc.paragraphs:
        if "Từ ngày" in p.text:
            p.text = range_text
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(18)
                run.font.bold = True
                run.font.italic = False
        elif "Người quản lý sổ" in p.text:
            if not p.text.strip():
                p.text = "Người quản lý sổ:  CN. Phạm Minh Nhi"
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
                run.font.bold = False

    col_mapping = [
        "ngay_gio", "khoa", "nguoi_bao_cao", "nguoi_nhan",
        "ten_benh_nhan", "ma_benh_nhan", "noi_dung", "ket_qua", "ghi_chu"
    ]

    for idx, r in enumerate(rows):
        target_row = table.rows[idx + 1] if idx + 1 < len(table.rows) else table.add_row()
        vals = [str(idx + 1)] + [r[k] if r[k] is not None else "" for k in col_mapping]
        for c_idx, val in enumerate(vals):
            cell = target_row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            if c_idx in [0, 1, 2, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)
                if c_idx == 8:
                    run.bold = True

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def generate_word_trao_doi(rows, from_str="", to_str=""):
    template_path = "template_trao_doi.docx"
    doc = docx.Document(template_path) if os.path.exists(template_path) else None
    if not doc:
        return io.BytesIO()

    table = doc.tables[1]
    range_text = f"Từ ngày: {from_str}  Đến ngày: {to_str}" if from_str and to_str else (
        f"Từ ngày: {from_str}" if from_str else (
            f"Đến ngày: {to_str}" if to_str else "Từ ngày …../…../20… đến ngày …../…../20…"
        )
    )

    if len(doc.tables) > 0:
        cell_t0 = doc.tables[0].rows[1].cells[0]
        for p in cell_t0.paragraphs:
            if "Từ ngày" in p.text:
                p.text = range_text
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(18)
                    run.font.bold = True
                    run.font.italic = False
            elif "Người quản lý sổ" in p.text:
                if not p.text.strip():
                    p.text = "Người quản lý sổ: ……………………………."
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(12)
                    run.font.bold = False

    col_mapping = [
        "ngay_gio", "nguoi_goi", "nguoi_nghe", "ten_benh_nhan",
        "khoa", "noi_dung", "yeu_cau", "ket_qua", "ghi_chu"
    ]

    for idx, r in enumerate(rows):
        target_row = table.rows[idx + 1] if idx + 1 < len(table.rows) else table.add_row()
        vals = [r[k] if r[k] is not None else "" for k in col_mapping]
        for c_idx, val in enumerate(vals):
            cell = target_row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            if c_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def generate_word_tu_choi(rows, from_str="", to_str=""):
    template_path = "template_tu_choi.docx"
    doc = docx.Document(template_path) if os.path.exists(template_path) else None
    if not doc:
        return io.BytesIO()

    range_text = f"Từ ngày: {from_str}  Đến ngày: {to_str}" if from_str and to_str else (
        f"Từ ngày: {from_str}" if from_str else (
            f"Đến ngày: {to_str}" if to_str else "Từ ngày …../…../20… đến ngày …../…../20…"
        )
    )
    
    if len(doc.tables) > 0:
        cell_t0 = doc.tables[0].rows[1].cells[0]
        for p in cell_t0.paragraphs:
            if "Từ ngày" in p.text:
                p.text = range_text
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(18)
                    run.font.bold = True
                    run.font.italic = False
            elif "Người quản lý sổ" in p.text:
                if not p.text.strip():
                    p.text = "Người quản lý sổ: ……………………………."
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(12)
                    run.font.bold = False

    table = doc.tables[1]
    col_mapping = [
        "thoi_gian", "ten_benh_nhan", "nam_sinh_nam", "nam_sinh_nu",
        "khoa", "ly_do", "cach_xu_ly", "nguoi_nhan", "nguoi_gui", "ghi_chu"
    ]

    for idx, r in enumerate(rows):
        target_row = table.rows[idx + 2] if idx + 2 < len(table.rows) else table.add_row()
        vals = [str(idx + 1)] + [r[k] if r[k] is not None else "" for k in col_mapping]
        for c_idx, val in enumerate(vals):
            cell = target_row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            if c_idx in [0, 1, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ----------------- TẠO BIỂU MẪU EXCEL ADMIN -----------------

def make_excel_template(book_type):
    wb = openpyxl.Workbook()
    ws = wb.active
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Times New Roman", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Times New Roman", size=11)
    thin_border = Border(
        left=Side(style='thin', color='BFBFBF'),
        right=Side(style='thin', color='BFBFBF'),
        top=Side(style='thin', color='BFBFBF'),
        bottom=Side(style='thin', color='BFBFBF')
    )

    now_sample = get_now_vn().replace(tzinfo=None)

    if book_type == "canh_bao":
        ws.title = "Mau_Nhap_Canh_Bao"
        headers = [
            "Ngày/giờ báo cáo", "Khoa", "Người báo cáo", "Người nhận báo cáo",
            "Tên bệnh nhân", "Mã số bệnh nhân", "Nội dung trao đổi", "Kết quả báo cáo", "Ghi chú"
        ]
        sample = [
            now_sample, "HSCC", "KTV Hải", "BS Minh",
            "NGUYỄN VĂN A", "24001234", "Báo động đỏ điện giải", "K+ 7.2 mmol/L", "Khoa đã tiếp nhận"
        ]
    elif book_type == "trao_doi":
        ws.title = "Mau_Nhap_Trao_Doi"
        headers = [
            "Ngày/giờ", "Người gọi", "Người nghe", "Họ tên bệnh nhân",
            "Khoa", "Nội dung trao đổi", "Yêu cầu", "Kết quả trao đổi", "Ghi chú"
        ]
        sample = [
            now_sample, "KTV Hải", "ĐD Lan", "TRẦN THỊ B",
            "C1-3", "Mẫu vỡ hồng cầu", "Đề nghị lấy lại mẫu", "Đã đồng ý gửi lại", "Mẫu máu tĩnh mạch"
        ]
    elif book_type == "tu_choi":
        ws.title = "Mau_Nhap_Tu_Choi_Mau"
        headers = [
            "Thời gian", "Họ và tên bệnh nhân", "Năm sinh Nam", "Năm sinh Nữ",
            "Khoa/Phòng", "Lý do mẫu không đạt", "Cách xử lý", "Người nhận", "Người gửi", "Ghi chú"
        ]
        sample = [
            now_sample, "NGUYỄN VĂN A", "1980", "",
            "C1-3", "Mẫu vỡ hồng cầu", "Báo khoa lấy lại mẫu", "KTV Hải", "ĐD Lan", "Lấy lại tube Heparin"
        ]
    else:  # book_type == "users"
        ws.title = "Mau_Nhap_Tai_Khoan"
        headers = ["Họ và tên", "Tên đăng nhập (username)", "Mật khẩu", "Vai trò (staff/admin)"]
        sample = ["CN. Nguyễn Văn A", "nguyenvana", "123456", "staff"]

    ws.append(headers)
    ws.append(sample)
    if book_type == "users":
        ws.append(["KTV. Trần Thị B", "tranthib", "123456", "staff"])

    for col_idx in range(1, len(headers) + 1):
        h_cell = ws.cell(row=1, column=col_idx)
        h_cell.fill = header_fill
        h_cell.font = header_font
        h_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        h_cell.border = thin_border

        for r_idx in range(2, len(ws["A"]) + 1):
            d_cell = ws.cell(row=r_idx, column=col_idx)
            d_cell.font = data_font
            d_cell.alignment = Alignment(vertical="center")
            d_cell.border = thin_border
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = 26

    # Cột 1 là ngày giờ định dạng dd/mm/yy hh:mm:ss cho 3 sổ xét nghiệm
    if book_type != "users":
        for r in range(2, 201):
            cell_dt = ws.cell(row=r, column=1)
            cell_dt.number_format = 'dd/mm/yy hh:mm:ss'
            cell_dt.alignment = Alignment(horizontal="center", vertical="center")

    buf = io.BytesIO()
    wb.save(buf)
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
    now_str = get_now_vn().strftime("%d/%m/%Y %H:%M")
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao ORDER BY id DESC").fetchall()
        td = conn.execute("SELECT * FROM trao_doi ORDER BY id DESC").fetchall()
        tc = conn.execute("SELECT * FROM tu_choi ORDER BY id DESC").fetchall()
        users = conn.execute("SELECT id, username, full_name, role FROM users ORDER BY id ASC").fetchall()
    return render_template_string(MAIN_TEMPLATE, now_str=now_str, canh_bao_list=cb, trao_doi_list=td, tu_choi_list=tc, users_list=users)

@app.route("/add_canh_bao", methods=["POST"])
@login_required
def add_canh_bao():
    ngay_gio = request.form.get("ngay_gio") or get_now_vn().strftime("%d/%m/%Y %H:%M")
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
                conn, cb["ngay_gio"], cb["nguoi_bao_cao"], cb["nguoi_nhan"],
                cb["ten_benh_nhan"], cb["khoa"], cb["ket_qua"], cb["noi_dung"], cb["ghi_chu"]
            )
            flash(f"✅ Đã đồng bộ bản ghi BN {cb['ten_benh_nhan']} sang Sổ Trao Đổi!", "info")
    return redirect(url_for("index") + "#tab-td")

@app.route("/add_trao_doi", methods=["POST"])
@login_required
def add_trao_doi():
    ngay_gio = request.form.get("ngay_gio") or get_now_vn().strftime("%d/%m/%Y %H:%M")
    with get_db() as conn:
        conn.execute("""
            INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ngay_gio, request.form.get("nguoi_goi"), request.form.get("nguoi_nghe"),
            request.form.get("ten_benh_nhan"), request.form.get("khoa"), request.form.get("noi_dung"),
            request.form.get("yeu_cau"), request.form.get("ket_qua"), request.form.get("ghi_chu")
        ))
        flash("✅ Đã lưu cuộc trao đổi thông tin thành công!", "success")
    return redirect(url_for("index") + "#tab-td")

@app.route("/add_tu_choi", methods=["POST"])
@login_required
def add_tu_choi():
    thoi_gian = request.form.get("thoi_gian") or get_now_vn().strftime("%d/%m/%Y %H:%M")
    ten_benh_nhan = request.form.get("ten_benh_nhan")
    gioi_tinh = request.form.get("gioi_tinh", "Nam")
    nam_sinh = request.form.get("nam_sinh", "").strip()
    nam_sinh_nam = nam_sinh if gioi_tinh == "Nam" else ""
    nam_sinh_nu = nam_sinh if gioi_tinh == "Nữ" else ""
    khoa = request.form.get("khoa")
    ly_do = request.form.get("ly_do")
    cach_xu_ly = request.form.get("cach_xu_ly")
    nguoi_nhan = request.form.get("nguoi_nhan")
    nguoi_gui = request.form.get("nguoi_gui")
    ghi_chu = request.form.get("ghi_chu")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO tu_choi (thoi_gian, ten_benh_nhan, nam_sinh_nam, nam_sinh_nu, khoa, ly_do, cach_xu_ly, nguoi_nhan, nguoi_gui, ghi_chu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (thoi_gian, ten_benh_nhan, nam_sinh_nam, nam_sinh_nu, khoa, ly_do, cach_xu_ly, nguoi_nhan, nguoi_gui, ghi_chu))
        flash("✅ Đã lưu bản ghi từ chối mẫu thành công!", "success")
    return redirect(url_for("index") + "#tab-tc")

# ----------------- QUẢN LÝ TÀI KHOẢN (CHỈ ADMIN) -----------------

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
    except (sqlite3.IntegrityError, PGIntegrityError):
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
@admin_required
def reset_user_password():
    target_id = request.form.get("user_id")
    new_pwd = request.form.get("new_password", "").strip()

    if len(new_pwd) < 6:
        flash("Mật khẩu mới phải có ít nhất 6 ký tự!", "danger")
        return redirect(url_for("index"))

    new_hash = generate_password_hash(new_pwd)
    with get_db() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, target_id))
        user = conn.execute("SELECT full_name FROM users WHERE id = ?", (target_id,)).fetchone()
        name = user["full_name"] if user else "thành viên"
        flash(f"✅ Đã cập nhật mật khẩu mới cho {name}!", "success")

    return redirect(url_for("index"))

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

# ----------------- TẢI MẪU & NẠP DỮ LIỆU EXCEL (CHỈ ADMIN) -----------------

@app.route("/download_template/<book_type>")
@login_required
@admin_required
def download_template(book_type):
    buf = make_excel_template(book_type)
    if book_type == "canh_bao":
        name = "Mau_Nhap_So_Canh_Bao_SP01_QTQL_SH_37.xlsx"
    elif book_type == "trao_doi":
        name = "Mau_Nhap_So_Trao_Doi_SP01_QTQL_SH_16.xlsx"
    elif book_type == "tu_choi":
        name = "Mau_Nhap_So_Tu_Choi_Mau_SP02_QTQL_SH_35.xlsx"
    else:
        name = "Mau_Nhap_Tai_Khoan.xlsx"

    return send_file(
        buf,
        as_attachment=True,
        download_name=name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/import_data/<book_type>", methods=["POST"])
@login_required
@admin_required
def import_data(book_type):
    if "file" not in request.files:
        flash("Vui lòng chọn file dữ liệu để nạp!", "danger")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("Chưa chọn file!", "danger")
        return redirect(url_for("index"))

    auto_sync = request.form.get("auto_sync")
    filename = secure_filename(file.filename).lower()

    try:
        df = pd.read_csv(file) if filename.endswith(".csv") else pd.read_excel(file)
        imported_count = 0
        skipped_count = 0

        with get_db() as conn:
            if book_type == "users":
                for _, row in df.iterrows():
                    vals = list(row.values)[:4]
                    while len(vals) < 4:
                        vals.append("")
                    full_name, username, pwd, role = [str(v).strip() for v in vals]
                    username = username.lower()
                    if not username or not full_name:
                        continue
                    if len(pwd) < 6:
                        pwd = "123456"
                    role = "admin" if role.lower() == "admin" else "staff"
                    
                    pwd_hash = generate_password_hash(pwd)
                    try:
                        conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                                     (username, pwd_hash, full_name, role))
                        imported_count += 1
                    except (sqlite3.IntegrityError, PGIntegrityError):
                        skipped_count += 1
                
                msg = f"🎉 Đã nạp thành công {imported_count} tài khoản mới!"
                if skipped_count > 0:
                    msg += f" (Đã bỏ qua {skipped_count} tài khoản do trùng tên đăng nhập)"
                flash(msg, "success")
                return redirect(url_for("index") + "#tab-users")

            elif book_type == "canh_bao":
                for _, row in df.iterrows():
                    vals = list(row.values)[:9]
                    while len(vals) < 9:
                        vals.append("")
                    ngay_gio, khoa, nguoi_bc, nguoi_nhan, ten_bn, ma_bn, noi_dung, ket_qua, ghi_chu = [format_cell_value(v) for v in vals]
                    if not ngay_gio and not ten_bn:
                        continue
                    conn.execute("""
                        INSERT INTO canh_bao (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_benh_nhan, ma_benh_nhan, noi_dung, ket_qua, ghi_chu)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (ngay_gio, khoa, nguoi_bao_cao, nguoi_nhan, ten_bn, ma_bn, noi_dung, ket_qua, ghi_chu))

                    if auto_sync:
                        sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bc, nguoi_nhan, ten_bn, khoa, ket_qua, noi_dung, ghi_chu)
                    imported_count += 1
            elif book_type == "trao_doi":
                for _, row in df.iterrows():
                    vals = list(row.values)[:9]
                    while len(vals) < 9:
                        vals.append("")
                    ngay_gio, nguoi_goi, nguoi_nghe, ten_bn, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu = [format_cell_value(v) for v in vals]
                    if not ngay_gio and not noi_dung:
                        continue
                    conn.execute("""
                        INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (ngay_gio, nguoi_goi, nguoi_nghe, ten_bn, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu))
                    imported_count += 1
            else:
                for _, row in df.iterrows():
                    vals = list(row.values)[:10]
                    while len(vals) < 10:
                        vals.append("")
                    thoi_gian, ten_bn, nam_nam, nam_nu, khoa, ly_do, cach_xl, nguoi_nhan, nguoi_gui, ghi_chu = [format_cell_value(v) for v in vals]
                    if not thoi_gian and not ten_bn:
                        continue
                    conn.execute("""
                        INSERT INTO tu_choi (thoi_gian, ten_benh_nhan, nam_sinh_nam, nam_sinh_nu, khoa, ly_do, cach_xu_ly, nguoi_nhan, nguoi_gui, ghi_chu)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (thoi_gian, ten_bn, nam_nam, nam_nu, khoa, ly_do, cach_xl, nguoi_nhan, nguoi_gui, ghi_chu))
                    imported_count += 1

        flash(f"🎉 Đã nạp thành công {imported_count} bản ghi từ file vào hệ thống!", "success")
    except Exception as e:
        flash(f"Lỗi khi đọc file nạp dữ liệu: {str(e)}", "danger")

    tab_map = {"canh_bao": "#tab-cb", "trao_doi": "#tab-td", "tu_choi": "#tab-tc"}
    return redirect(url_for("index") + tab_map.get(book_type, ""))

# ----------------- XUẤT WORD & CSV -----------------

@app.route("/export_word/<book_type>")
@login_required
def export_word(book_type):
    from_date = request.args.get("from_date", "").strip()
    to_date = request.args.get("to_date", "").strip()

    from_str = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d/%m/%Y") if from_date else ""
    to_str = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d/%m/%Y") if to_date else ""

    with get_db() as conn:
        if book_type == "canh_bao":
            all_rows = conn.execute("SELECT * FROM canh_bao ORDER BY id ASC").fetchall()
            rows = filter_records_by_date(all_rows, from_date, to_date, "ngay_gio")
            buf = generate_word_canh_bao(rows, from_str, to_str)
            filename = f"SP.01-QTQL.SH.37-So_theo_doi_bao_cao_KQ_canh_bao_{get_now_vn().strftime('%Y%m%d')}.docx"
        elif book_type == "trao_doi":
            all_rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            rows = filter_records_by_date(all_rows, from_date, to_date, "ngay_gio")
            buf = generate_word_trao_doi(rows, from_str, to_str)
            filename = f"SP.01-QTQL.SH.16-So_trao_doi_thong_tin_{get_now_vn().strftime('%Y%m%d')}.docx"
        else:
            all_rows = conn.execute("SELECT * FROM tu_choi ORDER BY id ASC").fetchall()
            rows = filter_records_by_date(all_rows, from_date, to_date, "thoi_gian")
            buf = generate_word_tu_choi(rows, from_str, to_str)
            filename = f"SP.02-QTQL.SH.35-So_tu_choi_mau_{get_now_vn().strftime('%Y%m%d')}.docx"

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
            filename = f"So_Canh_Bao_SP01_QTQL_SH_37_{get_now_vn().strftime('%Y%m%d')}.csv"
        elif book_type == "trao_doi":
            writer.writerow(["STT", "Ngày/Giờ", "Người gọi", "Người nghe", "Tên bệnh nhân", "Khoa", "Nội dung trao đổi", "Yêu cầu", "Kết quả trao đổi", "Ghi chú"])
            rows = conn.execute("SELECT * FROM trao_doi ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["ngay_gio"], r["nguoi_goi"], r["nguoi_nghe"], r["ten_benh_nhan"], r["khoa"], r["noi_dung"], r["yeu_cau"], r["ket_qua"], r["ghi_chu"]])
            filename = f"So_Trao_Doi_SP01_QTQL_SH_16_{get_now_vn().strftime('%Y%m%d')}.csv"
        else:
            writer.writerow(["TT", "Thời gian", "Họ và tên bệnh nhân", "Năm sinh Nam", "Năm sinh Nữ", "Khoa/Phòng", "Lý do mẫu không đạt", "Cách xử lý", "Người nhận", "Người gửi", "Ghi chú"])
            rows = conn.execute("SELECT * FROM tu_choi ORDER BY id ASC").fetchall()
            for idx, r in enumerate(rows, 1):
                writer.writerow([idx, r["thoi_gian"], r["ten_benh_nhan"], r["nam_sinh_nam"], r["nam_sinh_nu"], r["khoa"], r["ly_do"], r["cach_xu_ly"], r["nguoi_nhan"], r["nguoi_gui"], r["ghi_chu"]])
            filename = f"So_Tu_Choi_Mau_SP02_QTQL_SH_35_{get_now_vn().strftime('%Y%m%d')}.csv"

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
