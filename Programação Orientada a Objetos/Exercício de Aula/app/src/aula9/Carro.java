package aula9;

public class Carro extends Automovel{
    private String cor, modelo;
    
    //Construtor
    public Carro(String nome, String fabricante, String cor, String modelo) {
        super(nome, fabricante);
        this.setCor(cor);
        this.setModelo(modelo);
    }

    public void setCor(String cor) {
        this.cor = cor;
    }

    public String getCor() {
        return this.cor;
    }

    public void setModelo(String modelo) {
        this.modelo = modelo;
    }
    
    public String getModelo() {
        return this.modelo;
    }
}
