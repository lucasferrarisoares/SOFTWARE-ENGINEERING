package aula9;

public class Automovel {
    protected String nome, fabricante;

    public Automovel(String nome, String fabricante) {
        this.setNome(nome);
        this.setFabricante(fabricante);   
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return this.nome;
    }

    public void setFabricante(String fabricante) {
        this.fabricante = fabricante;
    }
    
    public String getFabricante() {
        return this.fabricante;
    }
}
