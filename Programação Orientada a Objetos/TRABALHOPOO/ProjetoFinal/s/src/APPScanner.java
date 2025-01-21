import Cliente.*;
import java.util.List;
import java.util.Scanner;


public class APPScanner {
     public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ClienteDAO clienteDAO = new ClienteDAO();
        int opcao;

        do {
            System.out.println("\n=== Sistema de Gerenciamento de Cliente ===");
            System.out.println("1 - Inserir Cliente");
            System.out.println("2 - Atualizar Cliente");
            System.out.println("3 - Listar Todos os Cliente");
            System.out.println("4 - Buscar Cliente por Nome");
            System.out.println("5 - Deletar Cliente");
            System.out.println("6 - Sair");
            System.out.print("Escolha uma opcao: ");
            opcao = scanner.nextInt();
            scanner.nextLine(); // Limpa o buffer

            switch (opcao) {
                case 1:
                    Cliente novoCliente = new Cliente();
                    System.out.print("Nome: ");
                    novoCliente.setNome(scanner.nextLine());
                    System.out.print("CNPJ: ");
                    novoCliente.setCNPJ(scanner.nextLine());
                    System.out.print("Email: ");
                    novoCliente.setEmail(scanner.nextLine());
                    System.out.print("Telefone: ");
                    novoCliente.setTelefone(scanner.nextLine());
                    System.out.print("Data de Nascimento (YYYY-MM-DD): ");
                    novoCliente.setDataNascimento(scanner.nextLine());
                    System.out.print("Endereco: ");
                    novoCliente.setEndereco(scanner.nextLine());
                    clienteDAO.inserirCliente(novoCliente);
                    System.out.println("Cliente inserido com sucesso!");
                    break;
                case 2:
                    System.out.print("ID do Cliente para atualizar: ");
                    int idAtualizar = scanner.nextInt();
                    scanner.nextLine();
                    Cliente clienteAtualizar = new Cliente();
                    clienteAtualizar.setId(idAtualizar);
                    System.out.print("Novo Nome: ");
                    clienteAtualizar.setNome(scanner.nextLine());
                    System.out.print("Nova CNPJ: ");
                    clienteAtualizar.setCNPJ(scanner.nextLine());
                    System.out.print("Novo Email: ");
                    clienteAtualizar.setEmail(scanner.nextLine());
                    System.out.print("Novo Telefone: ");
                    clienteAtualizar.setTelefone(scanner.nextLine());
                    System.out.print("Nova Data de Nascimento (YYYY-MM-DD): ");
                    clienteAtualizar.setDataNascimento(scanner.nextLine());
                    System.out.print("Novo Endereco: ");
                    clienteAtualizar.setEndereco(scanner.nextLine());
                    clienteDAO.atualizarCliente(clienteAtualizar);
                    System.out.println("Cliente atualizado com sucesso!");
                    break;
                case 3:
                    List<Cliente> clientes = clienteDAO.listarTodos();
                    for (Cliente cliente : clientes) {
                        System.out.println("ID: " + cliente.getId() + " NOME: " + cliente.getNome() + " TELEFONE: " + cliente.getTelefone());
                    }
                    break;
                case 4:
                    System.out.print("Nome para buscar: ");
                    String nomeBusca = scanner.nextLine();
                    Cliente clienteEcontrado = clienteDAO.buscarPorNome(nomeBusca);
                    if (clienteEcontrado != null) {
                        System.out.println("ID: " + clienteEcontrado.getId());
                        System.out.println("Nome: " + clienteEcontrado.getNome());
                        System.out.println("Telefone: " + clienteEcontrado.getTelefone());
                    } else {
                        System.out.println("Cliente nao encontrado.");
                    }
                    break;
                case 5:
                    System.out.print("ID do Cliente para deletar: ");
                    int idDeletar = scanner.nextInt();
                    scanner.nextLine();
                    clienteDAO.deletarCliente(idDeletar);
                    System.out.println("Cliente deletado com sucesso!");
                    break;
                case 6:
                    System.out.println("Saindo do sistema...");
                    break;
                default:
                    System.out.println("Opcao invalida!");
            }
        } while (opcao != 6);

        scanner.close();
    }
}
