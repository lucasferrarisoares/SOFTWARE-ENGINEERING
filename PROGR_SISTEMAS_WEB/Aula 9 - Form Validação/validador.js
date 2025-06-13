document.getElementById('contatoForm').addEventListener('submit', function (event) {
  event.preventDefault(); // evita envio mesmo que esteja válido
  const form = event.target;
  let valido = true;

  // Limpa mensagens anteriores
  document.getElementById('erro-nome').textContent = '';
  document.getElementById('erro-email').textContent = '';
  document.getElementById('erro-telefone').textContent = '';

  // Nome
  if (!form.nome.value.trim()) {
    document.getElementById('erro-nome').textContent = "O campo Nome é obrigatório.";
    valido = false;
  }

  // Email
  if (!form.email.value.trim()) {
    document.getElementById('erro-email').textContent = "O campo E-mail é obrigatório.";
    valido = false;
  } else if (!form.email.checkValidity()) {
    document.getElementById('erro-email').textContent = "Informe um e-mail válido.";
    valido = false;
  }

  // Telefone
  const telefone = form.telefone.value.trim();
  if (!telefone) {
    document.getElementById('erro-telefone').textContent = "O campo Telefone é obrigatório.";
    valido = false;
  } else if (!/^\d{10,11}$/.test(telefone)) {
    document.getElementById('erro-telefone').textContent = "Informe um número com 10 ou 11 dígitos.";
    valido = false;
  }

  // Se estiver tudo certo
  if (valido) {
    alert("Formulário enviado com sucesso!");
    form.reset();
  }
});
