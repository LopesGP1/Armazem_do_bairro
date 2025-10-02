// cliente.js - Pop-up de adicionar produto ao carrinho
let produtoSelecionado = null;

// Seleciona elementos do pop-up
const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const popupNome = document.getElementById('popup-nome');
const popupPreco = document.getElementById('popup-preco');
const popupQuantidade = document.getElementById('quantidade');
const popupTotal = document.getElementById('popup-total');
const btnCancelar = document.getElementById('cancelar');
const btnConfirmar = document.getElementById('confirmar');

document.querySelectorAll('.add-carrinho').forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const card = e.target.closest('.produto-card');
        const nome = card.querySelector('h2').innerText;
        const preco = parseFloat(card.querySelector('.preco').innerText.replace('R$', '').replace(',', '.'));
        const id_produto = card.dataset.id;

        produtoSelecionado = { id_produto, nome, preco, quantidade: 1 };

        popupNome.innerText = nome;
        popupPreco.innerText = preco.toFixed(2);
        popupQuantidade.value = 1;
        popupTotal.innerText = preco.toFixed(2);

        overlay.style.display = 'block';
        popup.style.display = 'block';
    });
});

popupQuantidade.addEventListener('input', () => {
    const qtd = parseFloat(popupQuantidade.value);
    produtoSelecionado.quantidade = qtd;
    popupTotal.innerText = (produtoSelecionado.preco * qtd).toFixed(2);
});

btnCancelar.addEventListener('click', () => {
    popup.style.display = 'none';
    overlay.style.display = 'none';
});

btnConfirmar.addEventListener('click', async () => {
    await fetch("/api/adicionar_carrinho", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id_produto: produtoSelecionado.id_produto, quantidade: produtoSelecionado.quantidade})
    });

    popup.style.display = 'none';
    overlay.style.display = 'none';
    alert('Produto adicionado ao carrinho!');
});
