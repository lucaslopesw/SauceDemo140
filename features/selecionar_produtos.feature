Feature: Selecionar Produto

    Scenario: Selecionar produto "Sauce Labs Backpack"
        Given que acesso o site Sauce Demo
        When preencho os campos de login com usuario standard_user e senha secret_sauce
        Then sou direcionado para página home
        
    Scenario: Login com a senha invalida
        Given que acesso o site Sauce Demo
        When preencho os campos de login com usuario standard_user e senha senha_invalida
        Then exibe a mensagem de erro no login

    Scenario Outline: Login Negativo
        Given que acesso o site Sauce Demo
        When preencho os campos de login com usuario <usuario> e senha <senha>
        Then exibe a <mensagem> de erro no login

        Examples:
            | id  | usuario        | senha         | mensagem                                                                  |
            | 01  | standard_user  | laranja       | Epic sadface: Username and password do not match any user in this service |
            | 02  | standard_user  |               | Epic sadface: Password is required                                        |
            | 03  |                | secret_sauce  | Epic sadface: Username is required                                        |
            | 04  | juca           | secret_sauce  | Epic sadface: Username and password do not match any user in this service |
            | 05  | juca           | laranja       | Epic sadface: Username and password do not match any user in this service |
            | 06  | juca           |               | Epic sadface: Password is required                                        |
            | 07  |                |               | Epic sadface: Username is required                                        |
            | 08  |                | laranja       | Epic sadface: Username is required                                        |