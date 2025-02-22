from decouple import config
from woocommerce import API

# Función para configurar la conexión con WooCommerce
def get_wcapi():
    wcapi = API(
        url=config("WOOCOMMERCE_URL"),
        consumer_key=config("WOOCOMMERCE_CONSUMER_KEY"),
        consumer_secret=config("WOOCOMMERCE_CONSUMER_SECRET"),
        version="wc/v3"
    )
    return wcapi

# Prueba de conexión
def test_connection():
    wcapi = get_wcapi()
    response = wcapi.get("products")  # Intenta obtener productos
    if response.status_code == 200:
        print("¡Conexión exitosa!")
    else:
        print(f"Error al conectar: {response.status_code}, {response.text}")
