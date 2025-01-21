package cliente;

import lombok.*;


@Getter
@Setter
public class cliente extends pessoa {
    private String cnpj;
    private String telefone;
    private String email;
    private String endereco;
    private String datacadastro;

    public Cliente(int d, String nome, String cpf, String cnpj, String telefone, String email, String endereco, String datacadastro) {
        super(id, nome, cpf);
        this.cnpj = cnpj;
        this.telefone = telefone;
        this.email = email;
        this.endereco = endereco;
        this.datacadastro = datacadastro;
    }

}
