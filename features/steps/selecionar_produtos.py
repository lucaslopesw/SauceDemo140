from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By 

url = "https://www.saucedemo.com"

@given(u'que acesso o site Sauce Demo')
def step_impl(context):
    context.driver = webdriver.Firefox()
    context.driver.maximize_window()
    context.driver.get("https://www.saucedemo.com")

@when(u'preencho os campos de login com usuario {usuario} e senha {senha}')
def step_impl(context, usuario, senha):
    context.driver.find_element(By.ID, "user-name").send_keys(usuario)
    context.driver.find_element(By.ID, "password").send_keys(senha)
    context.driver.find_element(By.CSS_SELECTOR, "input.submit-button.btn_action").click()

@then(u'sou direcionado para página home')
def step_impl(context):
    assert context.driver.find_element(By.CSS_SELECTOR, ".title").text == "Products"

    context.driver.quit()