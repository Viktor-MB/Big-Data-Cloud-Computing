# Catálogo de Produtos e Categorias

Este repositório contém o código-fonte de um sistema de catálogo de produtos, desenvolvido com Django e hospedado na AWS.

## 👥 Integrantes do Grupo
* **Tiago Macedo**
* **Viktor Mayer**
* **Luca Confente**

## 🔗 Links do Projeto
* **Deploy (AWS Elastic Beanstalk):** [Acessar ao Projeto](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/)
* **API Publicada:** [Acessar à API](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/api/)

## 📖 Guia de Utilização da API (Etapas de Implementação)

Para garantir o funcionamento correto dos dados, é necessário seguir a ordem lógica de cadastro devido ao relacionamento de dependência entre as entidades:

1. **Adicionar Categorias:** Antes de criar qualquer produto, deve popular as categorias.
   * Acesse: [Endpoint de Categorias](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/api/categorias/)
2. **Criar Produtos:** Com as categorias criadas, poderá associar cada produto a uma categoria existente.
   * Acesse: [Endpoint de Produtos](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/api/produtos/)

## 🛠️ Alterações e Funcionalidades Implementadas

Nesta versão do projeto, foram realizadas as seguintes melhorias técnicas:

1.  **Relacionamento Categoria-Produto:** Criação da classe `Categoria` e implementação de um relacionamento de chave estrangeira (One-to-Many). Agora, cada produto pertence obrigatoriamente a uma categoria (ex: um "Telefone" vinculado à categoria "Eletrónicos").
2.  **Comando de Gestão na Nuvem:** Desenvolvimento de um comando personalizado para permitir a execução e gestão do painel administrativo (`admin`) diretamente através da infraestrutura de nuvem da AWS.

## 🚀 Como Configurar e Executar Localmente

Siga as instruções abaixo para configurar o ambiente de desenvolvimento:

### Pré-requisitos
* Python 3.x instalado.
* Ambiente virtual configurado (`venv`).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd <nome-do-diretorio>
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare o Banco de Dados:**
    Gere os ficheiros de migração e aplique-os ao banco de dados:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Inicie o servidor de desenvolvimento:**
    Utilize o comando:
    ```bash
    python manage.py runserver
    ```

A aplicação estará disponível localmente em `http://127.0.0.1:8000/`.
