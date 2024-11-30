package aula8;

public class ContaCorrente extends Conta {
    private double limite;

    //Construtor
    public ContaCorrente(String agencia, String numeroConta, String titular, Double saldo, Double limite) {
        super(agencia,numeroConta,titular,saldo); 
        this.setLimite(limite);
    }
    
    public String exibirExtrato(){
        return String.format(
            "{ \"Titular\": \"%s\", \"Agencia\": \"%s\", \"Conta\": \"%s\", \"Saldo\": \"%.2f\" }",
            this.getTitular(), this.getAgencia(), this.getNumeroConta(), this.getSaldo()
        );

    }

    public boolean retirar(double valor) {
        if(valor>0 && (this.getSaldo() >= valor)) {
            return true;
        } else {
            return false;
        }
    }

    protected void setLimite(Double limite) {
        this.limite=limite;
    }
    protected Double getLimite() {
        return this.limite;
    }
}
