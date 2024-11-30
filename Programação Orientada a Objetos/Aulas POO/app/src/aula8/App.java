package aula8;

public class App {
    public static void main(String[] args) {
        ContaCorrente cliente1 = new ContaCorrente("3284-0", "12456-8", "JosÃ©", 1500.05, 500.00);

        // Realizando operações.
        cliente1.depositar(500.25);
        String extrato = cliente1.exibirExtrato();
        System.out.println(extrato);

        cliente1.retirar(1000.25);
        extrato = cliente1.exibirExtrato();
        System.out.println(extrato);

    }
}
