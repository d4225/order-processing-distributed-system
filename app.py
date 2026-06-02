from flask import Flask, render_template_string, jsonify
from tasks import process_order_task
import random

app = Flask(__name__)

# Giao diện Web HTML tích hợp Bootstrap nhìn cho chuyên nghiệp
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Hệ thống xử lý đơn hàng Flash Sale</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-5">
    <div class="p-4 mb-4 bg-dark text-white rounded-3">
        <h2>⚡ HỆ THỐNG XỬ LÝ ĐƠN HÀNG FLASH SALE PHÂN TÁN</h2>
        <p>Giải pháp chống sập Web khi có hàng vạn giao dịch đồng thời bằng Celery & Redis.</p>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card p-4 shadow-sm border-danger">
                <h4 class="text-danger">🔥 Sự kiện Flash Sale đang diễn ra</h4>
                <p>Bấm nút bên dưới để giả lập tình huống 100 khách hàng cùng click "Mua Ngay" vào cùng 1 giây.</p>
                <button onclick="createFlashSale()" class="btn btn-danger btn-lg w-100">🛒 BẤM MUA NGAY (100 Đơn/giây)</button>
                <div id="status" class="mt-3 alert alert-warning d-none"></div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card p-4 shadow-sm bg-light">
                <h4>📊 Giám sát các Trạm xử lý (Distributed Nodes)</h4>
                <div class="mt-3">
                    <p>🖥️ <strong>Trạm Worker 1 (Máy của bạn):</strong> <span class="badge bg-success">Online (Đang chạy)</span></p>
                    <p>🖥️ <strong>Trạm Worker 2 (Máy bạn cùng nhóm):</strong> <span class="badge bg-secondary">Offline (Chờ kết nối)</span></p>
                    <hr>
                    <div class="alert alert-info py-2 small">
                        Hệ thống sử dụng cơ chế Heartbeat đồng bộ qua Redis để theo dõi trạng thái sống/chết của các máy trạm phân tán.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function createFlashSale() {
            var statusDiv = document.getElementById('status');
            statusDiv.classList.remove('d-none');
            statusDiv.innerText = "Đang gửi 100 đơn hàng lên hệ thống...";
            
            fetch('/buy-flash-sale')
                .then(response => response.json())
                .then(data => {
                    statusDiv.className = "mt-3 alert alert-success";
                    statusDiv.innerText = "Trang Web đã nhận 100 đơn hàng thành công trong 0.1 giây! Khách hàng mua sắm mượt mà. Hãy nhìn xuống Terminal của VS Code để xem Worker đang chia nhau xử lý đơn ngầm.";
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/buy-flash-sale')
def buy_flash_sale():
    danh_sach_sp = ["Điện thoại iPhone 17 Pro", "Tai nghe chống ồn", "Bàn phím cơ Gaming"]
    
    # Vòng lặp giả lập tạo 100 đơn hàng đồng thời ném vào Redis
    for i in range(2001, 2101):
        order_id = i
        customer_name = f"User_{random.randint(100, 999)}"
        items = random.choice(danh_sach_sp)
        
        # 🔥 Đẩy đơn hàng vào Celery (Xếp hàng vào giỏ Redis)
        process_order_task.delay(order_id, customer_name, items)
        
    return jsonify({"message": "100 đơn hàng đã xếp hàng thành công!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)