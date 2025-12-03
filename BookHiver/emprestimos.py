from conexao import get_connection

def registrarEmprestimo(request):
    leitor = request.form["borrowReaderName"]
    data = request.form["borrowDate"]
    isbn = request.form["borrowISBN"]
    situacao = "ATIVO"


    conn = get_connection()
    csr = conn.cursor()

    try:
        csr.execute("SELECT 1 FROM leitores WHERE nome = %s", (leitor,))
        leitor_existe = csr.fetchone()

        csr.execute("SELECT 1 FROM livros WHERE isbn = %s", (isbn,))
        livro_existe = csr.fetchone()

        if not leitor_existe:
            return {
                "leitorExiste": False,
                "error": "Leitor não cadastrado."
            }
        
        if not livro_existe:
            return {
                "livroExiste": False,
                "error": "Livro não cadastrado."
            }

        csr.execute(
            "INSERT INTO emprestimos (leitor, dataEmprestimo, ISBN, situacao )VALUES (%s, %s, %s, %s)",
            (leitor, data, isbn, situacao)
        )

        conn.commit()
        return{
            "emprestimo": True,
            "message": "Empréstimo registrado com sucesso!"
        }
    
    except Exception as e:
        print("Erro:", e)
        return {
            "emprestimo": False,
            "error": "Erro ao registrar empréstimo."
        }
    finally:
        csr.close()
        conn.close()