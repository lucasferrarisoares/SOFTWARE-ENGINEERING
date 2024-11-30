package aula6;

public class App {
    public static void main(String[] args) {
        Fisica pessoa1 = new Fisica("Rua João Batista Rezende N 46","carlos.luz@uem.br", "2024-11-08", "Carlos Danilo", "059.888.999-77");
        System.out.println("\n"+pessoa1);
        
        Juridica pessoa2 = new Juridica("Rua João Batista Rezende N 46","carlos.luz@uem.br", "2024-11-08", "LUZ E SOL LTAD", "99.252.252/0001-96");
        System.out.println("\n"+pessoa2);        
        
        Pessoa pessoa3 = new Pessoa("Rua João Batista Rezende N 46","carlos.luz@uem.br", "2024-11-08");
        System.out.println("\n"+pessoa3);

    }
}
