// Seleção dos elementos
const popupGlobal = document.getElementById('aviso-popup-global');
const overlayGlobal = document.getElementById('overlay-aviso-global');
const fecharPopupGlobal = document.getElementById('fechar-aviso-global');

// Função para abrir o pop-up
function abrirPopupGlobal() {
    popupGlobal.style.display = 'block';
    overlayGlobal.style.display = 'block';
}

// Função para fechar o pop-up
fecharPopupGlobal.addEventListener('click', () => {
    popupGlobal.style.display = 'none';
    overlayGlobal.style.display = 'none';
});

// Adicionar evento nos botões de Funcionário e Gerente
document.querySelectorAll('.botoes .botao').forEach((btn) => {
    // Só para Funcionário e Gerente
    if (btn.innerText.includes('Funcionário') || btn.innerText.includes('Gerente')) {
        btn.addEventListener('click', (e) => {
            e.preventDefault(); // impede o redirecionamento
            abrirPopupGlobal();
        });
    }
});
