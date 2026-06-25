# 🤖 Facebook Bot com IA Gratuita (Groq)

Bot para atendimento no Facebook Messenger usando Groq (100% gratuito).

---

## 📁 Arquivos do projeto

```
facebook-bot/
├── app.py            # Código principal do bot
├── requirements.txt  # Bibliotecas necessárias
├── Procfile          # Comando de inicialização (Render)
└── README.md         # Este arquivo
```

---

## 🔑 Passo 1 — Pegar a chave do Groq (grátis)

1. Acesse [console.groq.com](https://console.groq.com)
2. Crie uma conta gratuita
3. Vá em **API Keys > Create API Key**
4. Copie a chave gerada

---

## 🐙 Passo 2 — Subir no GitHub

1. Acesse [github.com](https://github.com) e crie uma conta
2. Clique em **New repository**
3. Dê um nome (ex: `meu-bot-facebook`)
4. Clique em **uploading an existing file**
5. Faça upload dos 4 arquivos
6. Clique em **Commit changes**

---

## 🚀 Passo 3 — Configurar no Render (grátis)

1. Acesse [render.com](https://render.com)
2. Clique em **New > Web Service**
3. Conecte seu repositório GitHub
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### Variáveis de ambiente no Render:

| Variável | Valor |
|----------|-------|
| `PAGE_ACCESS_TOKEN` | Token da sua Página do Facebook |
| `VERIFY_TOKEN` | Uma senha que você inventar (ex: `anabot2024`) |
| `APP_SECRET` | App Secret do seu app Meta |
| `GROQ_API_KEY` | Sua chave do Groq |

---

## 📘 Passo 4 — Configurar no Meta

1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Crie um App > Messenger
3. Vá em **Webhooks** e adicione:
   - **URL:** `https://SEU-APP.onrender.com/webhook`
   - **Verify Token:** o mesmo que você colocou no Render
4. Assine o evento: `messages`
5. Conecte sua Página do Facebook ao app

---

## ✅ Pronto!

Mande uma mensagem para sua Página do Facebook e o bot responderá automaticamente com IA! 🎉
