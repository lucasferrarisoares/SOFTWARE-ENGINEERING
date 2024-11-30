package aula6;

public class Pessoa {
    protected String endereco ;
    protected String email ;
    protected String dataCadastro;

    public Pessoa(String endereco, String email, String dataCadastro){
        this.setEndereco(endereco);
        this.setEmail(email);
        this.setdataCadastro(dataCadastro);
    }
    private boolean setEndereco (String endereco){
        if(endereco != null && !endereco.isEmpty()){
            this.endereco=endereco;
            return true;
        }
        return false;
    }
    private boolean setEmail (String email){
        if(email != null && !email.isEmpty()){
            this.email=email;
            return true;
        }
        return false;
    }
    private boolean setdataCadastro (String dataCadastro){
        if(dataCadastro != null && !dataCadastro.isEmpty()){
            this.dataCadastro=dataCadastro;
            return true;
        }
        return false;
    }

    @Override
    public String toString(){
        return "Endereço: "+this.endereco+
        ", Email: "+this.email+
        "Data de Cadastro: "+this.dataCadastro;
    }
}
