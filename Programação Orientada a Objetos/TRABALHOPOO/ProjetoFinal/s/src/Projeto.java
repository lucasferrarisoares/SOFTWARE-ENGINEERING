public class Projeto {    
    protected Integer idProjeto;
    protected String nome; 
    protected String descrircaoCliente; 
    protected String equipe; 
    protected String responsavel; 
    protected String prazo;
    protected String status; 
    protected Float orcamento;

    public Projeto() {}

    public Projeto(String nome, String descricaoCliente, String equipe, String responsavel, String prazo, Float orcamento) {
        this.setNome(nome);
        this.setDescricaoCliente(descricaoCliente);
        this.setEquipe(equipe);
        this.setResponsavel(responsavel);
        this.setPrazo(prazo);
        this.setStatus("ANDAMENTO");
        this.setOrcamento(orcamento);
    }

    public void setIdProjeto(Integer idProjeto) {
        this.idProjeto = idProjeto;
    }

    public Integer getIdProjeto() {
        return this.getIdProjeto();
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return this.nome;
    }

    public void setDescricaoCliente(String descricaoCliente) {
        this.descrircaoCliente = descricaoCliente;
    }

    public String getDescricaoCliente() {
        return this.descrircaoCliente;
    }

    public void setEquipe(String equipe) {
        this.equipe = equipe;
    }

    public String getEquipe() {
        return this.equipe;
    }

    public void setResponsavel(String responsavel) {
        this.responsavel = responsavel;
    }

    public String getResponsavel() {
        return this.responsavel;
    }

    public void setPrazo(String prazo) {
        this.prazo = prazo;
    }

    public String getPrazo() {
        return this.prazo;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getStatus() {
        return this.status;
    }

    public void setOrcamento(Float orcamento) {
        this.orcamento = orcamento;
    }

    public Float getOrcamento() {
        return this.orcamento;
    }

}
