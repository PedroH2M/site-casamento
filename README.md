# Sistema de Lista de Presentes de Casamento (Pedro & Sabrina)

Este projeto é um sistema web completo para gerenciar a lista de presentes de casamento. Foi desenvolvido visando a melhor experiência em dispositivos móveis (mobile-first), performance, segurança e design elegante e natural.

## 🛠️ Stack Tecnológica

- **Backend:** Python + Django (Robusto, seguro e possui admin embutido).
- **Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Produção).
- **Frontend:** HTML5, Vanilla CSS (Variáveis CSS, CSS Grid/Flexbox) e JavaScript nativo (sem dependências pesadas).
- **ORM:** Django ORM (proteção nativa contra injeção SQL e suporte a transações ACID para prevenir duplas reservas de presentes).
- **Infraestrutura:** Docker e Docker Compose prontos para uso.

## 🚀 Funcionalidades

### Área Pública
- Apresentação do Casal (Capa com fotos configuráveis).
- História do Casal.
- Detalhes do Casamento (Data, Local, Mapa).
- Galeria de Fotos.
- Lista de Presentes por Categoria com visualização de quantidade disponível.
- **Reserva Segura de Presentes:** Os convidados podem reservar x unidades de um presente informando o nome e mensagem, com controle restrito de estoque.
- Mensagens de Convidados.
- Sessão de Contribuição via PIX.

### Painel Administrativo
- Proteção por autenticação e senhas (hash).
- Configuração de todos os textos, frases, imagens de capa e chaves PIX de forma dinâmica, sem necessidade de tocar no código.
- Gerenciamento de Categorias.
- Gerenciamento de Presentes (Imagem, Nome, Quantidade Total).
- Gerenciamento de Reservas (Acompanhar as reservas, aprovar mensagens e opção para cancelar e devolver ao estoque).
- Registro de logs (Notification Logs).

## 💻 Como executar localmente (Ambiente Virtual)

1. Tenha o Python instalado na máquina (recomendado >= 3.11).
2. Acesse a pasta do projeto.
3. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\Activate.ps1
   # No Linux/Mac:
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure as variáveis de ambiente copiando o arquivo `.env.example`:
   ```bash
   cp .env.example .env
   ```
6. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
7. Crie o superusuário padrão e os dados de teste (Seed):
   ```bash
   python seed.py
   ```
8. Inicie o servidor local:
   ```bash
   python manage.py runserver
   ```
9. Acesse:
   - Público: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/` (Login: `admin` / Senha: `admin123`)

## 🐳 Como executar localmente com Docker

1. Verifique se tem o Docker e o Docker Compose instalados.
2. Na raiz do projeto, execute:
   ```bash
   docker-compose up -d --build
   ```
3. O app estará em `http://localhost:8000`.

## 🧪 Testes

Foram implementados testes unitários garantindo:
- Carregamento da página principal.
- Reserva válida de presentes e atualização de estoque.
- Bloqueio de reservas maiores do que a disponibilidade (`overbooking`).
- Devolução de estoque após o cancelamento de uma reserva via Admin.

Para rodar os testes:
```bash
python manage.py test
```

## 🔒 Variáveis de Ambiente e Credenciais

Nenhuma credencial ou token foi fixado no código. Tudo deve ser providenciado através do arquivo `.env`:
- `SECRET_KEY`: Chave secreta do Django.
- `DATABASE_URL`: String de conexão com o PostgreSQL (se vazio, usa SQLite).
- Variáveis de E-mail para configurar servidor SMTP (WhatsApp necessitará integração API de terceiros através dos logs de notificação).
