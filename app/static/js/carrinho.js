document.addEventListener("DOMContentLoaded", () => {

    const atualizarResumo = () => {
        let subtotal = 0;
        document.querySelectorAll(".produto-lista .colunas-conteudo").forEach(produtoDiv => {
            const precoUnitario = parseFloat(produtoDiv.querySelector(".preco").dataset.preco);
            const quantidade = parseInt(produtoDiv.querySelector(".qtd").innerText);
            const totalProduto = precoUnitario * quantidade;

            // Atualiza o preço exibido na linha
            produtoDiv.querySelector(".preco").innerText = "R$ " + totalProduto.toFixed(2);

            subtotal += totalProduto;
        });

        document.getElementById("subtotal").innerText = "R$ " + subtotal.toFixed(2);
        const taxa = parseFloat(document.getElementById("taxa").innerText.replace("R$","")) || 10;
        document.getElementById("total").innerText = "R$ " + (subtotal + taxa).toFixed(2);
    };

    // Adiciona dataset com o preço unitário para cada produto
    document.querySelectorAll(".produto-lista .colunas-conteudo").forEach(produtoDiv => {
        const precoText = produtoDiv.querySelector(".preco").innerText.replace("R$", "").replace(",", ".");
        produtoDiv.querySelector(".preco").dataset.preco = parseFloat(precoText);
    });

    // Aumentar quantidade
    document.querySelectorAll(".produto-lista .aumentar").forEach(btn => {
        btn.addEventListener("click", async () => {
            const produtoDiv = btn.closest(".colunas-conteudo");
            const id = produtoDiv.dataset.id;
            const qtdSpan = produtoDiv.querySelector(".qtd");
            let quantidade = parseInt(qtdSpan.innerText);
            quantidade++;
            qtdSpan.innerText = quantidade;

            await fetch("/api/adicionar_carrinho", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({id_produto: id, quantidade: 1})
            });

            atualizarResumo();
        });
    });

    // Diminuir quantidade
    document.querySelectorAll(".produto-lista .diminuir").forEach(btn => {
        btn.addEventListener("click", async () => {
            const produtoDiv = btn.closest(".colunas-conteudo");
            const id = produtoDiv.dataset.id;
            const qtdSpan = produtoDiv.querySelector(".qtd");
            let quantidade = parseInt(qtdSpan.innerText);
            if(quantidade > 1) quantidade--;
            qtdSpan.innerText = quantidade;

            await fetch("/api/adicionar_carrinho", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({id_produto: id, quantidade: -1})
            });

            atualizarResumo();
        });
    });

    // Remover produto
    document.querySelectorAll(".produto-lista .remover").forEach(btn => {
        btn.addEventListener("click", async () => {
            const produtoDiv = btn.closest(".colunas-conteudo");
            const id = produtoDiv.dataset.id;

            await fetch("/api/remover_carrinho", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({id_produto: id})
            });

            produtoDiv.remove();
            atualizarResumo();
        });
    });

    atualizarResumo(); // inicializa valores
});
// Seleciona elementos do pop-up
const avisoPopup = document.getElementById("aviso-popup");
const btnFecharAviso = document.getElementById("fechar-aviso");

// Função para abrir o pop-up
function mostrarAviso() {
    avisoPopup.style.display = "block";
}

// Fecha o pop-up
btnFecharAviso.addEventListener("click", () => {
    avisoPopup.style.display = "none";
});

// Seleciona os botões Finalizar e Limpar
const btnFinalizar = document.getElementById("finalizar");
const btnLimpar = document.getElementById("limpar");

// Mostra aviso ao clicar
btnFinalizar.addEventListener("click", mostrarAviso);
btnLimpar.addEventListener("click", mostrarAviso);
