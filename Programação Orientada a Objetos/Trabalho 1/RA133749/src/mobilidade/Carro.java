package mobilidade;

public class Carro extends Automovel{
    
    //Construtor
    public Carro(String Cor, Integer cavalos) {
        super(Cor, cavalos);
        this.setRodas(4);
        this.setPortas(4);
    }



    public void Acelerar() {
        if (this.getMotorLigado() == true) {
            System.out.println("==============");
            System.out.println("Acelerando Carro");
            this.setVeloAtual(this.getVeloAtual() + 10);
            System.out.println("\nVelocidade Atual e de: " + this.getVeloAtual());
            if (this.getVeloAtual() > 110) {
                System.out.println("\nVoce ultrapassou os 110km por hora!\n");
            } 
        } else {
            System.out.println("\nO carro esta desligado\n");
        }
    }

    public void Diminuir() {
        if (this.getVeloAtual() == 0) {
            System.out.println("==============");
            System.out.println("Freiando Carro");
            System.out.println("\nO carro esta parado!\n");
        } else {
            this.setVeloAtual(this.getVeloAtual() - 10);
        }
    }

    public void TrocarCor(String cor) {
        this.setCor(cor);
        System.out.println("\nSeu carro agora e "+ this.getCor());
    }

    public Double TrocarPneu() {
        Double x = this.getRodas() * 150.00;
        System.out.println("Voce gastou "+ x + " trocando os pneus do seu carro");
        return x;
    }

    public void exibirEstado() {
        if(this.getMotorLigado() == true) {
            System.out.println("Seu carro esta ligado");
        } else {
            System.out.println("Seu carro esta desligado");
        }
    }

    public void TunarAutomovel(Integer quantidade) {
        this.setCavalos(quantidade + this.getCavalos());
        System.out.println("Seu Carro Possui agora: "+ this.getCavalos() + " cavalos");
    }
}
