from conexao import get_connection
from flask import session

def login(request):
    user = request.form["user"]
    password = request.form["password"]

    conn = get_connection()
    crs = conn.cursor()

    try:

        crs.execute("""SELECT usuario, senha FROM users WHERE usuario = %s AND senha = %s""",
                    (user, password))
        
        resultado = crs.fetchone()

        crs.execute("SELECT COUNT(*) FROM livros")
        acervo = crs.fetchone()[0]

        crs.execute("SELECT COUNT(*) FROM leitores")
        leitores = crs.fetchone()[0]

        crs.execute("SELECT COUNT(*) FROM emprestimos WHERE situacao = 'ATIVO'")
        emprestimos = crs.fetchone()[0]

        if resultado:
            session["usuario"] = user
            return {
                "logado": True,
                "acervo": acervo,
                "emprestimos": emprestimos,
                "leitores": leitores
            }
        else:
            return {
                "logado": False,
                "error": "Usuário ou senha inválidos."
            }
        
    except Exception as e:
        print("Erro: ", e)
        return {
                "logado": False,
                "error": "Erro ao conectar com o banco de dados."
            }

    
    finally:
        if conn:
            crs.close()
            conn.close()