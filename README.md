# API de Upload e Download de Arquivos

API REST desenvolvida em **Python + Flask** para enviar (upload) e baixar (download) arquivos, com validação de tipo e tamanho, registro de logs e publicação em produção no **Render**.

🔗 **Link público:** `COLE_AQUI_O_LINK_DO_RENDER` (ex.: `https://api-upload-download.onrender.com`)

---

## 📌 Sobre o projeto

A API recebe arquivos por requisição `POST`, valida o tipo e o tamanho, salva na pasta `uploads/` e permite baixá-los depois por uma requisição `GET`. Todas as tentativas de upload (com sucesso ou falha) são registradas no arquivo `uploads.log`.

O projeto segue uma organização em camadas (rotas → controllers → models → banco de dados).

## 🛠️ Tecnologias

- Python 3.12
- Flask 3.1
- SQLite (módulo `sqlite3` da biblioteca padrão)
- Gunicorn (servidor de produção)
- Render (hospedagem)

## 📁 Estrutura de pastas

```
.
├── app.py                         # Ponto de entrada da aplicação
├── requirements.txt               # Dependências do projeto
├── Procfile                       # Comando de inicialização em produção
├── render.yaml                    # Configuração do serviço no Render (opcional)
├── .gitignore
├── controllers/
│   ├── upload_controller.py       # Validação e salvamento dos arquivos
│   └── download_controller.py     # Envio dos arquivos para download
├── database/
│   └── db.py                      # Conexão e criação da tabela SQLite
├── models/
│   ├── upload_model.py
│   └── download_model.py
└── routes/
    ├── upload_route.py            # Rota de upload
    └── download_route.py          # Rota de download
```

## 🔌 Endpoints

| Método | Rota                                    | Descrição                                    |
|--------|-----------------------------------------|----------------------------------------------|
| GET    | `/`                                     | Verifica se a API está online                |
| POST   | `/uploads/upload`                       | Envia um arquivo (`form-data`, campo `file`) |
| GET    | `/downloads/download/<nome_do_arquivo>` | Baixa um arquivo já enviado                  |

### Regras do upload

- **Extensões permitidas:** `png`, `jpg`, `jpeg`, `gif`, `pdf`, `txt`
- **Tamanho máximo:** 30 KB
- O nome do arquivo é sanitizado com `secure_filename` (protege contra nomes como `../../arquivo`).

### Exemplos de resposta

**Upload com sucesso** — `200 OK`
```json
{ "mensagem": "Arquivo salvo com sucesso!", "arquivo": "teste.txt" }
```

**Nenhum arquivo enviado** — `400 Bad Request`
```json
{ "erro": "Nenhum arquivo enviado" }
```

**Tipo não permitido** — `400 Bad Request`
```json
{ "erro": "Tipo de arquivo não permitido!", "tipos_permitidos": ["png", "jpg", "jpeg", "gif", "pdf", "txt"] }
```

**Arquivo grande demais** — `400 Bad Request`
```json
{ "erro": "Arquivo excede o tamanho máximo permitido (30 KB)" }
```

**Download de arquivo inexistente** — `404 Not Found`

## ▶️ Como executar localmente

Pré-requisito: Python 3.10 ou superior.

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/api-upload-download.git
cd api-upload-download

# 2. (Opcional) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a API
python app.py
```

A API ficará disponível em `http://localhost:5000`.

Para ativar o modo de depuração do Flask (somente em desenvolvimento): `FLASK_DEBUG=1 python app.py`.

## 🧪 Como testar

### Com curl

```bash
# Upload
curl -F "file=@teste.txt" http://localhost:5000/uploads/upload

# Download
curl -O -J http://localhost:5000/downloads/download/teste.txt
```

### Com Postman ou Insomnia

1. **Upload:** método `POST` → URL `/uploads/upload` → aba **Body** → **form-data** → chave `file` (tipo *File*) → selecione o arquivo → **Send**.
2. **Download:** método `GET` → URL `/downloads/download/teste.txt` → **Send** (ou abra a URL no navegador).

> Para testar a versão publicada, troque `http://localhost:5000` pelo link público do Render.

## ☁️ Configurações para produção

Ajustes feitos para a publicação:

- **`requirements.txt`**: lista as dependências para o Render instalar (Flask e Gunicorn).
- **Gunicorn**: servidor WSGI de produção, no lugar do servidor de desenvolvimento do Flask (`gunicorn app:app`).
- **`debug` desativado**: o `debug=True` expõe um console interativo e não deve ir para produção. Agora só liga com `FLASK_DEBUG=1`.
- **Porta e host**: em produção o Gunicorn usa a variável `PORT` definida pelo Render; localmente o `app.py` lê `PORT` (padrão 5000) e escuta em `0.0.0.0`.
- **Rota `/`**: facilita testar pelo navegador e serve de *health check*.
- **`.gitignore`**: evita versionar `uploads/`, `database.db`, `uploads.log` e `__pycache__`.
- **`render.yaml` e `Procfile`**: deixam o comando de inicialização documentado.
- **Correções no upload**: tratamento de `Content-Length` ausente e mensagem de erro corrigida para 30 KB (antes dizia 15 KB).

## 🚀 Deploy no Render (passo a passo)

1. Suba o projeto para um repositório no GitHub.
2. Acesse [render.com](https://render.com) e entre com sua conta do GitHub.
3. Clique em **New +** → **Web Service**.
4. Conecte o repositório da API.
5. Preencha:
   - **Language/Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** `Free`
6. (Opcional) Em **Environment Variables**, adicione `PYTHON_VERSION` = `3.12.3`.
7. Clique em **Create Web Service** e aguarde o build terminar (status *Live*).
8. Copie a URL gerada (`https://nome-do-servico.onrender.com`) e teste.

## ⚠️ Limitações conhecidas

- No plano gratuito do Render o **sistema de arquivos é temporário**: arquivos enviados e o `database.db` são apagados a cada novo deploy ou reinício. Para guardar arquivos de forma permanente seria necessário um disco persistente ou um serviço de armazenamento externo (como S3).
- No plano gratuito o serviço **"dorme"** após alguns minutos sem uso; a primeira requisição depois disso pode levar cerca de 1 minuto.
- A tabela `uploads` do SQLite é criada, mas os arquivos enviados ainda não são registrados nela (o controller salva apenas em disco).

## 👤 Autor

Pedro — Estudante de Desenvolvimento de Sistemas
