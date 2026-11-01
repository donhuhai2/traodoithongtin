import sqlite3
import csv
import io
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, Response, flash

app = Flask(__name__)
app.secret_key = "lab_records_secret_bvqy175"
DB_NAME = "lab_records.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
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
init_db()
HTML_TEMPLATE = """
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
        .sync-badge { font-size: 0.8rem; background-color: #e7f5ff; color: #0c8599; padding: 3px 8px; border-radius: 4px; border: 1px solid #a5d8ff; }
    </style>
</head>
<body class="py-3">
<div class="container-fluid px-4">
    <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
        <div>
            <h4 class="text-primary fw-bold mb-1">🏥 HỆ THỐNG QUẢN LÝ SỔ ĐIỆN TỬ PHÒNG XÉT NGHIỆM</h4>
            <span class="text-muted small">Bệnh viện Quân y 175 — Tự động liên thông Sổ Cảnh Báo & Sổ Trao Đổi</span>
        </div>
        <div>
            <span class="badge bg-success fs-6"><i class="bi bi-check-circle me-1"></i>Đang chạy độc lập (Local)</span>
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
                                    <input type="text" name="nguoi_bao_cao" class="form-control form-control-sm" required>
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
                                <div class="text-muted" style="font-size: 0.72rem;">
                                    (Người BC ➔ Người gọi, Người nhận ➔ Người nghe, KQ cảnh báo ➔ Nội dung TĐ, Nội dung TĐ ➔ Yêu cầu, Ghi chú ➔ KQ trao đổi)
                                </div>
                            </div>

                            <button type="submit" class="btn btn-danger w-100 fw-bold"><i class="bi bi-save me-1"></i>Lưu Bản Ghi Cảnh Báo</button>
                        </form>
                    </div>
                </div>

                <div class="col-lg-8">
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="fw-bold mb-0">📜 Danh Sách Kết Quả Cảnh Báo ({{ canh_bao_list|length }} bản ghi)</h6>
                            <a href="/export/canh_bao" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>Xuất Excel/CSV</a>
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
                                            <a href="/sync_one/{{ row.id }}" class="btn btn-sm btn-outline-primary py-0 px-2" title="Đồng bộ thủ công bản ghi này sang Sổ trao đổi">
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
                                    <input type="text" name="nguoi_goi" class="form-control form-control-sm" required>
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
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="fw-bold mb-0">📜 Nhật Ký Trao Đổi Thông Tin ({{ trao_doi_list|length }} bản ghi)</h6>
                            <a href="/export/trao_doi" class="btn btn-outline-success btn-sm fw-bold"><i class="bi bi-file-earmark-excel me-1"></i>Xuất Excel/CSV</a>
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
    // Giữ trạng thái tab khi chuyển trang
    if (window.location.hash === '#tab-td') {
        const tabTrigger = new bootstrap.Tab(document.querySelector('#tab-td-btn'));
        tabTrigger.show();
    }
</script>
</body>
</html>
"""

def sync_canh_bao_to_trao_doi(conn, ngay_gio, nguoi_bc, nguoi_nhan, ten_bn, khoa, ket_qua_cb, noi_dung_cb, ghi_chu_cb):
    # Mapping theo đúng yêu cầu:
    # Người báo cáo --> người gọi
    # Người nhận --> người nghe
    # Tên bệnh nhân --> họ tên bệnh nhân
    # Khoa --> khoa
    # Kết quả cảnh báo --> nội dung trao đổi
    # Nội dung trao đổi --> yêu cầu
    # Ghi chú --> kết quả trao đổi
    conn.execute("""
        INSERT INTO trao_doi (ngay_gio, nguoi_goi, nguoi_nghe, ten_benh_nhan, khoa, noi_dung, yeu_cau, ket_qua, ghi_chu)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ngay_gio,
        nguoi_bc,
        nguoi_nhan,
        ten_bn,
        khoa,
        ket_qua_cb,    # KQ cảnh báo -> Nội dung trao đổi
        noi_dung_cb,   # Nội dung trao đổi -> Yêu cầu
        ghi_chu_cb,    # Ghi chú -> Kết quả trao đổi
        "Đồng bộ từ Sổ Cảnh Báo"  # Ghi chú sổ trao đổi
    ))

@app.route("/")
def index():
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_db() as conn:
        cb = conn.execute("SELECT * FROM canh_bao ORDER BY id DESC").fetchall()
        td = conn.execute("SELECT * FROM trao_doi ORDER BY id DESC").fetchall()
    return render_template_string(HTML_TEMPLATE, now_str=now_str, canh_bao_list=cb, trao_doi_list=td)

@app.route("/add_canh_bao", methods=["POST"])
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

@app.route("/export/<book_type>")
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
    app.run(host="127.0.0.1", port=5000, debug=False)
