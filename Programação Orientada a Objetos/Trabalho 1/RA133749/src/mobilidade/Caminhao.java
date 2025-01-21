package mobilidade;

public class Caminhao extends Automovel {


    public Caminhao(String Cor, Integer cavalos, Integer rodas) {
        super(Cor, cavalos);
        this.setRodas(rodas);
        this.setPortas(2);
    }

    public void Acelerar() {
        
        if (this.getMotorLigado() == true) {
            System.out.println("==============");
            System.out.println("Acelerando Caminhao");
            this.setVeloAtual(this.getVeloAtual() + 5);
            System.out.println("Velocidade atual e de: " + this.getVeloAtual());
            if (this.getVeloAtual() > 80) {
                System.out.println("Voce ultrapassou os 80km por hora!\n");
            } 
        } else {
            System.out.println("O caminhao está desligado\n");
        }
    }

    public void Diminuir() {
        if (this.getVeloAtual() == 0) {
            System.out.println("==============");
            System.out.println("Freiando caminhao");
            System.out.println("O caminhao esta parado!\n");
        } else {
            this.setVeloAtual(this.getVeloAtual() - 10);
        }
    }

    public void TrocarCor(String cor) {
        this.setCor(cor);
        System.out.println("Seu caminhao agora e "+ this.getCor());
    }

    public Double TrocarPneu() {
        Double x = this.getRodas() * 150.00;
        System.out.println("Voce gastou "+ x + " trocando os pneus do seu Caminhao");
        return x;
    }

    public void exibirEstado() {
        if(this.getMotorLigado() == true) {
            System.out.println("Seu caminhao esta ligado\n");
        } else {
            System.out.println("Seu caminhao esta desligado\n");
        }
    }

    public void TunarAutomovel(Integer quantidade) {
        this.setCavalos(quantidade + this.getCavalos());
        System.out.println("Seu caminhao possui agora: "+ this.getCavalos() + " cavalos");
    }
}
