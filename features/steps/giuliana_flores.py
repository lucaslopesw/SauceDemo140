import random
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

url = "https://www.giulianaflores.com.br/"
cep= "02019-030"
celular= "11999999999"
cpf_valido = "948.826.832-88"
senha = "ASas!@12"
senha_invalida = "senha_errada"

def generate_cpf():                                                        
        cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                
        for _ in range(2):                                                          
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
            cpf.append(11 - val if val > 1 else 0)                                  
                                                                                
        return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)


@given(u'que acesso o site Giuliana Flores')
def step_impl(context):
    context.driver = webdriver.Firefox()
    context.driver.get(url)
    context.driver.maximize_window()


@when(u'faço o cadastro do usuário')
def step_impl(context):
    context.driver.implicitly_wait(1)
    cpf = generate_cpf()
    print(cpf)
    context.driver.find_element(By.ID, "perfil-display").click()
    context.driver.find_element(By.ID, "UrlLogin").click()

    context.driver.find_element(By.ID, "ContentSite_ibtNewCustomer").click()

    context.driver.find_element(By.ID, "ContentSite_txtName").send_keys("Teste Fulano")
    context.driver.find_element(By.CSS_SELECTOR, ".CadastroPF.CPF").send_keys(cpf)
    context.driver.find_element(By.ID, "ContentSite_txtEmail").send_keys("teste"+cpf+"@teste.com")
    context.driver.find_element(By.ID, "ContentSite_txtPasswordNew").send_keys(senha)
    context.driver.find_element(By.ID, "ContentSite_CustomerAddress_txtZip").send_keys(cep)
    context.driver.find_element(By.ID, "ContentSite_CustomerAddress_btnAddressFind").click()
    context.driver.find_element(By.ID, "ContentSite_CustomerAddress_txtAddressNumber").send_keys("100")
    context.driver.find_element(By.ID, "ContentSite_CustomerAddress_txtPhoneCelularNum").send_keys(celular)

    context.driver.find_element(By.ID, "ContentSite_btnCreateCustomer").click()

@then(u'o usuário é criado com sucesso')
def step_impl(context):
    context.driver.implicitly_wait(1)
    context.driver.find_element(By.ID, "perfil-display").click()
    assert "Teste" in context.driver.find_element(By.ID, "lblWelcome").text
    context.driver.quit()

@when(u'faço o login com credenciais válidas')
def step_impl(context):
    context.driver.implicitly_wait(1)
    context.driver.find_element(By.ID, "perfil-display").click()
    context.driver.find_element(By.ID, "UrlLogin").click()

    context.driver.find_element(By.ID, "ContentSite_txtEmail").send_keys(cpf_valido)
    context.driver.find_element(By.ID, "ContentSite_txtPassword").send_keys(senha)
    context.driver.find_element(By.ID, "ContentSite_ibtContinue").click()


@then(u'o usuário é autenticado com sucesso')
def step_impl(context):
    context.driver.implicitly_wait(1)
    context.driver.find_element(By.ID, "perfil-display").click()
    assert "Teste" in context.driver.find_element(By.ID, "lblWelcome").text
    context.driver.quit()

@when(u'faço o login com credenciais inválidas')
def step_impl(context):
    context.driver.implicitly_wait(1)
    context.driver.find_element(By.ID, "perfil-display").click()
    context.driver.find_element(By.ID, "UrlLogin").click()

    context.driver.find_element(By.ID, "ContentSite_txtEmail").send_keys(cpf_valido)
    context.driver.find_element(By.ID, "ContentSite_txtPassword").send_keys(senha_invalida)
    context.driver.find_element(By.ID, "ContentSite_ibtContinue").click()


@then(u'o sistema apresenta mensagem de erro')
def step_impl(context):
    context.driver.implicitly_wait(1)
    assert context.driver.find_element(By.CSS_SELECTOR, ".aviso-erro").text == "ATENÇÃO - e-mail ou senha inválidos!"
    context.driver.quit()

@when(u'adiciono o produto ao carrinho de compras')
def step_impl(context):
    context.driver.implicitly_wait(1)
    context.driver.find_element(By.CSS_SELECTOR, ".list-carousel:nth-child(1)").click()
    global preço
    preço= context.driver.find_element(By.CSS_SELECTOR, ".precoPor_prod").text
    global nome
    nome= context.driver.find_element(By.CSS_SELECTOR,"span[itemprop='name']:nth-child(2)").text
    context.driver.find_element(By.ID, "ContentSite_txtZip").send_keys(cep)
    context.driver.find_element(By.ID, "ContentSite_lbtBuy").click()
    try:
        WebDriverWait(context.driver, 10).until(EC.alert_is_present())
        alert = context.driver.switch_to.alert
        alert.dismiss()
    except  TimeoutException:
        print("No alert present")

    context.driver.find_element(By.ID,"btConfirmShippingData").click()
    
    


@when(u'finalizo a compra')
def step_impl(context):
    context.driver.implicitly_wait(1)
    context.driver.find_element(By.ID, "ContentSite_lbtBuy").click()


@then(u'o sistema apresenta mensagem de sucesso')
def step_impl(context):
    context.driver.implicitly_wait(1)
    assert context.driver.find_element(By.CSS_SELECTOR, ".prodBasket_nome").text.lower() in nome.lower()
    assert context.driver.find_element(By.CSS_SELECTOR, ".precoPor_basket").text in preço
    context.driver.find_element(By.CSS_SELECTOR, ".prodBasket_remover").click()
    context.driver.quit()