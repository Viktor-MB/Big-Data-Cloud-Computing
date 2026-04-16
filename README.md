# Catálogo de Produtos e Categorias

Este repositório contém o código-fonte de um sistema de catálogo de produtos, desenvolvido com Django e hospedado na AWS.

## 👥 Integrantes do Grupo
* **Tiago Macedo**
* **Viktor Mayer**
* **Luca Confente**

## 🔗 Links do Projeto
* **Deploy (AWS Elastic Beanstalk):** [assessar ao Projeto](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/)
* **API Publicada:** [Assessar à API](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/api/)

## 🛠️ Alterações e Funcionalidades Implementadas
Nesta versão do projeto, foram realizadas as seguintes melhorias técnicas:

1.  **Relacionamento Categoria-Produto:** Foi criada uma nova classe `Categoria`. Implementamos um relacionamento de chave estrangeira (One-to-Many) onde cada produto pertence obrigatoriamente a uma categoria.
    * *Exemplo:* Um produto do tipo "Telefone" está associado à categoria "Eletrónicos".
2.  **Comando de Gestão na Nuvem:** Desenvolvemos um comando personalizado para permitir a execução e gestão do painel administrativo (`admin`) diretamente através da infraestrutura de nuvem da AWS, facilitando a manutenção remota.

## 🚀 Como Configurar e Executar Localmente

Siga as instruções abaixo para configurar o ambiente de desenvolvimento:

### Pré-requisitos
* Python 3.12 instalado.
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

3.  **Execute as migrações (se aplicável):**
    ```bash
    python manage.py migrate
    ```

4.  **Inicie o servidor de desenvolvimento:**
    Para rodar o projeto localmente, utilize o seguinte comando:
    ```bash
    python manage.py runserver
    ```

A aplicação estará disponível no seu browser em `http://127.0.0.1:8000/`.
