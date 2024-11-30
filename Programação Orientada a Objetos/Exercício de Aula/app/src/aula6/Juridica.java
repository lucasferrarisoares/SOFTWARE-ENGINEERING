package aula6;

public class Juridica extends Pessoa {
    private String razaoSocial;
    private String CNPJ;

    public Juridica(String endereco, String email, String dataCadastro, String razaoSocial, String CNPJ){
        super(endereco, email, dataCadastro);
        this.setRazaoSocial(razaoSocial);
        this.setCNPJ(CNPJ);
    }

    
    private boolean setRazaoSocial (String razaoSocial){
        if(razaoSocial != null && !razaoSocial.isEmpty()){
            this.razaoSocial=razaoSocial;
            return true;
        }
        return false;
    }
    private boolean setCNPJ (String CNPJ){
        if(CNPJ != null && !CNPJ.isEmpty()){
            this.CNPJ=CNPJ;
            return true;
        }
        return false;
    }
    @Override
    public String toString(){        
        return "Razão Social: "+razaoSocial+
        ", CNPJ: "+CNPJ+
        ", Pessoa: "+endereco+
        ", Email: "+email+
        "Data de Cadastro: "+dataCadastro;
    }
}
