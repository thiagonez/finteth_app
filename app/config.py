import streamlit as st
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da aplicação
APP_NAME = "Análise Financeira Pessoal"
APP_VERSION = "0.1.0"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Configurações do Stripe
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "pk_live_51RRhcMDVv3pnR1Zf91ylZQVNFjIb8sjHrVxlygus4X8EDHl4EbJh3Q9isWWPgYUVJTQ8CCNjksJMzW8B7vZaud1z00RHCfrVFu")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "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")

# Configurações da API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDi54Bpx14wY8QZ6B5gVLd5LzSm-Mfw76I")

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurações de banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fintech_app.db")

# Configurações de relatórios
BASIC_REPORT_PRICE = 50.00  # Preço em reais
