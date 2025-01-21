package mobilidade;

abstract class Automovel {
    protected Integer rodas, portas, veloAtual, cavalos;
    protected Boolean motorLigado;
    protected String cor;  

    //construtor
    public Automovel(String Cor, Integer cavalos) {
        this.setCor(Cor);
        this.setCavalos(cavalos); 
        this.setMotorLigado(false);
        this.setVeloAtual(0);
    }

    public abstract void TrocarCor(String cor);

    public abstract void TunarAutomovel(Integer quantidade);

    public abstract void Acelerar();

    public abstract void Diminuir();

    public abstract Double TrocarPneu();
    
    public void LigarMotor() {
        this.setMotorLigado(true);
    }
    public void DesligarMotor() {
        this.setMotorLigado(false);
    }

    public abstract void exibirEstado();

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
