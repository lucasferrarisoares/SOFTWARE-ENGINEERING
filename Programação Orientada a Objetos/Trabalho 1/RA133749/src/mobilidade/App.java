package mobilidade;

public class App {
    public static void main(String[] args) {
        Carro ferrari = new Carro("vermelho", 220);
        Moto mobilete = new Moto("Azul", 100);
        Caminhao mionete = new Caminhao("Preto", 150, 8);

        System.out.println("==============");
        System.out.println("Ligando Carro");
        ferrari.LigarMotor();
        System.out.println("==============");
        System.out.println("Ligando Moto");
        mobilete.LigarMotor();


        ferrari.Acelerar();
        ferrari.Acelerar();
        mobilete.Acelerar();
        mobilete.Acelerar();
        mionete.Acelerar();
        mionete.Acelerar();

        mionete.TrocarPneu();
        ferrari.exibirEstado();
        mobilete.exibirEstado();
        mionete.exibirEstado();

        mobilete.TunarAutomovel(50);
        mionete.TrocarCor("Branco");

    }
}
