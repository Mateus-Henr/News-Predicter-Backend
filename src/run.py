import threading

from app import create_app
from watch.watch_news import watch

app = create_app()

if __name__ == '__main__':
    thread = threading.Thread(target=watch)
    thread.start()
    print("Thread started")
    app.run(host="0.0.0.0", port=5001)
