from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By 

url = "https://www.saucedemo.com"

@given(u'que acesso o site Sauce Demo')
def step_impl(context):
    context.driver = webdriver.Firefox()
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

    context.driver.quit()

@then(u'exibe a mensagem de erro no login')
def step_impl(context):
    assert context.driver.find_element(By.CSS_SELECTOR, "h3").text == "Epic sadface: Username and password do not match any user in this service"

    context.driver.quit()

#Verifica a mensagem para o Scenario Outline
@then(u'exibe a {mensagem} de erro no login')
def step_impl(context, mensagem):
    assert context.driver.find_element(By.CSS_SELECTOR, "h3").text == mensagem

    context.driver.quit()