# Instruções de Deploy e Produção

## Hospedagem Escolhida (Sugestão: Render, Fly.io ou AWS)

A aplicação foi montada para ser Stateless no que se refere ao processamento (utilizando o Banco de Dados para persistência). A escolha ideal e de baixo custo é utilizar o **Render.com** ou **Fly.io**, que oferecem camadas gratuitas generosas e suportam Docker nativamente ou deploy via repositório.

### Dependências Manuais (O que os donos precisam fazer)

1. **Repositório Git**: Empurrar (push) esse código para um repositório no GitHub.
2. **Serviço de Banco de Dados**: Criar um banco de dados PostgreSQL (pode ser o gratuito da Render ou Supabase).
3. **Credenciais (Environment Variables)**: Cadastrar as variáveis no painel da provedora:
   - `SECRET_KEY`: Gerar uma string aleatória (não usar a do `.env.example`).
   - `DEBUG`: `False`.
   - `ALLOWED_HOSTS`: Domínio da aplicação (ex: `casamento-pedrosabrina.com.br`).
   - `DATABASE_URL`: URL do banco de dados provisionado (`postgres://...`).
   - `EMAIL_...`: Credenciais de SMTP (SendGrid, Mailgun ou Gmail via App Password) se as notificações forem habilitadas.

## Como fazer o Deploy

Se a sua plataforma utilizar o Docker (como Fly.io):
```bash
fly launch
fly deploy
```

Se utilizar o Render:
1. Conecte o repositório.
2. Defina o ambiente como "Docker".
3. Preencha as Environment Variables com os dados de produção e a string do Banco de Dados PostgreSQL que o Render fornece.

## Armazenamento de Imagens (Uploads) em Produção
Como o app possui um painel onde são submetidas fotos (presentes, galeria, pix):
- Por padrão, os uploads de media ficam salvos no disco em `/app/media`.
- **Atenção**: Plataformas serverless / efêmeras (como Heroku e Fly.io padrão) resetam os discos.
- Você deve configurar um provedor de Cloud Storage, como AWS S3 (via pacote `django-storages`) e `boto3`.
- Se o deploy ocorrer num VPS tradicional (DigitalOcean Droplet, AWS EC2, Hostinger), o disco será persistido normalmente pela diretiva de volumes do `docker-compose.yml`.

## Configuração de Domínio

1. Acesse o provedor de onde o domínio foi comprado (Registro.br, GoDaddy, Hostinger).
2. Na área de "Zonas de DNS", adicione um apontamento (Registro A ou CNAME) para o IP/URL fornecido pelo serviço de hospedagem.
3. Garanta a emissão de certificado SSL (todas as PaaS modernas como Render e Fly geram isso automaticamente em 1 clique após a configuração do CNAME).

## Opcionais / Futuro
- **Integração WhatsApp**: Ao invés de disparar o e-mail no modelo `reserve_gift` em `views.py`, você pode plugar a API oficial do WhatsApp (Zenvia, Twilio) na camada que cria os `NotificationLogs`.
