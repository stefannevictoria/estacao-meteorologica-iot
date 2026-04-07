// Funções globais da interface

// Deleta uma leitura pelo id via API e remove a linha da tabela
async function deletar(id) {
  if (!confirm(`Deseja remover a leitura #${id}?`)) return;

  try {
    const resp = await fetch(`/leituras/${id}`, { method: 'DELETE' });
    if (resp.ok) {
      // Remove a linha da tabela sem recarregar a página
      const btn = document.querySelector(`button.btn-del[onclick="deletar(${id})"]`);
      if (btn) btn.closest('tr').remove();
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