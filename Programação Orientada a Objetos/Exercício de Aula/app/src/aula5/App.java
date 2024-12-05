package aula5;

public class App {
    public static void main(String[] args) {
        mesa mesa1 = new mesa();
        if(mesa1.adicionarMesa(4,"Madeira","Retangular")){
            System.out.println("Mesa Cadastrada "+mesa1.mostrarMesa());
        }else{
            System.out.println("Erro!");
        }
    }
}
