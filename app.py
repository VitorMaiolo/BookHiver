from flask import Flask, render_template, request, url_for, session, redirect, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "BookHiver25477Sec"

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="bookhiver",
        user="postgres",
        password="1234"
    )

#Definição da rota inicial para a tela de login
@app.route("/")
def index():
    return render_template("index.html")

#Definição da rota para a tela de dashboard
@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    csr = conn.cursor()

    csr.execute("SELECT COUNT(*) FROM livros")
    acervo = csr.fetchone()[0]

    csr.execute("SELECT COUNT(*) FROM leitores")
    leitores = csr.fetchone()[0]

    csr.execute("SELECT COUNT(*) FROM emprestimos WHERE situacao = 'ATIVO'")
    emprestimos = csr.fetchone()[0]

    csr.execute(
            "SELECT COUNT(*) FROM emprestimos WHERE" \
            "   situacao = 'ATIVO'" \
            "   AND data_devolucao_real IS NULL" \
            "   AND CURRENT_DATE > data_devolucao_prevista;"
        )
    atrasados = csr.fetchone()[0]
    return render_template("dashboard.html", acervo=acervo, leitores=leitores, emprestimos=emprestimos, atrasados=atrasados)

#Definição da rota para a tela de empréstimos
@app.route("/emprestimos")
def emprestimo():
    conn = get_connection()
    csr = conn.cursor()

    csr.execute("SELECT COUNT(*) FROM emprestimos WHERE situacao = 'ATIVO'")
    emprestimos = csr.fetchone()[0]

    csr.execute(
        "SELECT COUNT(*) FROM emprestimos WHERE" \
        "   situacao = 'ATIVO'" \
        "   AND data_devolucao_real IS NULL" \
        "   AND CURRENT_DATE > data_devolucao_prevista;"
    )
    atrasados = csr.fetchone()[0]
    return render_template("emprestimos.html", emprestimos=emprestimos, atrasados=atrasados)

#Definição da rota para a tela de leitores
@app.route("/leitores")
def leitores():
    conn = get_connection()
    csr = conn.cursor()

    try:
        csr.execute(
            "SELECT nome, email, telefone FROM leitores ORDER BY nome"
        )
        leitores = csr.fetchall()

        csr.execute("SELECT COUNT(*) FROM leitores")
        quantLeitores = csr.fetchone()[0]

        return render_template("leitores.html", leitores=leitores, quantLeitores=quantLeitores)
    except Exception as e:
        print("Erro ao listar leitores", e)
        return render_template("leitores.html", leitores=[], error="Erro ao listar leitores.")
    finally:
        csr.close()
        conn.close()

#Definição da rota para a tela de livros
@app.route("/livros")
def livros():
    return render_template("livros.html")

#Definição da rota para a tela de listar os leitores
@app.route("/leitores/listar")
def leitores_listar():
    return render_template("leitores_listar.html")

#Definição da rota para a tela de adiconar leitores
@app.route("/leitores/adicionar")
def leitores_adicionar():
    return render_template("leitores_adicionar.html")

#Definição da rota para a tela de listar livros
@app.route("/livros/listar")
def livros_listar():
    conn = get_connection()
    csr = conn.cursor()

    try:
        csr.execute(
            "SELECT titulo, autor, isbn, id, editora FROM livros ORDER BY titulo"
        )
        livros = csr.fetchall()

        return render_template("livros_listar.html", livros=livros)
    except Exception as e:
        print("Erro ao listar livros:", e)
        return render_template("livros_listar.html", livros=[], error="Erro ao listar livros.")
    finally:
        csr.close()
        conn.close()

#Definição da rota para a tela de adicionar livros
@app.route("/livros/cadastrar")
def livros_adicionar():
    return render_template("livros_cadastrar.html")

#Definição da rota para a tela principal após o login 
@app.route("/main", methods=["POST"])
def login():
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
            return render_template("main-page.html", acervo=acervo, leitores=leitores, emprestimos=emprestimos)
        else:
            return render_template("index.html", error="Usuário ou senha inválidos.")
        
    except Exception as e:
        print("Erro: ", e)
        return render_template("index.html", error="Erro ao conectar com o banco de dados.")
    
    finally:
        if conn:
            crs.close()
            conn.close()

#Definição da rota para logout e retornar para a página de login
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))

#Definição da rota para registrar um empréstimo
@app.route("/registerBorrow", methods=["POST"])
def registerBorrow():

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
            return render_template("emprestimos.html", error = "Leitor não cadastrado")
        
        if not livro_existe:
            return render_template("emprestimos.html", error = "Livro não cadastrado")

        csr.execute(
            "INSERT INTO emprestimos (leitor, dataEmprestimo, ISBN, situacao )VALUES (%s, %s, %s, %s)",
            (leitor, data, isbn, situacao)
        )

        conn.commit()
        return render_template("emprestimos.html", message="Empréstimo registrado com sucesso!")
    
    except Exception as e:
        print("Erro:", e)
        return render_template("emprestimos.html", error="Erro ao registrar empréstimo.")
    finally:
        csr.close()
        conn.close()

