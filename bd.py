import sqlite3
from datetime import datetime

class Banco:
    

    def __init__(self):
        # Abre (ou cria) o arquivo de banco de dados SQLite
        self.conexao = sqlite3.connect("biblioteca.db", check_same_thread=False)
        # Para retornar cada linha como dicionário {coluna: valor}
        self.conexao.row_factory = sqlite3.Row
        cursor = self.conexao.cursor()

        # Cria a tabela 'livros' caso não exista
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                autor TEXT NOT NULL,
                edicao INTEGER NOT NULL,
                idioma TEXT NOT NULL
            )
        """)

        # Cria a tabela 'emprestimos' caso não exista, ligando-a a livros(id)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id INTEGER NOT NULL,
                usuario TEXT NOT NULL,
                data_emprestimo TEXT NOT NULL,
                data_devolucao TEXT,
                FOREIGN KEY(livro_id) REFERENCES livros(id)
            )
        """)

        self.conexao.commit()
        cursor.close()

    #
    # --- MÉTODOS CRUD PARA LIVROS ---
    #

    def adicionar_livro(self, nome: str, autor: str, edicao: int, idioma: str) -> int:
        """
        Insere um novo livro na tabela 'livros' e Retorna o ID gerado para o livro.
        """
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO livros(nome, autor, edicao, idioma) VALUES(?,?,?,?)",
            (nome, autor, edicao, idioma)
        )
        self.conexao.commit()
        livro_id = cursor.lastrowid
        cursor.close()
        return livro_id

    def obter_livro(self, livro_id: int) -> dict | None:
        """
        Recupera um único livro pelo ID ou Retorna um dicionário com os campos ou None se não existir.
        """
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return dict(row)
        return None

    def listar_livros(self) -> list[dict]:
        """
        Retorna uma lista de todos os livros.
        """
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM livros")
        rows = cursor.fetchall()
        cursor.close()
        return [dict(r) for r in rows]

    def atualizar_livro(self, livro_id: int, nome: str, autor: str, edicao: int, idioma: str) -> bool:
        """
        Atualiza um livro existente. Retorna True se houve atualização, False caso contrário.
        """
        cursor = self.conexao.cursor()
        cursor.execute("""
            UPDATE livros
               SET nome = ?, autor = ?, edicao = ?, idioma = ?
             WHERE id = ?
        """, (nome, autor, edicao, idioma, livro_id))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso

    def deletar_livro(self, livro_id: int) -> bool:
        """
        Exclui um livro pelo ID. Retorna True se houve exclusão, False caso contrário.
        """
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso

    #
    # --- MÉTODOS CRUD PARA EMPRÉSTIMOS ---
    #

    def adicionar_emprestimo(self, livro_id: int, usuario: str, data_emprestimo: str, data_devolucao: str | None = None) -> int:
        """
        Insere um novo empréstimo na tabela 'emprestimos' e retorna o ID gerado para o empréstimo.
        """
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO emprestimos(livro_id, usuario, data_emprestimo, data_devolucao) VALUES(?,?,?,?)",
            (livro_id, usuario, data_emprestimo, data_devolucao)
        )
        self.conexao.commit()
        emprestimo_id = cursor.lastrowid
        cursor.close()
        return emprestimo_id

    def obter_emprestimo(self, emprestimo_id: int) -> dict | None:
        """
        Recupera um único empréstimo pelo ID e retorna um dicionário com os campos ou None se não existir.
        """
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM emprestimos WHERE id = ?", (emprestimo_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return dict(row)
        return None

    def listar_emprestimos(self) -> list[dict]:
        """
        Retorna uma lista de todos os empréstimos.
        """
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM emprestimos")
        rows = cursor.fetchall()
        cursor.close()
        return [dict(r) for r in rows]

    def atualizar_emprestimo(self, emprestimo_id: int, livro_id: int, usuario: str, data_emprestimo: str, data_devolucao: str | None) -> bool:
        """
        Atualiza um empréstimo existente. Retorna True se houve atualização, False caso contrário.
        """
        cursor = self.conexao.cursor()
        cursor.execute("""
            UPDATE emprestimos
               SET livro_id = ?, usuario = ?, data_emprestimo = ?, data_devolucao = ?
             WHERE id = ?
        """, (livro_id, usuario, data_emprestimo, data_devolucao, emprestimo_id))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso

    def deletar_emprestimo(self, emprestimo_id: int) -> bool:
        """
        Exclui um empréstimo pelo ID. Retorna True se houve exclusão, False caso contrário.
        """
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM emprestimos WHERE id = ?", (emprestimo_id,))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso
