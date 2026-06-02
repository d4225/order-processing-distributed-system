import time
from celery import Celery
import psutil

# Kết nối tới cái giỏ trung tâm Redis
app = Celery('order_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task(bind=True)
def process_order_task(self, order_id, customer_name, items):
    print(f"[*] Hệ thống đã nhận đơn hàng: #{order_id} của khách {customer_name}")
    
    # 🚀 TÍNH NĂNG MỚI 1: TỰ ĐỘNG ĐIỀU TIẾT TẢI ĐỘNG (FAILOVER)
    # Nếu máy tính chạy Worker này đang bị quá tải CPU (>80%), nó từ chối xử lý và đẩy đơn hàng ngược lại Redis sau 4 giây để máy khác gánh hộ
    cpu_usage = psutil.cpu_percent()
    if cpu_usage > 80.0:
        print(f"[!] Cảnh báo: Máy quá tải ({cpu_usage}% CPU). Đẩy đơn hàng #{order_id} về lại hàng đợi...")
        raise self.retry(countdown=4)

    # --- Giả lập quy trình xử lý đơn hàng (Mất tổng cộng 2 giây) ---
    print(f"   -> [Bước 1/3] Đang kiểm tra số lượng tồn kho của: {items}")
    time.sleep(0.5)
    
    print(f"   -> [Bước 2/3] Đang kết nối ngân hàng để trừ tiền tài khoản...")
    time.sleep(1)
    
    print(f"   -> [Bước 3/3] Đang xuất hóa đơn điện tử cho khách...")
    time.sleep(0.5)
    
    print(f"[✓] XỬ LÝ THÀNH CÔNG ĐƠN HÀNG: #{order_id}")
    return f"Đơn hàng #{order_id} hoàn tất! Đóng gói tại trạm: localhost"