#Definição da rota para regitrar uma devolução
@app.route("/registerReturn", methods=["POST"])
def registerReturn():

    isbn = request.form["retunISBN"]
    situacao = "INATIVO"

    conn = get_connection()
    csr = conn.cursor()

    try:
        csr.execute(
            "UPDATE emprestimos SET situacao = %s, data_devolucao_real = CURRENT_DATE WHERE isbn = %s",
            (situacao, isbn)
        )

        conn.commit()
        return render_template("emprestimos.html", return_message="Devolução registrada com sucesso!")
    except Exception as e:
        print("Erro:", e)
        return render_template("emprestimos.html", return_error="Erro ao registrar devolução.")
    finally:
        csr.close()
        conn.close()

#Definição da rota para cadastrar um leitor
@app.route("/cadastrasLeitor", methods=["POST"])
def cadastrarLeitor():
    
    nome = request.form["registerReaderName"].title()
    cpf = request.form["registerReaderCPF"]
    email = request.form["registerReaderEmail"]
    telefone = request.form["registerReaderPhone"]

    conn = get_connection()
    csr = conn.cursor()

    try:
        csr.execute(
            "INSERT INTO leitores (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)",
            (nome, cpf, email, telefone)
        )

        conn.commit()
        return render_template("leitores_adicionar.html", success="Leitor cadastrado!")
    except Exception as e:
        print("Erro: ", e)
        return render_template("leitores_adicionar.html", error="Não foi possível completar a ação.")
    finally:
        csr.close()
        conn.close()

#Definição da rota para cadastrar um livro
@app.route("/cadastrarLivro", methods=["POST"])
def cadastrarLivro():

    titulo = request.form["tituloLivro"].title()
    autor = request.form["autorLivro"].title()
    editora = request.form["editoraLivro"].title()
    ano = request.form["anoLivro"]
    # qtdePag = request.form["numPaginas"]
    isbn = request.form["isbnLivroCad"]
    genero = request.form["generoLivro"].title()
    idioma = request.form["idiomaLivro"].title()

    conn = get_connection()
    csr = conn.cursor()

    try:
        csr.execute(
            "INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, genero, idioma) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (titulo, autor, editora, ano, isbn, genero, idioma)
        )

        conn.commit()
        print('Livro Cadastrado!')
        return render_template("livros_cadastrar.html", success="Livro Cadastrado!")
    except Exception as e:
        print("Erro: ", e)
        return render_template("livros_cadastrar.html", error="Não foi possível realizar o cadastro!")
    finally:
        csr.close()
        conn.close()

#Definição da rota para editar as informações dos livros cadastrados
@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def updateBook(book_id):

    conn = get_connection()
    csr = conn.cursor()

    if request.method == "POST":
        titulo = request.form["upTitle"].title()
        autor = request.form["upAuthor"].title()
        editora = request.form["upEditor"].title()
        ano = int(request.form["upYear"])
        pages = int(request.form["upPages"])
        isbn = request.form["upISBN"]

        csr.execute(
            "UPDATE livros SET titulo = %s, autor = %s," \
            "   editora = %s, ano_publicacao = %s, isbn = %s, qtde_paginas = %s WHERE id = %s",
            (titulo, autor, editora, ano, isbn, pages, book_id)
        )
        conn.commit()
        csr.close()
        conn.close()
        print("livro atualizado")
        return render_template("close.html")
    else:
        csr.execute("SELECT * FROM livros WHERE id = %s", (book_id,))
        infos = csr.fetchone()
        author = infos[2]
        csr.close()
        conn.close()
        return render_template("editForm.html", titulo="Editar Livro", infos=list(infos), author=author)

@app.route("/info_book/<int:book_id>", methods=["GET"])
def infoBook(book_id):

     conn = get_connection()
     csr = conn.cursor()

     csr.execute(
         "SELECT * FROM livros WHERE id = %s", (book_id,)
     )
     infoBook = csr.fetchone()
     csr.close()
     conn.close()
     return render_template("editForm.html", titulo="Informações do Livro", infoBook=list(infoBook))    

@app.route("/delete_book/<int:book_id>", methods=["DELETE"])
def deleteBook(book_id):
    
    conn = get_connection()
    csr = conn.cursor()

    csr.execute( "DELETE FROM livros WHERE id = %s", (book_id,))
    conn.commit()
    csr.close()
    conn.close()

    return render_template("livros.html")


if __name__ == "__main__":
    app.run(debug=True)