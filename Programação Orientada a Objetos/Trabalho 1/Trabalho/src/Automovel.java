
public abstract class Automovel {
    protected Integer rodas, portas, veloAtual, cavalos;
    protected Boolean motorLigado;
    protected String cor;  

    //construtor
    public Automovel(String Cor, String cavalos, Boolean motorLigado, Integer rodas, Integer portas) {
        this.setCor(Cor);
        this.setCavalos(cavalos); 
        this.setMotorLigado(false);
        this.setRodas(rodas);
        this.setPortas(portas);
        this.setVeloAtual(0);
    }

    public void TrocarCor(String cor) {
        this.setCor(cor);
    }

    public void TunarAutomovel(Integer quantidade) {
        this.setCavalos(quantidade + this.getCavalos());
    }

    public void Acelerar() {

    }

    public void Diminuir() {
    
    }

    public Double TrocarPneu() {
        return this.getRodas() * 150.00;
    }

    public void LigarMotor() {
        this.setMotorLigado(true);
    }
    public void DesligarMotor() {
        this.setMotorLigado(false);
    }

    public void exibirEstado() {
        if(this.getMotorLigado() == true) {
            System.out.println("Seu automovel está ligado");
        } else {
            System.out.println("Seu automovel está desligado");
        }
    }

    public void setMotorLigado(Boolean motorLigado) {
        this.motorLigado = motorLigado;
    }
    public boolean getMotorLigado() {
        return this.motorLigado;
    }

    public void setCavalos(Integer cavalos) {
        this.cavalos = cavalos;
    }

    public Integer getCavalos() {
        return this.cavalos;
    }

    public void setCor(String cor) {
        this.cor = cor;
    }
    
    public String getCor() {
        return this.cor;
    }

    public Integer getRodas(){
        return this.rodas;
    }

    public void setRodas(Integer rodas){
        this.rodas = rodas;
    }

    public void setPortas(Integer portas) {
        this.portas = portas;
    }

    public Integer getPortas() {
        return this.portas;
    }

    public Integer getVeloAtual() {
        return this.veloAtual;
    }

    public void setVeloAtual(Integer veloAtual) {
        this.veloAtual = veloAtual;
    }

}
