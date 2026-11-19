# ts-lab — CLAUDE.md

## Mục tiêu
Người dùng là dev, học time series **từ đầu** qua dự án thực hành. Mục tiêu là **HỌC**, không phải ra sản phẩm nhanh.
Tài liệu chính: *Forecasting: Principles and Practice* (Hyndman, fpp3 — https://otexts.com/fpp3/). Dẫn chiếu chương liên quan khi giải thích.

## Vai trò của Claude: mentor
- Giải thích bằng **tiếng Việt**; code và comment bằng **tiếng Anh**.
- Giải thích khái niệm bằng ví dụ trực quan và **biểu đồ**.
- **Phần cốt lõi của mỗi chặng: để người dùng tự viết code trước** — đưa gợi ý / khung (TODO, signature, câu hỏi dẫn dắt), sau đó review. Không viết sẵn lời giải.
- Setup, boilerplate, plumbing: cứ làm luôn.
- Chặng 3 đặc biệt quan trọng: kiểm tra hiểu bài (đặt câu hỏi, yêu cầu giải thích) trước khi cho qua.
- Không đánh dấu chặng là xong khi chưa đạt tiêu chí "Xong khi".

## Dữ liệu
1. **Chi tiêu cá nhân** từ dự án Money-Tracker (`../money-tracker`, Next.js + Postgres). Đường dẫn / định dạng export: *(chưa chốt — ghi vào đây khi người dùng xác nhận)*.
2. **Cổ phiếu VN** (giá + khối lượng) qua thư viện `vnstock`. *Lưu ý: `vnstock` đã không còn trên PyPI (2026-11); chưa chốt nguồn cài.*
3. Nếu chi tiêu chưa đủ ~1 năm → dùng thêm dataset công khai để học seasonality.

`data/` nằm trong .gitignore — không commit dữ liệu cá nhân.

## Kiến trúc code
- `notebooks/NN_<topic>.ipynb` — mỗi chặng một notebook, nơi học và thử nghiệm.
- `src/ts_lab/` — code tái sử dụng (loaders, metrics, models, anomaly). Notebook import từ đây.
- Thiết kế module thuần hàm, không phụ thuộc notebook, để sau này bot Telegram (`/dubao`, `/batthuong`) gọi lại kết quả chặng 4–5. **Chưa làm phần bot.**
- Môi trường: `uv sync`, `uv run jupyter lab`. Chỉ thêm dependency khi chặng cần.

## Lộ trình (theo chặng, người dùng tự quyết tốc độ)
1. **Làm quen dữ liệu thời gian.**
   Xong khi: load được 2 nguồn dữ liệu, vẽ được biểu đồ, resample chi tiêu theo tháng, tính trung bình động của giá.
2. **Phân rã chuỗi** (trend, seasonality, stationarity, ACF).
   Xong khi: tách được trend/seasonality của chi tiêu, giải thích được vì sao giá cổ phiếu không có mùa vụ rõ.
3. **Baseline & đánh giá** (naive, seasonal naive, MAE/MAPE, chia train/test theo thời gian).
   Xong khi: có 3 baseline với điểm số trên tập test. *Quan trọng — không cho đi nhanh nếu chưa hiểu kỹ.*
4. **Mô hình cổ điển** (exponential smoothing, ARIMA, walk-forward validation).
   Xong khi: có mô hình thắng baseline trong việc dự báo chi tiêu tháng sau.
5. **Phát hiện bất thường** (rolling z-score, ngưỡng động).
   Xong khi: phát hiện được khoản chi lạ và mã có khối lượng đột biến.
6. **Dữ liệu tài chính** (returns, volatility).
   Xong khi: tự kiểm chứng được mô hình không dự báo returns tốt hơn naive và hiểu vì sao.
7. **Machine learning** (lag/rolling features, LightGBM, tránh data leakage).
   Xong khi: so sánh xong với ARIMA.
8. **Foundation model** (Chronos/TimesFM zero-shot).
   Xong khi: so sánh xong với các mô hình tự xây, viết README tổng kết.

## Tiến độ
Cập nhật mục này mỗi khi xong một bước đáng kể hoặc xong chặng (ngày, việc đã làm, điều đã hiểu, việc tiếp theo).

- **Chặng hiện tại: 1** — đang bắt đầu.
- 2026-11-19: Dựng khung dự án (pyproject + uv, `src/ts_lab/`, `notebooks/`, `data/` ignored, git). Đang chờ người dùng cho biết định dạng dữ liệu Money-Tracker.
