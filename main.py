import datetime

def say_hello():
    now = datetime.datetime.now()
    print(f"Salam, Burunc30! Bu kod {now.strftime('%Y-%m-%d %H:%M:%S')} tarixində işə düşdü.")

if __name__ == "__main__":
    say_hello()
