//Função para remover a seleção ativa da barra lateral
function removerActive() {
    document.querySelectorAll(".resource-item").forEach(btn =>
        btn.classList.remove("active")
    );
}

//Carrega uma tela de um endpoint Flask e insere em um container
function carregarTela(endpoint, destino = "main-info") {
    fetch(endpoint)
        .then(resp => {
            if (!resp.ok) {
                throw new Error("Erro HTTP: " + resp.status);
            }
            return resp.text();
        })
        .then(html => {
            document.getElementById(destino).innerHTML = html;
        })
        .catch(err => {
            console.error("Erro ao carregar:", err);
            document.getElementById(destino).innerHTML =
                "<h2>Erro ao carregar</h2><p>Contate o administrador.</p>";
        });
}

//Botões principais
document.getElementById("btn-dashboard").addEventListener("click", e => {
    e.preventDefault();
    carregarTela("/dashboard");
    removerActive();
    e.currentTarget.classList.add("active");
});

document.getElementById("btn-emprestimos").addEventListener("click", e => {
    e.preventDefault();
    carregarTela("/emprestimos");
    removerActive();
    e.currentTarget.classList.add("active");
});

document.getElementById("btn-leitores").addEventListener("click", e => {
    e.preventDefault();
    carregarTela("/leitores");
    removerActive();
    e.currentTarget.classList.add("active");
});

document.getElementById("btn-livros").addEventListener("click", e => {
    e.preventDefault();
    carregarTela("/livros");
    removerActive();
    e.currentTarget.classList.add("active");
});

//Carregar o dashboard por padrão
carregarTela("/dashboard");
document.getElementById("btn-dashboard").classList.add("active");

//Delegação de eventos para telas secundárias
document.addEventListener("click", e => {
    
    // Leitores → Adicionar
    if (e.target.closest("#adicionar-leitor")) {
        carregarTela("/leitores/adicionar", "leitores-container");
    }

    // Livros → Pesquisar
    if (e.target.closest("#opt-pesquisar-livro")) {
        carregarTela("/livros/listar", "livroContentSec");
    }

    // Livros → Cadastrar
    if (e.target.closest("#opt-cadastrar-livro")) {
        carregarTela("/livros/cadastrar", "livroContentSec");
    }
});

document.getElementById("main-info").addEventListener("submit", function(e) {

    // Formulário de empréstimo
    if (e.target && e.target.id === "form-emprestimo") {
        e.preventDefault();
        const formData = new FormData(e.target);
        fetch("/registerBorrow", { method: "POST", body: formData })
            .then(resp => resp.text())
            .then(html => {
                document.getElementById("main-info").innerHTML = html;
                // Oculta mensagens após 10s
                const successDiv = document.querySelector(".successAlert");
                const errorDiv = document.querySelector(".errorAlert");
                if (successDiv) setTimeout(() => successDiv.style.display = "none", 10000);
                if (errorDiv) setTimeout(() => errorDiv.style.display = "none", 10000);
            })
            .catch(err => console.error(err));
    }

    // Formulário de devolução
    if (e.target && e.target.id === "form-devolucao") {
        e.preventDefault();
        const formData = new FormData(e.target);
        fetch("/registerReturn", { method: "POST", body: formData })
            .then(resp => resp.text())
            .then(html => {
                document.getElementById("main-info").innerHTML = html;
                const successDiv = document.querySelector(".successAlert");
                const errorDiv = document.querySelector(".errorAlert");
                if (successDiv) setTimeout(() => successDiv.style.display = "none", 10000);
                if (errorDiv) setTimeout(() => errorDiv.style.display = "none", 10000);
            })
            .catch(err => console.error(err));
    }

    //Formulário de cadastrar livro
    if (e.target && e.target.id === "form-cadastrar-livro") {
        e.preventDefault();
        const formData = new FormData(e.target);
        fetch("/cadastrarLivro", { method: "POST", body: formData})
            .then(resp => resp.text())
            .then(html => {
                document.getElementById("livroContentSec").innerHTML = html;
                const successDiv = document.querySelector(".successAlert");
                const errorDiv = document.querySelector(".errorAlert");
                if (successDiv) setTimeout(() => successDiv.style.display = "none", 10000);
                if (errorDiv) setTimeout(() => errorDiv.style.display = "none", 10000);
            })
            .catch(err => console.error(err));
    }

});

let idSelecionado = null;

function abrirPopup(id) {
    idSelecionado = id;
    document.getElementById("popupBook").style.display = "flex";
}

// function abrirPopupEdit(id) {
//     idSelecionado = id;
//     document.getElementById("popupEditBook").style.display = "flex";

//     fetch(`/edit_book/${idSelecionado}`, { method: "GET"})
//         .then(resp => resp.json())
//         .then(data => {
//             document.querySelector("[name='upTitle']").value = data.titulo;
//             document.querySelector("[name='upAuthor']").value = data.author;
//             document.querySelector("[name='upEditor']").value = data.editora;
//             document.querySelector("[name='upYear']").value = data.ano_publicacao;
//             document.querySelector("[name='upPages']").value = data.qtde_paginas;
//             document.querySelector("[name='upISBN']").value = data.isbn
//         })
//         .catch(error => console.log('Erro ao carregar os dados dos livros:', error));
// }   

function fecharPopup(popup) {
    document.getElementById("popupBook").style.display = "none";
    idSelecionado = null;
}

function confirmarExclusao(){
    fetch(`/delete_book/${idSelecionado}`, { method: "DELETE"})
        .then(resp =>{
            if (resp.ok){
                alert("Livro excluído com sucesso!");
                fecharPopup();
                location.reload();
            } else {
                alert("Erro ao excluir!");
            }
        })
        .catch(err => console.error(err));
}