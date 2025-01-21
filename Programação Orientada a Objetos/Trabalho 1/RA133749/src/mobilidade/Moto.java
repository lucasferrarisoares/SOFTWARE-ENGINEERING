package mobilidade;

public class Moto extends Automovel {

    public Moto(String Cor, Integer cavalos) {
        super(Cor, cavalos);
        this.setRodas(2);
        this.setPortas(0);
    }

    public void Acelerar() {
        if (this.getMotorLigado() == true) {
            System.out.println("==============");
            System.out.println("Acelerando Moto");
            this.setVeloAtual(this.getVeloAtual() + 20);
            System.out.println("\nVelocidade Atual e de: " + this.getVeloAtual());
            if (this.getVeloAtual() > 110) {
                System.out.println("Voce ultrapassou os 110km por hora!");
            } 
        } else {
            System.out.println("A moto esta desligada");
        }
    }

    public void Diminuir() {
        if (this.getVeloAtual() == 0) {
            System.out.println("==============");
            System.out.println("Freiando Moto");
            System.out.println("A moto esta parada!");
        } else {
            this.setVeloAtual(this.getVeloAtual() - 20);
        }
    }

    public void TrocarCor(String cor) {
        this.setCor(cor);
        System.out.println("Sua moto agora e "+ this.getCor());
    }

    public Double TrocarPneu() {
        Double x = this.getRodas() * 150.00;
        System.out.println("Voce gastou "+ x + " trocando os pneus da sua moto");
        return x;
    }

    public void exibirEstado() {
        if(this.getMotorLigado() == true) {
            System.out.println("Sua moto esta ligada");
        } else {
            System.out.println("Sua moto esta desligada");
        }
    }

    public void TunarAutomovel(Integer quantidade) {
        this.setCavalos(quantidade + this.getCavalos());
        System.out.println("Sua moto possui agora: "+ this.getCavalos() + " cavalos");
    }
}
