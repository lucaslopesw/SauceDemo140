Feature: Giuliana Flores
    Scenario: Criação de usuário
        Given que acesso o site Giuliana Flores
        When faço o cadastro do usuário
        Then o usuário é criado com sucesso

    Scenario: Login Positivo
        Given que acesso o site Giuliana Flores
        When faço o login com credenciais válidas
        Then o usuário é autenticado com sucesso
    
    Scenario: Login Negativo
        Given que acesso o site Giuliana Flores
        When faço o login com credenciais inválidas
        Then o sistema apresenta mensagem de erro
    
    Scenario: Comprar Produto
        Given que acesso o site Giuliana Flores
        When faço o login com credenciais válidas
        And adiciono o produto ao carrinho de compras
        And finalizo a compra
        Then o sistema apresenta mensagem de sucesso