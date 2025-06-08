from pathlib import Path

# Ruta del archivo .env
env_path = Path(".env")

# Verificar si ya existe
if env_path.exists():
    confirm = input(".env ya existe. ¿Deseas sobrescribirlo? (s/n): ")
    if confirm.lower() != "s":
        print("Cancelado.")
        exit()

# Variables de ejemplo para Transbank Sandbox
env_content = """
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False/True

# SECURITY TRANSBANK
TRANSBANK_COMMERCE_CODE=597055555532
TRANSBANK_API_KEY=XNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
TRANSBANK_ENVIRONMENT=sandbox
""".strip()

# Crear el archivo
with open(env_path, "w") as f:
    f.write(env_content)

print(".env creado exitosamente.")
