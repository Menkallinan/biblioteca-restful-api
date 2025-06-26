import cherrypy
from bd import Banco
from datetime import datetime

def validar_dados_livro(dados: dict) -> tuple[bool, str | None]:
    # verifica se campos do livro estão corretos
    if 'nome' not in dados or not isinstance(dados['nome'], str) or not dados['nome'].strip():
        return False, "Campo 'nome' inválido. Deve ser uma string não vazia."
    if 'autor' not in dados or not isinstance(dados['autor'], str) or not dados['autor'].strip():
        return False, "Campo 'autor' inválido. Deve ser uma string não vazia."
    if 'edicao' not in dados or not isinstance(dados['edicao'], int) or dados['edicao'] <= 0:
        return False, "Campo 'edicao' inválido. Deve ser um inteiro positivo."
    if 'idioma' not in dados or not isinstance(dados['idioma'], str) or not dados['idioma'].strip():
        return False, "Campo 'idioma' inválido. Deve ser uma string não vazia."
    return True, None

def validar_dados_emprestimo(dados: dict, bd: Banco) -> tuple[bool, str | None]:
    #  verifica se dados de empréstimo são válidos
    if 'livro_id' not in dados or not isinstance(dados['livro_id'], int):
        return False, "Campo 'livro_id' inválido. Deve ser um inteiro."
    if not bd.obter_livro(dados['livro_id']):
        return False, f"Livro com id {dados['livro_id']} não encontrado."
    if 'usuario' not in dados or not isinstance(dados['usuario'], str) or not dados['usuario'].strip():
        return False, "Campo 'usuario' inválido. Deve ser uma string não vazia."
    if 'data_emprestimo' not in dados or not isinstance(dados['data_emprestimo'], str):
        return False, "Campo 'data_emprestimo' inválido. Deve ser string no formato YYYY-MM-DD."
    try:
        datetime.strptime(dados['data_emprestimo'], '%Y-%m-%d')
    except ValueError:
        return False, "Formato de 'data_emprestimo' incorreto. Deve ser YYYY-MM-DD."
    if 'data_devolucao' in dados and dados['data_devolucao'] is not None:
        if not isinstance(dados['data_devolucao'], str):
            return False, "Campo 'data_devolucao' inválido. Deve ser string no formato YYYY-MM-DD ou null."
        try:
            datetime.strptime(dados['data_devolucao'], '%Y-%m-%d')
        except ValueError:
            return False, "Formato de 'data_devolucao' incorreto. Deve ser YYYY-MM-DD."
    return True, None

class RecursoLivros:
    exposed = True  # ativa MethodDispatcher

    def __init__(self, bd: Banco):
        self.bd = bd

    @cherrypy.tools.json_out()
    def GET(self, id: str = None):
        # busca lista de livros ou livro específico
        if id is None:
            return self.bd.listar_livros()
        try:
            livro_id = int(id)
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID de livro deve ser um inteiro."}
        livro = self.bd.obter_livro(livro_id)
        if livro:
            return livro
        cherrypy.response.status = 404  # retorna 404 se não achar
        return {"erro": "Livro não encontrado."}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        # cadastra novo livro
        dados = cherrypy.request.json
        valido, msg = validar_dados_livro(dados)
        if not valido:
            cherrypy.response.status = 400
            return {"erro": msg}
        novo_id = self.bd.adicionar_livro(
            dados['nome'].strip(),
            dados['autor'].strip(),
            dados['edicao'],
            dados['idioma'].strip()
        )
        cherrypy.response.status = 201  # Retorna 201 Created ou 400 se payload inválido
        return {"id": novo_id}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, id: str):
        # atualiza dados de um livro existente
        try:
            livro_id = int(id)
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID de livro deve ser um inteiro."}
        dados = cherrypy.request.json
        valido, msg = validar_dados_livro(dados)
        if not valido:
            cherrypy.response.status = 400
            return {"erro": msg}
        sucesso = self.bd.atualizar_livro(
            livro_id,
            dados['nome'].strip(),
            dados['autor'].strip(),
            dados['edicao'],
            dados['idioma'].strip()
        )
        if sucesso:
            return {"mensagem": "Livro atualizado com sucesso."}
        cherrypy.response.status = 404  # 404 se não existir
        return {"erro": "Livro não encontrado."}

    @cherrypy.tools.json_out()
    def DELETE(self, id: str):
        # remove um livro
        try:
            livro_id = int(id)
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID de livro deve ser um inteiro."}
        sucesso = self.bd.deletar_livro(livro_id)
        if sucesso:
            return {"mensagem": "Livro deletado com sucesso."}
        cherrypy.response.status = 404  # retorna 404 se não existir
        return {"erro": "Livro não encontrado."}


class RecursoEmprestimos:
    exposed = True  # ativa MethodDispatcher

    def __init__(self, bd: Banco):
        self.bd = bd

    @cherrypy.tools.json_out()
    def GET(self, id: str = None):
        # aqui busca lista de empréstimos ou empréstimo específico
        if id is None:
            return self.bd.listar_emprestimos()
        try:
            emprestimo_id = int(id)
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID de empréstimo deve ser um inteiro."}
        emprestimo = self.bd.obter_emprestimo(emprestimo_id)
        if emprestimo:
            return emprestimo
        cherrypy.response.status = 404  # retorna 404 se não existir
        return {"erro": "Empréstimo não encontrado."}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        # cadastra novo empréstimo
        dados = cherrypy.request.json
        valido, msg = validar_dados_emprestimo(dados, self.bd)
        if not valido:
            cherrypy.response.status = 400
            return {"erro": msg}
        novo_id = self.bd.adicionar_emprestimo(
            dados['livro_id'],
            dados['usuario'].strip(),
            dados['data_emprestimo'],
            dados.get('data_devolucao')
        )
        cherrypy.response.status = 201  # Retorna 201 Created ou 400 se payload inválido
        return {"id": novo_id}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, id: str):
        # atualiza dados de um empréstimo
        try:
            emprestimo_id = int(id)
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID de empréstimo deve ser um inteiro."}
        dados = cherrypy.request.json
        valido, msg = validar_dados_emprestimo(dados, self.bd)
        if not valido:
            cherrypy.response.status = 400
            return {"erro": msg}
        sucesso = self.bd.atualizar_emprestimo(
            emprestimo_id,
            dados['livro_id'],
            dados['usuario'].strip(),
            dados['data_emprestimo'],
            dados.get('data_devolucao')
        )
        if sucesso:
            return {"mensagem": "Empréstimo atualizado com sucesso."}
        cherrypy.response.status = 404  # 404 se não existir
        return {"erro": "Empréstimo não encontrado."}

    @cherrypy.tools.json_out()
    def DELETE(self, id: str):
        # remove um empréstimo
        try:
            emprestimo_id = int(id)
        except ValueError:
            cherrypy.response.status = 400
            return {"erro": "ID de empréstimo deve ser um inteiro."}
        sucesso = self.bd.deletar_emprestimo(emprestimo_id)
        if sucesso:
            return {"mensagem": "Empréstimo deletado com sucesso."}
        cherrypy.response.status = 404  # retorna 404 se não existir
        return {"erro": "Empréstimo não encontrado."}


if __name__ == '__main__':
    bd = Banco()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    cherrypy.tree.mount(RecursoLivros(bd), '/livros', conf)
    cherrypy.tree.mount(RecursoEmprestimos(bd), '/emprestimos', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
