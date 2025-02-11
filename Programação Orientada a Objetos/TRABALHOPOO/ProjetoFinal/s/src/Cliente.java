
public class Cliente extends Pessoa {
    protected String cnpj;
    protected String telefone;
    protected String email;
    protected String endereco;
    protected String datacadastro;


    public Cliente(){}

    public Cliente(int id, String nome, String cpf, String cnpj, String telefone, String email, String endereco, String datacadastro) {
        super(id, nome, cpf);
        this.setCnpj(cnpj);
        this.setTelefone(telefone);
        this.setEmail(email);
        this.setEndereco(endereco);
        this.setDatacadastro(datacadastro);
    }
    
    
    public void setCnpj(String cnpj) {
        this.cnpj = cnpj;
    }

    public String getCnpj() {
        return this.cnpj;
    }

    public void setTelefone(String telefone) {
        this.telefone = telefone;
    }

    public String getTelefone() {
        return this.telefone;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEndereco(String endereco) {
        this.endereco = endereco;
    }

    public String getEndereco() {
        return this.endereco;
    }

    public void setDatacadastro(String datacadastro) {
        this.datacadastro = datacadastro;
    }

    public String getDatacadastro() {
        return this.datacadastro;
    }
}