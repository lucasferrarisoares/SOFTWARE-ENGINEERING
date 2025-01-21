package Pratica1;

public class Produto {
    

    private int id;
    private String nome;
    private String descricao;
    private int codBarras;
    private String categorias;
    private int quantidade;
    private double valor;

    public int getId() {
        return this.id;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return this.nome;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return this.descricao;
    }

    public void setCodBarras(int codbarras) {
        this.codBarras = codbarras;
    }

    public int getCodBarras() {
        return this.codBarras;
    }

    public void setCategorias(String categorias) {
        this.categorias = categorias;
    }

    public String getCategorias() {
        return this.categorias;
    }

    public void setQuantidade(int quantidade) {
        this.quantidade = quantidade;
    }

    public int getQuantidade() {
        return this.quantidade;
    }

    public void setValor(Double valor) {
        this.valor = valor;
    }

    public Double getValor() {
        return this.valor;
    }
}
