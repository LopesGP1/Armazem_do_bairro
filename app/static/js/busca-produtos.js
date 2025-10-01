document.addEventListener("DOMContentLoaded", () => {
    const inputBusca = document.querySelector(".header .search-bar input");
    const produtosContainer = document.querySelector(".produtos");

    if (!inputBusca || !produtosContainer) return;

    inputBusca.addEventListener("input", async () => {
        const termo = inputBusca.value.trim();

        const response = await fetch(`/api/buscar?q=${encodeURIComponent(termo)}`);
        const produtos = await response.json();

        produtosContainer.innerHTML = "";

        if (produtos.length === 0) {
            produtosContainer.innerHTML = "<p>Nenhum produto encontrado.</p>";
            return;
        }

        produtos.forEach(p => {
            const card = document.createElement("div");
            card.classList.add("produto-card");
            card.innerHTML = `
                <img src="/${p.imagem}" alt="${p.nome}">
                <h2>${p.nome}</h2>
                <p class="preco">R$ ${parseFloat(p.preco_unitario).toFixed(2)}</p>
                <button class="add-carrinho">Adicionar</button>
            `;
            produtosContainer.appendChild(card);
        });
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("popup");
    const overlay = document.getElementById("overlay");
    const nomeProduto = document.getElementById("popup-nome");
    const precoUnitario = document.getElementById("popup-preco");
    const total = document.getElementById("popup-total");
    const inputQuantidade = document.getElementById("quantidade");

    let produtoSelecionado = null;

    // Abre o pop-up ao clicar em "Adicionar"
    document.querySelectorAll(".add-carrinho").forEach((btn, index) => {
        btn.addEventListener("click", () => {
            const card = btn.closest(".produto-card");
            const nome = card.querySelector("h2").innerText;
            const preco = parseFloat(card.querySelector(".preco").innerText.replace("R$","").trim());

            produtoSelecionado = {
                nome: nome,
                preco_unitario: preco,
                id_produto: card.dataset.id // aqui você pode pegar o id real do produto via dataset se quiser
            };

            nomeProduto.innerText = produtoSelecionado.nome;
            precoUnitario.innerText = produtoSelecionado.preco_unitario.toFixed(2);
            inputQuantidade.value = 1;
            total.innerText = produtoSelecionado.preco_unitario.toFixed(2);

            popup.style.display = "block";
            overlay.style.display = "block";
        });
    });

    // Atualiza o total ao mudar a quantidade
    inputQuantidade.addEventListener("input", () => {
        const quantidade = parseFloat(inputQuantidade.value) || 1;
        total.innerText = (produtoSelecionado.preco_unitario * quantidade).toFixed(2);
    });

    // Cancelar
    document.getElementById("cancelar").addEventListener("click", () => {
        popup.style.display = "none";
        overlay.style.display = "none";
    });

    // Confirmar
    document.getElementById("confirmar").addEventListener("click", async () => {
        const quantidade = parseFloat(inputQuantidade.value);

        // Chamada ao Flask para adicionar ao carrinho
        const response = await fetch("/api/adicionar_carrinho", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id_produto: produtoSelecionado.id_produto,
                quantidade: quantidade
            })
        });

        if (response.ok) {
            alert("Produto enviado para o carrinho!");
        } else {
            alert("Erro ao adicionar o produto!");
        }

        popup.style.display = "none";
        overlay.style.display = "none";
    });
});
