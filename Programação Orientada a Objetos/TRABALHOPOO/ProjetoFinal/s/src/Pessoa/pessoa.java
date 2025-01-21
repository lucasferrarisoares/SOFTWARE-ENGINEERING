package Pessoa;

import lombok.*;


@Getter
@Setter
public abstract class Pessoa {
    private int id;
    private String nome;
    private String cpf;
    

    public Pessoa(){}

    public Pessoa(int id, String nome, String cpf) {
        this.id = id;
        this.nome = nome;
        this.cpf = cpf;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getCpf() {
        return this.cpf;
    }

    public void setMatricula(String cpf) {
        this.Cpf = cpf;
    }
}

