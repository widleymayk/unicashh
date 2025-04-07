# Unichash - Sistema de Gerenciamento de Estoque

## Sobre o Projeto

O Unichash é um sistema de gerenciamento de estoque desenvolvido especialmente para pet shops, oferecendo uma solução completa para controle de produtos, clientes, vendas e inventário. Com uma interface intuitiva e recursos abrangentes, o sistema ajuda a otimizar as operações diárias do seu pet shop.

## Funcionalidades Principais

- **Gerenciamento de Produtos**
  - Cadastro e edição de produtos
  - Categorização por tipo de animal
  - Controle de preços
  - Monitoramento de estoque
  - Alertas de estoque mínimo

- **Gestão de Clientes**
  - Cadastro de clientes
  - Histórico de compras
  - Informações de contato

- **Controle de Estoque**
  - Movimentações de entrada e saída
  - Controle de validade
  - Histórico de movimentações
  - Gestão de estoque mínimo

- **Gestão de Vendas**
  - Registro de vendas
  - Histórico de transações
  - Relatórios de vendas

## Requisitos

- Python 3.8 ou superior
- Django 3.2 ou superior
- Banco de dados SQLite (padrão)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/unichash.git
cd unichash
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## Uso

1. Acesse o sistema através do navegador: `http://localhost:8000`
2. Faça login com suas credenciais
3. Navegue pelo menu principal para acessar as diferentes funcionalidades:
   - Produtos
   - Clientes
   - Estoque
   - Vendas

## Tecnologias Utilizadas

- **Backend**: Django
- **Frontend**: Bootstrap 5
- **Banco de Dados**: SQLite
- **Ícones**: Font Awesome
- **JavaScript**: jQuery

## Segurança

O sistema implementa diversas medidas de segurança:
- Proteção contra CSRF
- Headers de segurança HTTP
- Sanitização de entrada de dados
- Autenticação de usuários

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Unichash - [contato@unichash.com](mailto:contato@unichash.com)

Link do Projeto: [https://github.com/seu-usuario/unichash](https://github.com/seu-usuario/unichash)