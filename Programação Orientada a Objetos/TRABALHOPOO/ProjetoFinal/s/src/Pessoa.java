public abstract class Pessoa {
    protected Integer id;
    protected String nome;
    protected String cpf;
    

    public Pessoa(){}

    public Pessoa(int id, String nome, String cpf) {
        this.setId(id);
        this.setNome(nome);
        this.setCpf(cpf);
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNome() {
        return this.nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getCpf() {
        return this.cpf;
    }

    public void setCpf(String cpf) {
        this.cpf = cpf;
    }
}

