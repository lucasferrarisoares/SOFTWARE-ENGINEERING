package aula6;

public class Fisica extends Pessoa {
    private String nome;
    private String CPF;

    public Fisica(String endereco, String email, String dataCadastro, String nome, String CPF){
        super(endereco, email, dataCadastro);
        this.setNome(nome);
        this.setCPF(CPF);
    }
    private boolean setNome (String nome){
        if(nome != null && !nome.isEmpty()){
            this.nome=nome;
            return true;
        }
        return false;
    }
    private boolean setCPF (String CPF){
        if(CPF != null && !CPF.isEmpty()){
            this.CPF=CPF;
            return true;
        }
        return false;
    }
    @Override
    public String toString(){        
        return "Nome: "+nome+
        ", CPF: "+CPF+
        ", Pessoa: "+endereco+
        ", Email: "+email+
        "Data de Cadastro: "+dataCadastro;
    }
}
