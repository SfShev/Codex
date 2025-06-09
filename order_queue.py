import json
from pathlib import Path
from datetime import datetime

BUFFER_FILE = Path('buffer.json')


def load_buffer():
    if BUFFER_FILE.exists():
        with BUFFER_FILE.open('r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_buffer(data):
    with BUFFER_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_order(order: dict):
    buffer = load_buffer()
    order['created_at'] = datetime.utcnow().isoformat()
    order['status'] = 'В обработке'
    buffer.append(order)
    save_buffer(buffer)


def list_orders(user_id: int):
    buffer = load_buffer()
    return [o for o in buffer if o.get('user_id') == user_id]
