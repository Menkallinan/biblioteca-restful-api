# 📚 API REST - Biblioteca

API RESTful simples para gerenciamento de livros e empréstimos utilizando Python, CherryPy e SQLite.

## 🚀 Tecnologias Utilizadas

- Python 3.x
- CherryPy
- SQLite3

## ▶️ Como Executar

1. Instale as dependências:
   ```bash
   pip install cherrypy
   ```

2. Execute o servidor:
   ```bash
   python server.py
   ```

A API será executada em `http://localhost:8080`.

## 📘 Endpoints

### 📚 Livros

- `GET /livros`  
  Retorna todos os livros cadastrados.

- `GET /livros/{id}`  
  Retorna os dados de um livro específico.

- `POST /livros`  
  Cadastra um novo livro.  
  Exemplo de payload:
  ```json
  {
    "nome": "Dom Casmurro",
    "autor": "Machado de Assis",
    "edicao": 1,
    "idioma": "Português"
  }
  ```

- `PUT /livros/{id}`  
  Atualiza os dados de um livro existente.

- `DELETE /livros/{id}`  
  Remove um livro pelo ID.

---

### 📄 Empréstimos

- `GET /emprestimos`  
  Lista todos os empréstimos.

- `GET /emprestimos/{id}`  
  Retorna os dados de um empréstimo específico.

- `POST /emprestimos`  
  Cadastra um novo empréstimo.  
  Exemplo de payload:
  ```json
  {
    "livro_id": 1,
    "usuario": "João da Silva",
    "data_emprestimo": "2025-06-26",
    "data_devolucao": "2025-07-10"
  }
  ```

- `PUT /emprestimos/{id}`  
  Atualiza os dados de um empréstimo.

- `DELETE /emprestimos/{id}`  
  Remove um empréstimo pelo ID.

## 🛠 Estrutura dos Arquivos

- `server.py`: Código principal do servidor e rotas da API.
- `bd.py`: Classe `Banco`, responsável por criar o banco de dados e manipular dados com SQLite.

## 📝 Observações

- O banco de dados `biblioteca.db` é criado automaticamente na primeira execução.
- Os dados de entrada são validados para garantir consistência.
- O formato de datas deve ser `"YYYY-MM-DD"`.

---
👨‍💻 Desenvolvido como projeto simples para demonstrar um CRUD completo em API REST com SQLite.
