# 📖 Documentação da API - Lighthouse

## **Visão Geral**

A API do projeto Lighthouse permite a análise de performance e acessibilidade de sites utilizando o **Unlighthouse**, além de gerenciar sites e usuários. Abaixo estão detalhadas as rotas disponíveis, os métodos suportados e exemplos de uso.

---

## **Base URL**
`http://localhost:3000`

---

## **Rotas da API**

### **1. Analisar Site**

#### **GET /api/analisar**
Executa a análise de um site fornecido e retorna o relatório em JSON.

**Parâmetros de Query:**
- `siteUrl` (obrigatório): URL do site a ser analisado.
- `device` (opcional): Tipo de dispositivo para análise (`desktop` ou `mobile`). Padrão: `desktop`.

**Exemplo de Requisição:**
```bash
GET /api/analisar?siteUrl=https://exemplo.com&device=mobile
```

**Resposta de Sucesso:**
```json
{
  "message": "Relatório gerado e salvo com sucesso",
  "data": {
    "siteUrl": "https://exemplo.com",
    "score": 90,
    "performance": 85,
    "accessibility": 95,
    "seo": 88
  }
}
```

---

### **2. Gerenciar Sites**

#### **GET /api/site**
Lista todos os sites cadastrados ou busca um site específico pelo ID.

**Query Parameters:**
- `id` (opcional): ID do site para busca específica.

**Exemplo de Requisição:**
```bash
GET /api/site?id=1
```

**Resposta de Sucesso:**
```json
{
  "id": 1,
  "nome": "Site Exemplo",
  "url": "https://exemplo.com",
  "orgao": "Organização Exemplo",
  "sigla": "OE",
  "ativo": true
}
```

#### **POST /api/site**
Cadastra um novo site.

**Body (JSON):**
```json
{
  "nome": "Site Exemplo",
  "url": "https://exemplo.com",
  "orgao": "Organização Exemplo",
  "sigla": "OE",
  "ativo": true
}
```

**Exemplo de Requisição:**
```bash
curl -X POST http://localhost:3000/api/site \
  -H "Content-Type: application/json" \
  -d '{"nome": "Site Exemplo", "url": "https://exemplo.com", "orgao": "Organização Exemplo", "sigla": "OE", "ativo": true}'
```

**Resposta de Sucesso:**
```json
{
  "id": 1,
  "nome": "Site Exemplo",
  "url": "https://exemplo.com",
  "orgao": "Organização Exemplo",
  "sigla": "OE",
  "ativo": true
}
```

#### **PUT /api/site**
Atualiza as informações de um site existente.

**Query Parameters:**
- `id` (obrigatório): ID do site a ser atualizado.

**Body (JSON):**
```json
{
  "nome": "Site Atualizado",
  "url": "https://exemplo.com",
  "orgao": "Organização Exemplo Atualizada",
  "ativo": false
}
```

**Exemplo de Requisição:**
```bash
curl -X PUT http://localhost:3000/api/site?id=1 \
  -H "Content-Type: application/json" \
  -d '{"nome": "Site Atualizado", "url": "https://exemplo.com", "orgao": "Organização Exemplo Atualizada", "ativo": false}'
```

#### **DELETE /api/site**
Remove um site pelo ID.

**Query Parameters:**
- `id` (obrigatório): ID do site a ser removido.

**Exemplo de Requisição:**
```bash
curl -X DELETE http://localhost:3000/api/site?id=1
```

**Resposta de Sucesso:**
```json
{
  "message": "Site removido com sucesso."
}
```

---

### **3. Gerenciar Usuários**

#### **GET /api/usuario**
Lista todos os usuários cadastrados.

**Exemplo de Requisição:**
```bash
GET /api/usuario
```

**Resposta de Sucesso:**
```json
[
  {
    "id": 1,
    "nome": "Usuário Exemplo",
    "email": "usuario@exemplo.com",
    "role": "admin"
  }
]
```

#### **POST /api/usuario**
Cadastra um novo usuário.

**Body (JSON):**
```json
{
  "nome": "Usuário Exemplo",
  "email": "usuario@exemplo.com",
  "senha": "senha123",
  "role": "admin"
}
```

**Exemplo de Requisição:**
```bash
curl -X POST http://localhost:3000/api/usuario \
  -H "Content-Type: application/json" \
  -d '{"nome": "Usuário Exemplo", "email": "usuario@exemplo.com", "senha": "senha123", "role": "admin"}'
```

**Resposta de Sucesso:**
```json
{
  "id": 1,
  "nome": "Usuário Exemplo",
  "email": "usuario@exemplo.com",
  "role": "admin"
}
```

#### **PUT /api/usuario**
Atualiza as informações de um usuário existente.

**Body (JSON):**
```json
{
  "id": 1,
  "nome": "Usuário Atualizado",
  "email": "usuario@exemplo.com",
  "senha": "novaSenha123"
}
```

**Exemplo de Requisição:**
```bash
curl -X PUT http://localhost:3000/api/usuario \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "nome": "Usuário Atualizado", "email": "usuario@exemplo.com", "senha": "novaSenha123"}'
```

#### **DELETE /api/usuario**
Remove um usuário pelo ID.

**Body (JSON):**
```json
{
  "id": 1
}
```

**Exemplo de Requisição:**
```bash
curl -X DELETE http://localhost:3000/api/usuario \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

---

## **Contato**
**Autor:** Fabio Ramos  
**E-mail:** [framos@segov.ms.gov.br](mailto:framos@segov.ms.gov.br)  
**LinkedIn:** [Fabio Ramos](https://www.linkedin.com/in/fabio-ramos-7b8608204/)
