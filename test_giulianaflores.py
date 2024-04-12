# 1 - Bibliotecas
import random
import selenium
from selenium import webdriver
import selenium.webdriver
import selenium.webdriver.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep

# 2 - Classe (opcional)
class Teste_Produtos():
    # 2.1 Atributos
    url = "https://www.giulianaflores.com.br/"
    cep= "02019-030"
    celular= "11999999999"
    cpf_valido= "840.138.040-50"
    senha= "ASas!@12"
    senha_incorreta= "senha_errada"

    # 2.2 Funções e Métodos
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(20)
        self.driver.set_window_size(1920, 1080)

    def teardown_method(self, method):
        self.driver.get_screenshot_as_png()
        self.driver.quit()

    def generate_cpf(self):                                                        
        cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                
        for _ in range(2):                                                          
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
            cpf.append(11 - val if val > 1 else 0)                                  
                                                                                
        return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)

    def test_criar_usuario(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, "perfil-display").click()
        self.driver.find_element(By.ID, "UrlLogin").click()

        self.driver.find_element(By.CSS_SELECTOR, ".txt_newlogindir").click()
        assert  self.driver.find_element(By.CSS_SELECTOR, "h1").text == "MINHA CONTA"

        self.driver.find_element(By.ID, "ContentSite_txtName").send_keys("Teste Fulano")
        cpf= self.generate_cpf()
        self.driver.find_element(By.CSS_SELECTOR, ".CadastroPF.CPF").send_keys(cpf)
        self.driver.find_element(By.ID, "ContentSite_txtEmail").send_keys("teste"+cpf+"@teste.com")
        self.driver.find_element(By.ID, "ContentSite_txtPasswordNew").send_keys(self.senha)
        self.driver.find_element(By.ID, "ContentSite_CustomerAddress_txtZip").send_keys(self.cep)
        self.driver.find_element(By.ID, "ContentSite_CustomerAddress_btnAddressFind").click()
        self.driver.find_element(By.ID, "ContentSite_CustomerAddress_txtAddressNumber").send_keys("100")
        self.driver.find_element(By.ID, "ContentSite_CustomerAddress_txtPhoneCelularNum").send_keys(self.celular)

        self.driver.find_element(By.ID, "ContentSite_btnCreateCustomer").click()

        self.driver.find_element(By.ID, "perfil-display").click()
        assert "Teste" in self.driver.find_element(By.ID, "lblWelcome").text


    def test_login_positivo(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, "perfil-display").click()
        self.driver.find_element(By.ID, "UrlLogin").click()

        self.driver.find_element(By.ID, "ContentSite_txtEmail").send_keys(self.cpf_valido)
        self.driver.find_element(By.ID, "ContentSite_txtPassword").send_keys(self.senha)
        self.driver.find_element(By.ID, "ContentSite_ibtContinue").click()

        self.driver.find_element(By.ID, "perfil-display").click()
        assert "Teste" in self.driver.find_element(By.ID, "lblWelcome").text
    
    def test_login_negativo(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, "perfil-display").click()
        self.driver.find_element(By.ID, "UrlLogin").click()

        self.driver.find_element(By.ID, "ContentSite_txtEmail").send_keys(self.cpf_valido)
        self.driver.find_element(By.ID, "ContentSite_txtPassword").send_keys(self.senha_incorreta)
        self.driver.find_element(By.ID, "ContentSite_ibtContinue").click()

        aviso= self.driver.find_element(By.CSS_SELECTOR, ".aviso-erro")
        assert aviso.is_displayed()
        assert " e-mail ou senha inválidos!" in aviso.text

    def test_comprar_produto(self):
        self.driver.get(self.url)
        
        self.driver.find_element(By.CSS_SELECTOR, ".list-carousel:nth-child(1)").click()
        preço= self.driver.find_element(By.CSS_SELECTOR, ".precoPor_prod").text
        nome= self.driver.find_element(By.CSS_SELECTOR,"span[itemprop='name']:nth-child(2)").text
        self.driver.find_element(By.ID, "ContentSite_txtZip").send_keys(self.cep)

        self.driver.find_element(By.ID, "ContentSite_lbtBuy").click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID,"btConfirmShippingData"))).click()

        self.driver.find_element(By.ID, "ContentSite_lbtBuy").click()

        assert self.driver.find_element(By.CSS_SELECTOR, ".prodBasket_nome").text.lower() in nome.lower()
        assert self.driver.find_element(By.CSS_SELECTOR, ".precoPor_basket").text in preço

        self.driver.find_element(By.CSS_SELECTOR, ".prodBasket_remover").click()
