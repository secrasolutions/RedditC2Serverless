# Reddit C2 Serverless - Shell Persistente

## Descripción

Este proyecto implementa un sistema de **Command and Control (C2) Serverless** utilizando Reddit como canal de comunicación. 

- **Serverless**: Sin infraestructura propia, utiliza Reddit como canal.
- **Cifrado XOR + Base64**: Comunicaciones obfuscadas.
- **Shell persistente**: Contexto mantenido entre comandos.
- **Evasión**:
  - User-Agent aleatorio.
  - Sleep aleatorio para evitar detección anti-bot.
  - Separadores invisibles para evitar bloqueos.

## Arquitectura

- 2 cuentas de Reddit:
  - **Controlador** publica comandos.
  - **Agente** monitoriza y responde.
- Subreddit privado como canal.
- Aplicaciones Reddit con API Keys para autenticación.

## Archivos

- `c2red.py`: Agente que ejecuta comandos en shell persistente.
- `c2redlistener.py`: Controlador que envía comandos y recibe respuestas.

## Requisitos

- Python 3.7+
- Librerías:
  - `praw`
  - `base64`
  - `random`, `re`, `subprocess`, `threading`

## Instalación

```bash
pip install praw
```

## Configuración

Editar credenciales en ambos scripts:

```python
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
```

## Uso

### 1. Ejecutar el agente

```bash
python c2red.py
```

### 2. Ejecutar el controlador

```bash
python reddit_c2_shell.py
```

### 3. Enviar comandos

```bash
> whoami
> uname -a
```

## Advertencia

Este proyecto es solo para **fines educativos**. No se promueve su uso malicioso ni incluye medidas de **seguridad operacional** avanzadas.

## Licencia

Secra Solutions S.L. 2025 
