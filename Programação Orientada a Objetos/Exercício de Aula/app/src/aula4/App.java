package aula4;

public class App {
    public static void main(String[] args) throws Exception {
       Funcionarios fun1 = new Funcionarios();

       fun1.nome = "Lucas Ferrari";
       fun1.setEmail("lucasferrarisoares@gmail.com");
       fun1.setSalario(15000.00);

       System.out.println(fun1.toString());
    }
}
