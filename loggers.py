import datetime

def log_activity(func):
    def wrapper(*args, **kwargs):
        with open("logs.txt", "a") as f:
            f.write(f"\n[{datetime.datetime.now()}] FUNCTION CALLED: {func.__name__}")

        try:
            result = func(*args, **kwargs)

            with open("logs.txt", "a") as f:
                f.write(f" → SUCCESS")

            return result

        except Exception as e:
            with open("logs.txt", "a") as f:
                f.write(f" → ERROR: {str(e)}")

            raise e

    return wrapper