# 💊 VidaFarma

<p align="center">
  <img src="./assets/logo.png" width="220">
</p>

<p align="center">
Sistema web para gerenciamento farmacêutico desenvolvido com Django, focado no controle de produtos, estoque, lotes e movimentações.
</p>

## 📖 Sobre o Projeto

O **VidaFarma** é uma aplicação web desenvolvida para auxiliar no gerenciamento de uma drogaria, centralizando informações importantes em um único sistema.

O projeto foi criado com o objetivo de proporcionar maior organização e controle operacional, permitindo o acompanhamento de produtos, estoque e movimentações de forma simples e eficiente.

Além de atender aos requisitos acadêmicos da disciplina **Back-End e Frameworks**, o sistema foi projetado simulando cenários reais encontrados em farmácias e drogarias.


## 🚀 Funcionalidades

### 🔐 Autenticação
- Login de funcionários por matrícula e senha
- Controle de acesso ao sistema

### 💊 Gestão de Produtos
- Cadastro de produtos
- Atualização de informações
- Exclusão de registros
- Organização por categorias

### 📦 Controle de Estoque
- Registro de lotes
- Controle de quantidade disponível
- Atualização automática do estoque

### 📋 Movimentações
- Registro de entradas e saídas
- Histórico de movimentações
- Associação das operações ao funcionário responsável

### 👥 Gestão de Funcionários
- Cadastro de colaboradores
- Controle por matrícula
- Definição de cargos

---

## 🛠️ Tecnologias Utilizadas

- Python
- Django
- Supabase
- HTML5
- CSS3
- JavaScript

## Estrutura do Sistema

O projeto segue uma arquitetura organizada por responsabilidades:

- **Usuários** → autenticação e funcionários
- **Produtos** → gerenciamento de medicamentos
- **Estoque** → controle de lotes e quantidades
- **Movimentações** → entradas e saídas de produtos

---

## Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/vidafarma.git
```

### 2. Acesse a pasta do projeto

```bash
cd vidafarma
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

**Windows**

```bash
venv\Scripts\activate
```

**Linux/MacOS**

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute as migrações

```bash
python manage.py migrate
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

### 8. Acesse o sistema

```text
http://127.0.0.1:8000/
```

---

## 🎯 Objetivo Acadêmico

Este projeto foi desenvolvido para aplicar conceitos de:

- Desenvolvimento Back-End
- Modelagem de Banco de Dados
- Framework Django
- Operações CRUD
- Relacionamentos entre entidades

---

## 👨‍💻 Integrantes

- Gabriel Cristóvão
- Maria Eduarda
- Yure Gabriel

---

## 📚 Disciplina

Projeto desenvolvido para a disciplina **Back-End e Frameworks**.