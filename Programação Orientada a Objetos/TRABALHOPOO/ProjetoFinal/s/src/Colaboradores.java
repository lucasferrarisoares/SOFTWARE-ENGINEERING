public class Colaboradores extends Pessoa {
    protected String funcao;
    protected Float salario;
    protected String vinculoProjeto;


    public Colaboradores(){}

    public Colaboradores(int id, String nome, String cpf, String funcao, Float salario, String vinculoProjeto) {
        super(id, nome, cpf);
        this.setFuncao(funcao);
        this.setSalario(salario);
        this.setVinculoProjeto(vinculoProjeto);
    }
    
    
    public void setFuncao(String funcao) {
        this.funcao = funcao;
    }

    public String getFuncao() {
        return this.funcao;
    }

    public void setSalario(Float salario) {
        this.salario = salario;
    }

    public Float getSalario() {
        return this.salario;
    }

    public void setVinculoProjeto(String vinculoProjeto) {
        this.vinculoProjeto = vinculoProjeto;
    }

    public String getVinculoProjeto() {
        return this.vinculoProjeto;
    }
}
