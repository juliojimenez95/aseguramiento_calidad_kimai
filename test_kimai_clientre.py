import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import uuid



# URL base del sistema Kimai
BASE_URL = "http://localhost:8001"
LOGIN_PATH = "/es/login" 
# La ruta de destino después del login es típicamente el timesheet.
POST_LOGIN_BASE_PATH = "/es/timesheet/" 
# Ruta de la lista de clientes (destino después de crear un cliente)
CUSTOMER_LIST_PATH = "/es/admin/customer/"

# Credenciales de prueba VÁLIDAS
TEST_USERNAME = "admin@example.com"
TEST_PASSWORD = "TallerCalidad2025"

# Selectores de Login
SELECTOR_USERNAME = "username" 
SELECTOR_PASSWORD = "password"
SELECTOR_SUBMIT_BUTTON = 'button[type="submit"]'
SELECTOR_SUCCESS_MESSAGE = '.alert-success' 

# Selectores de Administración y Clientes
# Selector del botón principal "Administración" (para desplegar el menú)
BUTTON_ADMIN_MENU_TOGGLE = 'a.navbar-menu-admin[data-bs-toggle="dropdown"]' 
# Selector de enlace en el submenú para ir a la lista de clientes
MENU_ADMIN_CUSTOMERS_LINK = 'a.navbar-menu-customers[href*="/customer/"]' 
# Selector del botón de "Crear nuevo cliente"
BUTTON_CREATE_CUSTOMER = 'a[href*="/customer/create"]' 

# ** IDs generados por Symfony para los campos **
FIELD_CUSTOMER_NAME = 'customer_edit_form_name' 
FIELD_CUSTOMER_HOMEPAGE = 'customer_edit_form_homepage'
BUTTON_SAVE = 'button[type="submit"]'


class KimaiCustomerFlowTest(unittest.TestCase):
    """
    Caso de prueba funcional enfocado en la creación de un Cliente en Kimai (hasta paso 5).
    """

    def setUp(self):
        """Prepara el entorno de Selenium para usar Firefox antes de cada prueba."""
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless") # Descomentar para ejecución sin interfaz gráfica
        options.add_argument("--start-maximized")
        
        try:
            self.driver = webdriver.Firefox(options=options)
            self.driver.implicitly_wait(15) 
        except Exception as e:
            self.fail(f"Fallo al inicializar WebDriver para Firefox. Asegúrate de que 'geckodriver' esté instalado y accesible en tu PATH. Error: {e}")


    def _login(self, username, password):
        """Función auxiliar para realizar el proceso de login."""
        driver = self.driver
        full_url = f"{BASE_URL}{LOGIN_PATH}"
        driver.get(full_url)
        
        # Esperar a que el campo de usuario esté visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, SELECTOR_USERNAME))
        )
        
        # Llenar el formulario y enviar
        driver.find_element(By.ID, SELECTOR_USERNAME).send_keys(username)
        driver.find_element(By.ID, SELECTOR_PASSWORD).send_keys(password)
        driver.find_element(By.CSS_SELECTOR, SELECTOR_SUBMIT_BUTTON).click()


    def _navigate_to_customers_list(self):
        """
        Función auxiliar para navegar a la lista de clientes.
        Reutilizable para evitar duplicación de código.
        """
        # Esperar y hacer clic en el menú de Administración
        admin_menu_toggle = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, BUTTON_ADMIN_MENU_TOGGLE))
        )
        admin_menu_toggle.click()
        
        # CRÍTICO: Pausa corta para asegurar que el dropdown esté completamente desplegado
        time.sleep(0.5)
        
        # Esperar y hacer clic en el enlace de Clientes
        customer_menu_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, MENU_ADMIN_CUSTOMERS_LINK))
        )
        customer_menu_link.click()
        
        # Esperar a que la URL de la lista de clientes se cargue
        WebDriverWait(self.driver, 15).until(
            EC.url_contains(CUSTOMER_LIST_PATH)
        )


    def test_01_customer_create_flow(self):
        """
        CP-AUTO-03 & 04: Flujo de creación de cliente (solo hasta paso 5).
        """
        
        # Generar un nombre único para el cliente
        customer_name = f"Cliente QA - {uuid.uuid4().hex[:6]}"
        
        print(f"\n--- Ejecutando Flujo: Creación de Cliente ({customer_name}) ---")
        
        # 1. Login exitoso (Pre-requisito)
        self._login(TEST_USERNAME, TEST_PASSWORD)
        
        try:
            # 1.b. Verificación de éxito post-login: Esperamos a que el botón de Administración esté disponible.
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, BUTTON_ADMIN_MENU_TOGGLE))
            )
            
            # Verificación de la URL post-login (Debe contener /timesheet/)
            self.assertIn(POST_LOGIN_BASE_PATH, self.driver.current_url.lower(), 
                          "ERROR: La URL no es la página principal post-login (/timesheet/), el inicio de sesión pudo haber fallado.")
            
            print("Paso 1: Login Exitoso y página principal verificada (Botón Administración visible).")

            # 2 y 3. Navegar a la página de clientes (CP-AUTO-03: Navegación)
            self._navigate_to_customers_list()
            print("Pasos 2 y 3: Menú de Administración desplegado y navegación a la lista de Clientes exitosa.")

            # 4. Click en el botón de Crear Cliente
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, BUTTON_CREATE_CUSTOMER))
            ).click()
            print("Paso 4: Click en 'Crear Cliente'.")

            # 5. Llenar el formulario de creación y guardar (CP-AUTO-04: Creación)
            
            # Esperamos a que el campo principal (NAME) esté presente
            customer_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, FIELD_CUSTOMER_NAME))
            )

            customer_field.send_keys(customer_name)
            
            # Campo de Homepage (usando el ID corregido)
            self.driver.find_element(By.ID, FIELD_CUSTOMER_HOMEPAGE).send_keys("http://www.ejemplo-qa.com")
            
            # Botón de Guardar
            self.driver.find_element(By.CSS_SELECTOR, BUTTON_SAVE).click()
            print(f"Paso 5: Formulario llenado y enviado para '{customer_name}'.")
            
            # Esperar a que se complete la acción de guardado (redirección o mensaje de éxito)
            time.sleep(2)
            
            print("--- Flujo Completo hasta Paso 5: OK ---")

        except TimeoutException as e:
            self.fail(f"Resultado FINAL: Fallo en el flujo (Timeout). No se encontró el elemento a tiempo. URL actual: {self.driver.current_url}. Detalle: {e.msg}")
        except NoSuchElementException as e:
            self.fail(f"Resultado FINAL: Fallo en el flujo (Elemento no encontrado). Error: {e}")


    def tearDown(self):
        """Cierra el navegador después de cada prueba para asegurar el aislamiento."""
        if hasattr(self, 'driver'):
            # Pausa de 2 segundos para que puedas ver el resultado final si lo estás viendo en vivo
            time.sleep(2) 
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()