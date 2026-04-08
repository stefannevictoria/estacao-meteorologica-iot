// Funções globais da interface

// Deleta uma leitura pelo id via API e remove a linha da tabela
async function deletar(id) {
  if (!confirm(`Deseja remover a leitura #${id}?`)) return;

  try {
    const resp = await fetch(`/leituras/${id}`, { method: 'DELETE' });
    if (resp.ok) {
      // Remove a linha da tabela sem recarregar a página
      const btn = document.querySelector(`button[onclick="deletar(${id})"]`);
      if (btn) {
        const row = btn.closest('tr');
        row.style.opacity = '0.5';
        setTimeout(() => row.remove(), 300);
      } else {
        location.reload();
      }
    } else {
      alert('Erro ao deletar a leitura.');
    }
  } catch (err) {
    alert('Erro de conexão com o servidor.');
    console.error(err);
  }
}

// Recarrega a página atual
function atualizarPagina() {
  location.reload();
}

// Event listeners gerais
document.addEventListener('DOMContentLoaded', function() {
  // Adiciona feedback visual em formulários
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function() {
      const button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
        button.textContent = '⏳ Salvando...';
      }
    });
  });

  // Smooth scroll para links internos
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});