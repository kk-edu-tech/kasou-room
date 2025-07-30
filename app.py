from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import time
import random

app = Flask(__name__)

# 初期状態
queue_number = 20000
last_updated = time.time()
start_time = datetime.now().strftime('%H:%M')
final_updated_time = None  # ← 0人になったときの時刻を記録
last_status_time = start_time

@app.route('/')
def waiting_room():
    global queue_number, last_updated, final_updated_time

    now = time.time()
    elapsed = now - last_updated

    if queue_number > 0 and elapsed >= 60:
      
        decrease_count = int(elapsed // 60)
        for _ in range(decrease_count):
            if queue_number <= 0:
                break
            queue_number = max(queue_number - random.randint(580, 620), 0)
        last_updated += decrease_count * 60
        last_status_time = datetime.now().strftime('%H:%M')

        # 0になった瞬間の時刻を記録（1回だけ）
        if queue_number == 0 and final_updated_time is None:
            final_updated_time = last_status_time

    # 表示する最終更新時刻
    if queue_number == 0 and final_updated_time:
        last_updated_time = final_updated_time
    else:
        last_updated_time = datetime.now().strftime('%H:%M')

    return render_template(
        'waiting_room.html',
        queue_number=queue_number,
        last_updated_time=last_updated_time,
        start_time=start_time
    )

@app.route('/reset')
def reset():
    global queue_number, last_updated, start_time, final_updated_time, last_status_time
    queue_number = 20000
    last_updated = time.time()
    start_time = datetime.now().strftime('%H:%M')
    final_updated_time = None  # ← ここもリセット
    last_status_time = start_time
    return redirect(url_for('waiting_room'))

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
