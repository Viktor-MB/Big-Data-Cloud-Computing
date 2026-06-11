# Catálogo de Produtos — AP1 e AP2

## 👥 Integrantes do Grupo
* **Tiago Macedo**
* **Viktor Mayer**
* **Luca Confente**

---

# AP1: Catálogo de Produtos e Categorias

## 🔗 Links do Projeto (AP1)
* **Deploy (AWS Elastic Beanstalk):** [Acessar o Projeto](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/)
* **API Publicada:** [Acessar a API](http://catalogo-produtos-categoria-v1-admin.eba-2anaedvb.us-east-1.elasticbeanstalk.com/api/)

## 🔐 Credenciais de Acesso (Admin)
* **Username:** admin
* **Password:** 123456

## 🛠️ Funcionalidades Implementadas (AP1)

1. **Relacionamento Categoria-Produto:** Criação da classe `Categoria` com relacionamento de chave estrangeira (One-to-Many) com `Produto`. Cada produto pode ser associado a uma categoria (ex: "Telefone" → "Eletrônicos").
2. **API REST completa:** Endpoints para listagem, criação, edição e remoção de categorias e produtos.
3. **Deploy no Elastic Beanstalk:** Aplicação publicada na AWS com servidor Gunicorn e proxy Nginx.

## 🚀 Como Executar Localmente (AP1)

```bash
git clone <url-do-repositorio>
cd AP1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000/`.

---

# AP2: Evolução para Arquitetura em Nuvem (PostgreSQL RDS + AWS S3)

## 🔗 Links do Projeto (AP2)
* **Deploy da API (Produção):** [http://luca.us-east-1.elasticbeanstalk.com/api/](http://luca.us-east-1.elasticbeanstalk.com/api/)
* **Painel Administrativo:** [http://luca.us-east-1.elasticbeanstalk.com/admin/](http://luca.us-east-1.elasticbeanstalk.com/admin/)

## 🔐 Credenciais de Acesso (Admin AP2)
* **Username:** root
* **Password:** root1234

## 🏗️ Arquitetura da Solução (AP1 → AP2)

```
AP1                          AP2
─────────────────────        ──────────────────────────────────
SQLite (local/efêmero)  →    AWS RDS PostgreSQL (gerenciado)
Disco da instância EB   →    AWS S3 (imagens dos produtos)
Senha hardcoded         →    Variáveis de ambiente no EB
Sem carrinho            →    Pedido + ItemPedido (e-commerce)
```

| Componente | AP1 | AP2 |
|---|---|---|
| Banco de dados | SQLite (arquivo local) | PostgreSQL no AWS RDS |
| Armazenamento de mídia | Disco da instância (efêmero) | Bucket AWS S3 |
| Carrinho de compras | Não tinha | Pedido + ItemPedido |
| Atributos variáveis | Não tinha | JSONField (JSONB no PostgreSQL) |
| Credenciais | Fixas no código | Variáveis de ambiente |

## 📸 Evidências de Nuvem (Obrigatório)

### Console AWS RDS (Instância Ativa)
Instância `catalogo-db` com engine **PostgreSQL**, status **Available**, região `us-east-1`, tamanho `db.t4g.micro`.

![RDS Console](evidencias/rds-instancia-ativa.png)

### Console AWS S3 (Mídia Enviada)
Bucket `catalogo-imagens-viktor` com a pasta `produtos/` criada automaticamente após o primeiro upload de imagem via Django Admin.

![S3 Console](evidencias/s3-bucket-produtos.png)

### Acesso ao Django Admin (Root Logado)
Painel administrativo acessível com usuário **root**, exibindo todos os models registrados: Categorias, Produtos, Pedidos e Item Pedidos. Ações recentes mostram dados criados no RDS.

![Django Admin Dashboard](evidencias/admin-dashboard-root.png)

![Django Admin Adicionar Produto](evidencias/admin-adicionar-produto.png)

### API /api/produtos/ retornando 200 com imagem no S3
`GET /api/produtos/` retorna HTTP 200. O campo `imagem` aponta para a URL do S3 (`https://catalogo-imagens-viktor.s3.amazonaws.com/produtos/...`), confirmando que o upload persiste no bucket e não no disco da instância.

![API Produtos 200](evidencias/api-produtos-200-s3.png)

## 📓 Documentação Técnica (AP2)

### Etapas Realizadas

1. **Configuração do AWS RDS PostgreSQL:** Criação de instância PostgreSQL gerenciada (`catalogo-db`), configuração de Security Group para liberar a porta 5432 às instâncias do Elastic Beanstalk, e criação manual do banco `catalogo_db` via `psql`.

2. **Criação do Bucket S3:** Criação de bucket para armazenamento das imagens dos produtos. Integração via `django-storages` + `boto3`, com credenciais lidas de variáveis de ambiente do EB (`AWS_STORAGE_BUCKET_NAME`).

3. **Atualização do `settings.py` para Django 6:** As configurações `DEFAULT_FILE_STORAGE` e `STATICFILES_STORAGE` foram removidas no Django 5.1+. A migração foi feita para o dicionário `STORAGES`, que seleciona automaticamente o S3 quando `AWS_STORAGE_BUCKET_NAME` está definido e o disco local em desenvolvimento.

4. **Evolução do modelo de dados:** Adição das classes `Pedido` e `ItemPedido` para suporte a carrinho de compras, com endpoints REST completos (`/api/pedidos/`). Adição de `JSONField` (`atributos`) em `Produto` para metadados dinâmicos persistidos como JSONB no PostgreSQL.

5. **Correção do `django.config`:** Os `container_commands` do Elastic Beanstalk não ativam a virtualenv automaticamente. Todos os comandos foram corrigidos com `source /var/app/venv/*/bin/activate &&` para usar o Python correto. Adição do comando `03_createsuperuser` para criar o usuário `root` automaticamente no primeiro deploy.

6. **Deploy no Elastic Beanstalk:** Variáveis de ambiente configuradas no painel do EB (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `AWS_STORAGE_BUCKET_NAME`). Deploy realizado via `app.zip` gerado pelo script `build_zip.py`.

### Principais Decisões Técnicas

* **Variáveis de ambiente para todos os segredos:** `DB_HOST`, `DB_PASSWORD` e `AWS_STORAGE_BUCKET_NAME` nunca aparecem no código — são lidas via `os.getenv()`. Isso evita expor credenciais no repositório público.

* **`STORAGES` condicional:** O backend de storage é decidido em tempo de execução. Se `AWS_STORAGE_BUCKET_NAME` estiver vazio (desenvolvimento local), usa `FileSystemStorage`. Se estiver preenchido (produção no EB), usa `S3Boto3Storage`. Isso permite que o projeto rode localmente sem precisar de credenciais AWS.

* **SQLite local / PostgreSQL na nuvem:** O mesmo padrão se aplica ao banco: se `DB_HOST` não estiver definido, Django usa SQLite. Isso elimina a necessidade de instalar PostgreSQL para rodar o projeto localmente.

* **`JSONField` (JSONB) para atributos variáveis:** Produtos de categorias diferentes têm atributos distintos (eletrônico tem `ram_gb`, roupa tem `cor`, etc.). Em vez de criar tabelas separadas ou dezenas de colunas opcionais, usamos um `JSONField` que persiste como JSONB no PostgreSQL — permitindo consultas eficientes diretamente dentro do JSON.

* **`leader_only: true` nos container_commands:** Garante que `migrate` e `createsuperuser` rodam em apenas uma instância quando há múltiplas no Auto Scaling, evitando conflitos de migração concorrente.

### Dificuldades e Soluções

* **Dificuldade 1:** `01_migrate` falhava no deploy com `Command failed` sem mensagem clara.
  * **Solução:** O `cfn-init-cmd.log` (não o `eb-engine.log`) continha o traceback real. Os `container_commands` do EB não ativam a venv automaticamente — o `python` disponível no PATH é o do sistema (sem Django instalado). A correção foi prefixar cada comando com `source /var/app/venv/*/bin/activate &&`.

* **Dificuldade 2:** Mesmo com a venv ativada, o `migrate` continuava falhando: `FATAL: database "catalogo_db" does not exist`.
  * **Solução:** Ao criar a instância RDS, o PostgreSQL cria apenas o banco inicial definido na configuração (geralmente `postgres`). O banco `catalogo_db` precisou ser criado manualmente com `psql -h <host> -U postgres -d postgres -c "CREATE DATABASE catalogo_db;"` via AWS CloudShell.

* **Dificuldade 3:** Upload de imagens ia para o disco local em vez do S3, mesmo com `django-storages` instalado.
  * **Solução:** No Django 6.0, as configurações `DEFAULT_FILE_STORAGE` e `STATICFILES_STORAGE` foram removidas e são silenciosamente ignoradas. A configuração correta passou a ser o dicionário `STORAGES = {'default': {'BACKEND': '...'}, 'staticfiles': {'BACKEND': '...'}}`.

## ⚙️ Passo a Passo para Execução Local (AP2)

### Pré-requisitos
* Python 3.10+ instalado
* Ambiente virtual (`venv`) criado e ativado

### Passos

```bash
# 1. Clone e entre na pasta
git clone <url-do-repositorio>
cd AP1

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute as migrações (usa SQLite automaticamente sem DB_HOST)
python manage.py migrate

# 4. Crie um superusuário local (opcional)
python manage.py createsuperuser

# 5. Inicie o servidor
python manage.py runserver
```

A API estará em `http://127.0.0.1:8000/api/` e o admin em `http://127.0.0.1:8000/admin/`.

### Para usar PostgreSQL e S3 localmente

Defina as variáveis de ambiente antes de rodar:

```bash
export DB_HOST=<host-do-rds>
export DB_NAME=catalogo_db
export DB_USER=postgres
export DB_PASSWORD=<senha>
export AWS_STORAGE_BUCKET_NAME=<nome-do-bucket>
```

## 🚀 Passo a Passo de Deploy

```bash
# 1. Gere o pacote de deploy
cd AP1
python build_zip.py        # gera app.zip

# 2. Faça o deploy (requer EB CLI configurado)
eb deploy

# Ou suba o app.zip manualmente pelo console:
# Elastic Beanstalk → seu ambiente → Upload and deploy → selecionar app.zip
```

**Variáveis de ambiente obrigatórias no EB** (Configuration → Software → Environment properties):

| Variável | Descrição |
|---|---|
| `DB_HOST` | Endpoint do RDS (ex: `catalogo-db.xxxxx.us-east-1.rds.amazonaws.com`) |
| `DB_NAME` | Nome do banco (`catalogo_db`) |
| `DB_USER` | Usuário do PostgreSQL |
| `DB_PASSWORD` | Senha do PostgreSQL |
| `AWS_STORAGE_BUCKET_NAME` | Nome do bucket S3 para mídia |
| `DJANGO_SUPERUSER_PASSWORD` | Senha do admin `root` (opcional, padrão: `root1234`) |

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/` | Raiz da API (DRF browsable) |
| GET/POST | `/api/categorias/` | Listar e criar categorias |
| GET/POST | `/api/produtos/` | Listar e criar produtos |
| GET/PUT/DELETE | `/api/produtos/{id}/` | Detalhe, edição e remoção |
| GET | `/api/produtos/?search=nome` | Busca por nome/descrição |
| GET | `/api/produtos/?categoria=eletronicos` | Filtro por categoria |
| GET | `/api/produtos/?marca=Dell` | Filtro por atributo JSON |
| GET | `/api/produtos/?cor=preto` | Filtro por atributo JSON |
| GET | `/api/produtos/?ram_gb=16` | Filtro por atributo JSON |
| GET | `/api/produtos/por-atributo/?chave=cpu&valor=i7` | Filtro genérico por JSON |
| GET/POST | `/api/pedidos/` | Listar e criar pedidos |
| POST | `/api/pedidos/{id}/adicionar-item/` | Adicionar item ao pedido |

## 🗃️ Quando usar campo relacional vs JSONField

| Situação | Usar |
|---|---|
| Atributo presente em **todos** os produtos (nome, preço, categoria) | Campo relacional (coluna dedicada) |
| Atributo presente só em **alguns** produtos (marca, RAM, cor, tamanho) | `JSONField` (JSONB) |
| Necessidade de **JOIN** com outras tabelas | Campo relacional com FK |
| Metadados variáveis por tipo de produto, sem schema fixo | `JSONField` (JSONB) |

O `JSONField` no Django persiste como tipo `JSONB` no PostgreSQL, que armazena o JSON em formato binário indexável — permitindo consultas como `WHERE atributos->>'marca' = 'Dell'` com performance equivalente a colunas convencionais.

## 📋 Checklist de Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| `01_migrate failed` no deploy | venv não ativada no comando | Prefixar com `source /var/app/venv/*/bin/activate &&` |
| `FATAL: database "X" does not exist` | Banco não criado no RDS | `psql ... -c "CREATE DATABASE X;"` |
| Upload de imagem vai pro disco local | `DEFAULT_FILE_STORAGE` ignorado no Django 6+ | Usar `STORAGES = {'default': {'BACKEND': '...'}}` |
| `/api/produtos/` retorna 500 | Tabelas não existem (migrate não rodou) | Verificar `cfn-init-cmd.log`, não o `eb-engine.log` |
| Arquivos estáticos 404 (`/static/...`) | `collectstatic` não rodou | Verificar comando `02_collectstatic` no `django.config` |
