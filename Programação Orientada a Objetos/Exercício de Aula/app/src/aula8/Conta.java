package aula8;

public class Conta {

    protected String agencia, numeroConta, titular;
    protected Double saldo;

    //Construtor
    public Conta(String agencia, String numeroConta, String titular, Double saldo) {
        this.setAgencia(agencia);
        this.setNumeroConta(numeroConta);
        this.setTitular(titular);
        this.setSaldo(saldo);
    }

    public boolean depositar(Double valor) {
        if(valor > 0) {
            this.setSaldo(this.getSaldo() + valor);
            return true;
        } else {
            return false;
        }
    }

    public boolean sacar(Double valor) {
        if(valor > 0) {
            if(this.getSaldo() >= valor) {
                this.setSaldo(this.getSaldo() - valor);
                return true;
            } else {
                System.out.printf("Saldo insuficiente\n");
                return false;
            }
        } else {
            System.out.printf("Não é possível sacar um valor nefativo\n");
            return false;
        }
    }




    protected  void setAgencia(String agencia) {
        this.agencia=agencia;
    }
    protected  String getAgencia() {
        return this.agencia;
    }
    protected  void setNumeroConta(String numeroConta) {
        this.numeroConta=numeroConta;
    }
    protected  String getNumeroConta() {
        return this.numeroConta;
    }
    protected void setTitular(String titular) {
        this.titular=titular;
    }
    protected String getTitular() {
        return this.titular;
    }
    protected void setSaldo(Double saldo) {
        this.saldo=saldo;
    }
    protected Double getSaldo() {
        return this.saldo;
    }

}
