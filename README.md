# AP1: Catálogo de Produtos e Categorias (Entrega AP1)

Este repositório contém o código-fonte de um sistema de catálogo de produtos, desenvolvido com Django e hospedado na AWS.

## 👥 Integrantes do Grupo
* **Tiago Macedo**
* **Viktor Mayer**
* **Luca Confente**

## 🔗 Links do Projeto
* **Deploy (AWS Elastic Beanstalk):** [Acessar ao Projeto](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/)
* **API Publicada:** [Acessar à API](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/api/)

## 🔐 Credenciais de Acesso (Admin)
Para realizar a gestão de dados através do painel administrativo ou endpoints protegidos:
* **Username:** admin
* **Password:** 123456

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

---

# AP2: Evolução da Arquitetura (PostgreSQL RDS + AWS S3)

Nesta etapa, o projeto evolui para uma arquitetura em nuvem mais próxima de produção, integrando banco de dados gerenciado e armazenamento de arquivos estáticos no ecossistema AWS.

## 🏗️ Arquitetura da Solução (AP1 -> AP2)
* **Banco de Dados:** Migração de SQLite (local) para **AWS RDS (PostgreSQL)**, garantindo persistência isolada da aplicação.
* **Armazenamento de Mídia:** Implementação do **AWS S3** para upload e armazenamento das imagens dos produtos.
* **Regras de Negócio:** Evolução do domínio para e-commerce com a adição de carrinho de compras (Pedido, Itens do Pedido).
* **Segurança:** Utilização de variáveis de ambiente para ocultar credenciais e chaves de acesso confidenciais.

## 🔗 Links do Projeto (AP2)
* **Deploy da API (Produção):** `[INSERIR LINK AQUI APÓS O DEPLOY DA AP2]`
* **Painel Administrativo (Django Admin):** `[INSERIR LINK DO ADMIN AQUI]`

## 📸 Evidências de Nuvem (Obrigatório)
* **Console AWS RDS (Instância Ativa):**
  > `[INSERIR PRINT AQUI]`
* **Console AWS S3 (Mídia Enviada):**
  > `[INSERIR PRINT AQUI]`
* **Requisição na API com Upload de Mídia:**
  > `[INSERIR PRINT DA REQUISIÇÃO (POSTMAN/INSOMNIA) AQUI]`
* **Acesso ao Django Admin (Root Logado):**
  > `[INSERIR PRINT AQUI]`

*(Caso opte por implementar a extensão do campo JSONB, inclua aqui os prints do registro salvo no banco e os resultados das consultas).*

## 📓 Documentação Técnica (AP2)

### Etapas Realizadas
1. `[Ex: Configuração de variáveis de ambiente para proteção de chaves da AWS e credenciais do RDS]`
2. `[Ex: Instalação das dependências psycopg2-binary e boto3]`
3. `[Ex: Criação da instância PostgreSQL no RDS e ajustes de Security Groups]`
4. `[Ex: Criação do Bucket S3, configuração de políticas de acesso público e CORS]`
5. `[Ex: Deploy atualizado no Elastic Beanstalk]`

### Principais Decisões Técnicas
* `[Descrever brevemente o porquê das escolhas de configuração feitas pela equipe, ex: isolamento de credenciais via variáveis de ambiente para maior segurança.]`

### Dificuldades e Soluções
* **Dificuldade 1:** `[Qual foi o erro? Ex: Timeout de conexão no RDS durante as migrações]`
  * **Solução:** `[Como resolveram? Ex: Liberação de Inbound Rules para a porta 5432 no Security Group do banco de dados]`
* **Dificuldade 2:** `[Outro erro de permissão do S3 ou deploy no Elastic Beanstalk]`
  * **Solução:** `[Solução técnica aplicada]`

## ⚙️ Passo a Passo para Execução Local (Versão AP2)

1. Instale as novas dependências do projeto:
   ```bash
   pip install -r requirements.txt