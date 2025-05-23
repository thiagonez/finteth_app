# Ferramenta de Análise Financeira Pessoal

Este arquivo contém instruções para instalação, configuração e execução da ferramenta de análise financeira pessoal desenvolvida com Streamlit.

## Requisitos do Sistema

- Python 3.8 ou superior
- PostgreSQL (recomendado para ambiente de produção)
- Pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório ou extraia os arquivos para um diretório de sua preferência.

2. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto baseado no arquivo `.env.example`
   - Preencha as variáveis com suas configurações

## Configuração do Banco de Dados

1. Crie um banco de dados PostgreSQL:
   ```sql
   CREATE DATABASE fintech_app;
   ```

2. Configure a string de conexão no arquivo `.env`:
   ```
   DATABASE_URL=postgresql://usuario:senha@localhost/fintech_app
   ```

3. Execute as migrações do banco de dados (quando implementadas):
   ```bash
   python -m app.database.migrations
   ```

## Execução Local

Para executar a aplicação localmente:

```bash
streamlit run app/main.py
```

A aplicação estará disponível em `http://localhost:8501`.

## Implantação em Produção

### Opção 1: Streamlit Cloud

A maneira mais simples de implantar a aplicação é usando o [Streamlit Cloud](https://streamlit.io/cloud):

1. Crie uma conta no Streamlit Cloud
2. Conecte seu repositório GitHub
3. Selecione o repositório e o arquivo principal (`app/main.py`)
4. Configure as variáveis de ambiente secretas
5. Implante a aplicação

### Opção 2: Heroku

Para implantar no Heroku:

1. Crie uma conta no Heroku e instale a CLI
2. Crie um novo aplicativo:
   ```bash
   heroku create nome-do-app
   ```

3. Adicione o add-on do PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Configure as variáveis de ambiente:
   ```bash
   heroku config:set STRIPE_PUBLIC_KEY=sua_chave_publica
   heroku config:set STRIPE_SECRET_KEY=sua_chave_secreta
   heroku config:set GEMINI_API_KEY=sua_chave_api
   heroku config:set SECRET_KEY=sua_chave_secreta
   ```

5. Crie um arquivo `Procfile` na raiz do projeto:
   ```
   web: sh setup.sh && streamlit run app/main.py
   ```

6. Crie um arquivo `setup.sh` na raiz do projeto:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"seu-email@dominio.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS = false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

7. Implante a aplicação:
   ```bash
   git add .
   git commit -m "Configuração para Heroku"
   git push heroku main
   ```

### Opção 3: AWS, GCP ou Azure

Para ambientes de produção mais robustos, considere:

- AWS Elastic Beanstalk
- Google App Engine
- Azure App Service

Cada plataforma tem suas próprias instruções de implantação, mas geralmente envolvem:

1. Configurar um serviço de banco de dados gerenciado (RDS, Cloud SQL, etc.)
2. Configurar variáveis de ambiente
3. Implantar o código usando CLI ou integração contínua

## Estrutura do Projeto

```
fintech_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_processing.py
│   │   ├── file_import.py
│   │   └── visualization.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── financial.py
│   │   └── psychological.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   ├── questionnaire.py
│   │   ├── financial_analysis.py
│   │   ├── psychological_analysis.py
│   │   ├── dashboard.py
│   │   ├── reports.py
│   │   └── payment.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── stripe_integration.py
│   │   └── gemini_integration.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── welcome.py
│   │   ├── onboarding.py
│   │   ├── financial_input.py
│   │   ├── questionnaire.py
│   │   ├── dashboard.py
│   │   ├── reports.py
│   │   └── payment.py
│   └── components/
│       ├── __init__.py
│       └── navigation.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
├── data/
│   ├── templates/
│   └── sample_data/
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py
│   └── test_questionnaire.py
├── requirements.txt
├── .env.example
└── README.md
```

## Personalização

### Alteração de Estilos

Para modificar a aparência da aplicação, edite o arquivo `static/css/style.css`.

### Adição de Novas Perguntas

Para adicionar novas perguntas ao questionário, edite o arquivo `app/pages/questionnaire.py`.

### Configuração de Integrações

- **Stripe**: Atualize as chaves no arquivo `.env`
- **Gemini API**: Atualize a chave de API no arquivo `.env`

## Suporte e Manutenção

Para suporte ou dúvidas sobre a aplicação, entre em contato com o desenvolvedor.

## Próximos Passos e Expansão

Para expandir a aplicação no futuro, considere:

1. Implementar autenticação de usuários completa
2. Adicionar mais opções de importação de dados financeiros
3. Expandir os relatórios e análises
4. Implementar recursos de gamificação
5. Adicionar integração com instituições financeiras via Open Banking
6. Desenvolver uma comunidade de usuários
7. Criar um sistema de notificações e lembretes

## Licença

Este projeto é proprietário e confidencial. Todos os direitos reservados.
