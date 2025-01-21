package BancodeDados;

import java.util.List;
import java.util.Scanner;

public class APPScanner {
     public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        AlunoDAO alunoDAO = new AlunoDAO();
        int opcao;

        do {
            System.out.println("\n=== Sistema de Gerenciamento de Alunos ===");
            System.out.println("1 - Inserir Aluno");
            System.out.println("2 - Atualizar Aluno");
            System.out.println("3 - Listar Todos os Alunos");
            System.out.println("4 - Buscar Aluno por Nome");
            System.out.println("5 - Deletar Aluno");
            System.out.println("6 - Sair");
            System.out.print("Escolha uma opcao: ");
            opcao = scanner.nextInt();
            scanner.nextLine(); // Limpa o buffer

            switch (opcao) {
                case 1:
                    Aluno novoAluno = new Aluno();
                    System.out.print("Nome: ");
                    novoAluno.setNome(scanner.nextLine());
                    System.out.print("Matricula: ");
                    novoAluno.setMatricula(scanner.nextLine());
                    System.out.print("Curso: ");
                    novoAluno.setCurso(scanner.nextLine());
                    System.out.print("Email: ");
                    novoAluno.setEmail(scanner.nextLine());
                    System.out.print("Telefone: ");
                    novoAluno.setTelefone(scanner.nextLine());
                    System.out.print("Data de Nascimento (YYYY-MM-DD): ");
                    novoAluno.setDataNascimento(scanner.nextLine());
                    System.out.print("Endereco: ");
                    novoAluno.setEndereco(scanner.nextLine());
                    alunoDAO.inserirAluno(novoAluno);
                    System.out.println("Aluno inserido com sucesso!");
                    break;
                case 2:
                    System.out.print("ID do Aluno para atualizar: ");
                    int idAtualizar = scanner.nextInt();
                    scanner.nextLine();
                    Aluno alunoAtualizar = new Aluno();
                    alunoAtualizar.setId(idAtualizar);
                    System.out.print("Novo Nome: ");
                    alunoAtualizar.setNome(scanner.nextLine());
                    System.out.print("Nova Matricula: ");
                    alunoAtualizar.setMatricula(scanner.nextLine());
                    System.out.print("Novo Curso: ");
                    alunoAtualizar.setCurso(scanner.nextLine());
                    System.out.print("Novo Email: ");
                    alunoAtualizar.setEmail(scanner.nextLine());
                    System.out.print("Novo Telefone: ");
                    alunoAtualizar.setTelefone(scanner.nextLine());
                    System.out.print("Nova Data de Nascimento (YYYY-MM-DD): ");
                    alunoAtualizar.setDataNascimento(scanner.nextLine());
                    System.out.print("Novo Endereco: ");
                    alunoAtualizar.setEndereco(scanner.nextLine());
                    alunoDAO.atualizarAluno(alunoAtualizar);
                    System.out.println("Aluno atualizado com sucesso!");
                    break;
                case 3:
                    List<Aluno> alunos = alunoDAO.listarTodos();
                    for (Aluno aluno : alunos) {
                        System.out.println(aluno.getId() + " - " + aluno.getNome() + " - " + aluno.getCurso());
                    }
                    break;
                case 4:
                    System.out.print("Nome para buscar: ");
                    String nomeBusca = scanner.nextLine();
                    Aluno alunoEncontrado = alunoDAO.buscarPorNome(nomeBusca);
                    if (alunoEncontrado != null) {
                        System.out.println("ID: " + alunoEncontrado.getId());
                        System.out.println("Nome: " + alunoEncontrado.getNome());
                        System.out.println("Curso: " + alunoEncontrado.getCurso());
                    } else {
                        System.out.println("Aluno nao encontrado.");
                    }
                    break;
                case 5:
                    System.out.print("ID do Aluno para deletar: ");
                    int idDeletar = scanner.nextInt();
                    scanner.nextLine();
                    alunoDAO.deletarAluno(idDeletar);
                    System.out.println("Aluno deletado com sucesso!");
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
