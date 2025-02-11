import java.util.List;
import java.util.Scanner;

public class APPScanner {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ClienteDAO clienteDAO = new ClienteDAO();
        int opcao;

        do {
            System.out.println("\n=== Sistema de Gerenciamento ===");
            System.out.println("1 - Clientes");
            System.out.println("2 - Projetos");
            System.out.println("3 - Colaboradores");
            System.out.println("4 - Contratos");
            System.out.println("0 - Sair");
            System.out.print("Escolha uma opção: ");
            opcao = scanner.nextInt();
            scanner.nextLine();

            switch (opcao) {
                case 1:
                    menuClientes(scanner);
                    break;
                case 2:
                    menuProjetos(scanner);
                    break;
                case 3:
                    menuColaboradores(scanner);
                    break;
                case 4:
                    menuContratos(scanner);
                    break; 
                case 0:
                    System.out.println("Saindo do sistema...");
                    break;
                default:
                    System.out.println("Opção inválida!");
            }
        } while (opcao != 0);
        
        scanner.close();
    }

    private static void menuClientes(Scanner scanner) {
        int opcao;
        do {
            System.out.println("\n=== Gerenciamento de Clientes ===");
            System.out.println("1 - Adicionar Cliente");
            System.out.println("2 - Atualizar Cliente");
            System.out.println("3 - Listar Clientes");
            System.out.println("4 - Buscar Cliente por Nome");
            System.out.println("5 - Deletar Cliente");
            System.out.println("0 - Voltar ao Menu Principal");
            System.out.print("Escolha uma opção: ");
            opcao = scanner.nextInt();
            scanner.nextLine();

            switch (opcao) {
                case 1:
                    adicionarCliente(scanner);
                    break;
                case 2:
                    atualizarCliente(scanner);
                    break;
                case 3:
                    listarClientes();
                    break;
                case 4:
                    buscarCliente(scanner);
                    break;
                case 5:
                    deletarCliente(scanner);
                    break;
                case 0:
                    System.out.println("Retornando ao menu principal...");
                    break;
                default:
                    System.out.println("Opção inválida!");
            }
        } while (opcao != 0);
    }

    private static void menuColaboradores(Scanner scanner) {
        int opcao;
        do {
            System.out.println("\n=== Gerenciamento de Colaborador ===");
            System.out.println("1 - Adicionar Colaborador");
            System.out.println("2 - Atualizar Colaborador");
            System.out.println("3 - Listar Colaborador");
            System.out.println("4 - Buscar Colaborador por Nome");
            System.out.println("5 - Deletar Colaborador");
            System.out.println("0 - Voltar ao Menu Principal");
            System.out.print("Escolha uma opção: ");
            opcao = scanner.nextInt();
            scanner.nextLine();

            switch (opcao) {
                case 1:
                    adicionarColaboradores(scanner);
                    break;
                case 2:
                    atualizarColaboradores(scanner);
                    break;
                case 3:
                    listarColaboradores();
                    break;
                case 4:
                    buscarColaboradores(scanner);
                    break;
                case 5:
                    deletarColaboradores(scanner);
                    break;
                case 0:
                    System.out.println("Retornando ao menu principal...");
                    break;
                default:
                    System.out.println("Opção inválida!");
            }
        } while (opcao != 0);
    }

    private static void menuProjetos(Scanner scanner) {
        int opcao;
        do {
            System.out.println("\n=== Gerenciamento de Clientes ===");
            System.out.println("1 - Adicionar Projeto");
            System.out.println("2 - Atualizar Projeto");
            System.out.println("3 - Listar Projetos");
            System.out.println("4 - Buscar Projeto por Nome");
            System.out.println("5 - Deletar Projeto");
            System.out.println("0 - Voltar ao Menu Principal");
            System.out.print("Escolha uma opção: ");
            opcao = scanner.nextInt();
            scanner.nextLine();

            switch (opcao) {
                case 1:
                    adicionarProjeto(scanner);
                    break;
                case 2:
                    atualizarProjeto(scanner);
                    break;
                case 3:
                    listarProjeto();
                    break;
                case 4:
                    buscarProjeto(scanner);
                    break;
                case 5:
                    deletarProjeto(scanner);
                    break;
                case 0:
                    System.out.println("Retornando ao menu principal...");
                    break;
                default:
                    System.out.println("Opção inválida!");
            }
        } while (opcao != 0);
    }

    private static void menuContratos(Scanner scanner) {
        int opcao;
        do {
            System.out.println("\n=== Gerenciamento de Clientes ===");
            System.out.println("1 - Adicionar Contratos");
            System.out.println("2 - Atualizar Contratos");
            System.out.println("3 - Listar Contratos");
            System.out.println("5 - Deletar Contratos");
            System.out.println("0 - Voltar ao Menu Principal");
            System.out.print("Escolha uma opção: ");
            opcao = scanner.nextInt();
            scanner.nextLine();

            switch (opcao) {
                case 1:
                    adicionarContratos(scanner);
                    break;
                case 2:
                    atualizarContratos(scanner);
                    break;
                case 3:
                    listarContratos();
                    break;
                case 4:
                    buscarContratos(scanner);
                    break;
                case 5:
                    deletarContratos(scanner);
                    break;
                case 0:
                    System.out.println("Retornando ao menu principal...");
                    break;
                default:
                    System.out.println("Opção inválida!");
            }
        } while (opcao != 0);
    }

    private static void adicionarContratos(Scanner scanner) {
        Contrato contrato = new Contrato();
        ContratoDAO contratoDAO = new ContratoDAO();
        System.out.print("Id Cliente: ");
        contrato.setIdCliente(scanner.nextInt());
        System.out.print("Tipo Serviço: ");
        contrato.setTipoServico(scanner.nextLine());
        System.out.print("Prazo: ");
        contrato.setPrazo(scanner.nextLine());
        System.out.print("Valor: ");
        contrato.setValor(scanner.nextFloat());

        contratoDAO.inserirContrato(contrato);
        System.out.println("Cliente inserido com sucesso!");
    }

    private static void atualizarContratos(Scanner scanner) {
        Contrato contrato = new Contrato();
        ContratoDAO contratoDAO = new ContratoDAO();

        System.out.print("ID do Colaborador para atualizar: ");
        int idAtualizar = scanner.nextInt();
        scanner.nextLine();
        
        contrato.setIdContrato(idAtualizar);
        System.out.print("Id Cliente: ");
        contrato.setIdCliente(scanner.nextInt());
        System.out.print("Tipo Serviço: ");
        contrato.setTipoServico(scanner.nextLine());
        System.out.print("Prazo: ");
        contrato.setPrazo(scanner.nextLine());
        System.out.print("Valor: ");
        contrato.setValor(scanner.nextFloat());
        
        contratoDAO.atualizarContrato(contrato);
        System.out.println("Contrato atualizado com sucesso!");
    }

    private static void listarContratos() {
        ContratoDAO contratoDAO = new ContratoDAO();
        List<Contrato> contratos = contratoDAO.listarTodos();
        for (Contrato contrato : contratos) {
            System.out.println("ID: " + contrato.getIdContrato() + " | Cliente: " + contrato.getIdCliente() + " | Valor: " + contrato.getValor());
        }
    }

    private static void buscarContratos(Scanner scanner) {
        ContratoDAO contratoDAO = new ContratoDAO();
        System.out.print("Id para buscar: ");
        String nomeBusca = scanner.nextLine();
        
        Contrato contrato = contratoDAO.buscarPorNome(nomeBusca);

        if (contrato != null) {
            System.out.println("ID: " + contrato.getIdCliente());
            System.out.println("Id Cliente: " + contrato.getIdCliente());
            System.out.println("Valor: " + contrato.getValor());
        } else {
            System.out.println("Contrato não encontrado.");
        }
    }

    private static void deletarContratos(Scanner scanner) {
        ContratoDAO contratoDAO = new ContratoDAO();
        System.out.print("ID do Contrato para deletar: ");
        int idDeletar = scanner.nextInt();
        scanner.nextLine();
        contratoDAO.deletarContrato(idDeletar);
        System.out.println("Colaborador deletado com sucesso!");
    }



    private static void adicionarColaboradores(Scanner scanner) {
        Colaboradores colaborador = new Colaboradores();
        ColaboradorDAO colaboradorDAO = new ColaboradorDAO();
        System.out.print("Nome: ");
        colaborador.setNome(scanner.nextLine());
        System.out.print("CPF: ");
        colaborador.setCpf(scanner.nextLine());
        System.out.print("Funcao: ");
        colaborador.setFuncao(scanner.nextLine());
        System.out.print("Salario: ");
        colaborador.setSalario(scanner.nextFloat());
        System.out.print("Vinculo Projeto: ");
        colaborador.setVinculoProjeto(scanner.nextLine());

        
        colaboradorDAO.inserirColaborador(colaborador);
        System.out.println("Cliente inserido com sucesso!");
    }

    private static void atualizarColaboradores(Scanner scanner) {
        ColaboradorDAO colaboradorDAO = new ColaboradorDAO();
        Colaboradores colaboradoratualizar = new Colaboradores();

        System.out.print("ID do Colaborador para atualizar: ");
        int idAtualizar = scanner.nextInt();
        scanner.nextLine();
        
        colaboradoratualizar.setId(idAtualizar);
        System.out.print("Nome: ");
        colaboradoratualizar.setNome(scanner.nextLine());
        System.out.print("CPF: ");
        colaboradoratualizar.setCpf(scanner.nextLine());
        System.out.print("Funcao: ");
        colaboradoratualizar.setFuncao(scanner.nextLine());
        System.out.print("Salario: ");
        colaboradoratualizar.setSalario(scanner.nextFloat());
        System.out.print("Vinculo Projeto: ");
        colaboradoratualizar.setVinculoProjeto(scanner.nextLine());
        
        colaboradorDAO.atualizarColaborador(colaboradoratualizar);
        System.out.println("Colaborador atualizado com sucesso!");
    }

    private static void listarColaboradores() {
        ColaboradorDAO colaboradorDAO = new ColaboradorDAO();
        List<Colaboradores> colaboradores = colaboradorDAO.listarTodos();
        for (Colaboradores colaborador : colaboradores) {
            System.out.println("ID: " + colaborador.getId() + " | Nome: " + colaborador.getNome() + " | Responsável: " + colaborador.getFuncao());
        }
    }

    private static void buscarColaboradores(Scanner scanner) {
        ColaboradorDAO colaboradorDAO = new ColaboradorDAO();
        System.out.print("Nome para buscar: ");
        String nomeBusca = scanner.nextLine();
        
        Colaboradores colaboradoresEncontrado = colaboradorDAO.buscarPorNome(nomeBusca);

        if (colaboradoresEncontrado != null) {
            System.out.println("ID: " + colaboradoresEncontrado.getId());
            System.out.println("Nome: " + colaboradoresEncontrado.getNome());
            System.out.println("Responsável: " + colaboradoresEncontrado.getFuncao());
        } else {
            System.out.println("Colaborador não encontrado.");
        }
    }

    private static void deletarColaboradores(Scanner scanner) {
        ColaboradorDAO colaboradorDAO = new ColaboradorDAO();
        System.out.print("ID do Colaborador para deletar: ");
        int idDeletar = scanner.nextInt();
        scanner.nextLine();
        colaboradorDAO.deletarColaborador(idDeletar);
        System.out.println("Colaborador deletado com sucesso!");
    }
        

    
    private static void adicionarProjeto(Scanner scanner) {
        Projeto novoProjeto = new Projeto();
        ProjetoDAO projetoDAO = new ProjetoDAO();
        System.out.print("Nome: ");
        novoProjeto.setNome(scanner.nextLine());
        System.out.print("Descricação: ");
        novoProjeto.setDescricaoCliente(scanner.nextLine());
        System.out.print("Equipe: ");
        novoProjeto.setEquipe(scanner.nextLine());
        System.out.print("Responsável: ");
        novoProjeto.setResponsavel(scanner.nextLine());
        System.out.print("Prazo: ");
        novoProjeto.setPrazo(scanner.nextLine());
        System.out.print("Orçamento: ");
        novoProjeto.setOrcamento(scanner.nextFloat());
        
        projetoDAO.inserirProjeto(novoProjeto);
        System.out.println("Projeto inserido com sucesso!");
    }

    private static void atualizarProjeto(Scanner scanner) {
        ProjetoDAO projetoDAO = new ProjetoDAO();
        Projeto projetoAtualizar = new Projeto();

        System.out.print("ID do Projeto para atualizar: ");
        int idAtualizar = scanner.nextInt();
        scanner.nextLine();
        
        projetoAtualizar.setIdProjeto(idAtualizar);
        System.out.print("Nome: ");
        projetoAtualizar.setNome(scanner.nextLine());
        System.out.print("Descricação: ");
        projetoAtualizar.setDescricaoCliente(scanner.nextLine());
        System.out.print("Equipe: ");
        projetoAtualizar.setEquipe(scanner.nextLine());
        System.out.print("Responsável: ");
        projetoAtualizar.setResponsavel(scanner.nextLine());
        System.out.print("Prazo: ");
        projetoAtualizar.setPrazo(scanner.nextLine());
        System.out.print("Orçamento: ");
        projetoAtualizar.setOrcamento(scanner.nextFloat());
        
        projetoDAO.atualizarProjeto(projetoAtualizar);
        System.out.println("Projeto atualizado com sucesso!");
    }

    private static void listarProjeto() {
        ProjetoDAO projetoDAO = new ProjetoDAO();
        List<Projeto> projetos = projetoDAO.listarTodos();
        for (Projeto projeto : projetos) {
            System.out.println("ID: " + projeto.getIdProjeto() + " | Nome: " + projeto.getNome() + " | Responsável: " + projeto.getResponsavel());
        }
    }

    private static void buscarProjeto(Scanner scanner) {
        ProjetoDAO projetoDAO = new ProjetoDAO();
        System.out.print("Nome para buscar: ");
        String nomeBusca = scanner.nextLine();
        
        Projeto clienteEncontrado = projetoDAO.buscarPorNome(nomeBusca);

        if (clienteEncontrado != null) {
            System.out.println("ID: " + clienteEncontrado.getIdProjeto());
            System.out.println("Nome: " + clienteEncontrado.getNome());
            System.out.println("Responsável: " + clienteEncontrado.getResponsavel());
        } else {
            System.out.println("Projeto não encontrado.");
        }
    }

    private static void deletarProjeto(Scanner scanner) {
        ProjetoDAO projetoDAO = new ProjetoDAO();
        System.out.print("ID do Projeto para deletar: ");
        int idDeletar = scanner.nextInt();
        scanner.nextLine();
        projetoDAO.deletarProjeto(idDeletar);
        System.out.println("Projeto deletado com sucesso!");
    }
    


    private static void adicionarCliente(Scanner scanner) {
        Cliente novoCliente = new Cliente();
        ClienteDAO clienteDAO = new ClienteDAO();
        System.out.print("Nome: ");
        novoCliente.setNome(scanner.nextLine());
        System.out.print("CPF: ");
        novoCliente.setCpf(scanner.nextLine());
        System.out.print("CNPJ: ");
        novoCliente.setCnpj(scanner.nextLine());
        System.out.print("Email: ");
        novoCliente.setEmail(scanner.nextLine());
        System.out.print("Telefone: ");
        novoCliente.setTelefone(scanner.nextLine());
        System.out.print("Endereço: ");
        novoCliente.setEndereco(scanner.nextLine());
        
        clienteDAO.inserirCliente(novoCliente);
        System.out.println("Cliente inserido com sucesso!");
    }

    private static void atualizarCliente(Scanner scanner) {
        ClienteDAO clienteDAO = new ClienteDAO();
        Cliente clienteAtualizar = new Cliente();

        System.out.print("ID do Cliente para atualizar: ");
        int idAtualizar = scanner.nextInt();
        scanner.nextLine();
        
        clienteAtualizar.setId(idAtualizar);
        System.out.print("Novo Nome: ");
        clienteAtualizar.setNome(scanner.nextLine());
        System.out.print("Novo CPF: ");
        clienteAtualizar.setCpf(scanner.nextLine());
        System.out.print("Novo CNPJ: ");
        clienteAtualizar.setCnpj(scanner.nextLine());
        System.out.print("Novo Email: ");
        clienteAtualizar.setEmail(scanner.nextLine());
        System.out.print("Novo Telefone: ");
        clienteAtualizar.setTelefone(scanner.nextLine());
        System.out.print("Novo Endereço: ");
        clienteAtualizar.setEndereco(scanner.nextLine());
        
        clienteDAO.atualizarCliente(clienteAtualizar);
        System.out.println("Cliente atualizado com sucesso!");
    }

    private static void listarClientes() {
        ClienteDAO clienteDAO = new ClienteDAO();
        List<Cliente> clientes = clienteDAO.listarTodos();
        for (Cliente cliente : clientes) {
            System.out.println("ID: " + cliente.getId() + " | Nome: " + cliente.getNome() + " | Telefone: " + cliente.getTelefone());
        }
    }

    private static void buscarCliente(Scanner scanner) {
        ClienteDAO clienteDAO = new ClienteDAO();
        System.out.print("Nome para buscar: ");
        String nomeBusca = scanner.nextLine();
        
        Cliente clienteEncontrado = clienteDAO.buscarPorNome(nomeBusca);

        if (clienteEncontrado != null) {
            System.out.println("ID: " + clienteEncontrado.getId());
            System.out.println("Nome: " + clienteEncontrado.getNome());
            System.out.println("Telefone: " + clienteEncontrado.getTelefone());
        } else {
            System.out.println("Cliente não encontrado.");
        }
    }

    private static void deletarCliente(Scanner scanner) {
        ClienteDAO clienteDAO = new ClienteDAO();
        System.out.print("ID do Cliente para deletar: ");
        int idDeletar = scanner.nextInt();
        scanner.nextLine();
        clienteDAO.deletarCliente(idDeletar);
        System.out.println("Cliente deletado com sucesso!");
    }
}
