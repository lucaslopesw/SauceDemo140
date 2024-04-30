from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
import time

url = "https://www.saucedemo.com"
preco_produto = ""

@given(u'que acesso o site Sauce Demo')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.get("https://www.saucedemo.com")

#Preencher com usuário e senha
@when(u'preencho os campos de login com usuario {usuario} e senha {senha}')
def step_impl(context, usuario, senha):
    context.driver.find_element(By.ID, "user-name").send_keys(usuario)
    context.driver.find_element(By.ID, "password").send_keys(senha)
    context.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()

#Preencher com usuário em branco e senha
@when(u'preencho os campos de login com usuario  e senha {senha}')
def step_impl(context, senha):
    context.driver.find_element(By.ID, "password").send_keys(senha)
    context.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()

#Preencher com usuário, mas deixar a senha em branco
@when(u'preencho os campos de login com usuario {usuario} e senha ')
def step_impl(context, usuario):
    context.driver.find_element(By.ID, "user-name").send_keys(usuario)
    context.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()

#Clica no botão de login sem ter preenchido o usuário e a senha
@when(u'preencho os campos de login com usuario  e senha ')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()

@then(u'sou direcionado para página home')
def step_impl(context):
    assert context.driver.find_element(By.CSS_SELECTOR, ".title").text == "Products"

@then(u'exibe a mensagem de erro no login')
def step_impl(context):
    assert context.driver.find_element(By.CSS_SELECTOR, "h3").text == "Epic sadface: Username and password do not match any user in this service"

    context.driver.quit()

#Verifica a mensagem para o Scenario Outline
@then(u'exibe a {mensagem} de erro no login')
def step_impl(context, mensagem):
    assert context.driver.find_element(By.CSS_SELECTOR, "h3").text == mensagem

    context.driver.quit()

#Preencher com usuário e senha através da decisão (IF)
@when(u'digito os campos de login com usuario {usuario} e senha {senha} com IF')
def step_impl(context, usuario, senha):
    if usuario != '<branco>':
        context.driver.find_element(By.ID, "user-name").send_keys(usuario)
    if senha != '<branco>':
        context.driver.find_element(By.ID, "password").send_keys(senha)
        
    context.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()

@when(u'adiciono o produto Sauce Labs Backpack ao carrinho')
def step_impl(context):
    global preco_produto
    global nome_produto
    preco_produto = context.driver.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) .inventory_item_price").text
    nome_produto = context.driver.find_element(By.CSS_SELECTOR, "#item_4_title_link .inventory_item_name").text

    print(preco_produto)
    context.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()



@then(u'o produto deverá aparecer no carrinho de compras')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
    assert  context.driver.find_element(By.CSS_SELECTOR, ".title").text == "Your Cart"
    assert  context.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text == nome_produto
    assert  context.driver.find_element(By.CSS_SELECTOR, ".inventory_item_price").text == preco_produto
    
    context.driver.find_element(By.ID, "remove-sauce-labs-backpack").click()  


@then(u'faço o logout')
def step_impl(context):
    context.driver.implicitly_wait(5)
    context.driver.find_element(By.ID, "react-burger-menu-btn").click()
    context.driver.find_element(By.ID, "logout_sidebar_link").click()
    assert  context.driver.find_element(By.CSS_SELECTOR, "input[data-test='login-button']").is_displayed()
    context.driver.quit()