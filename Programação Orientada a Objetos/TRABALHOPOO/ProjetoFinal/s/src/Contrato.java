public class Contrato {

    public enum StatusContrato {
        ATIVO, //0  
        RENEGOCIACAO, //1
        ENCERRADO //2
    }


    protected  Integer idContrato;
    protected  Integer idCliente;
    protected  String tiposervico;
    protected  String prazo; 
    protected  Float valor;
    protected  String status;

    public Contrato() {}

    public Contrato(Integer idcliente, String tiposervico, String prazo, Float valor) {
        this.setIdCliente(idcliente);
        this.setTipoServico(tiposervico);
        this.setPrazo(prazo);
        this.setStatus("ATIVO");
        this.setValor(valor);
    }

    public void setIdCliente(Integer idcliente) {
        this.idCliente = idcliente;
    }

    public Integer getIdCliente() {
        return this.idCliente;
    }

    public void setTipoServico(String tiposervico) {
        this.tiposervico = tiposervico;
    }

    public String getTipoServico() {
        return this.tiposervico;
    }

    public void setPrazo(String prazo) {
        this.prazo = prazo;
    }

    public String getPrazo() {
        return this.prazo;
    }

    public void setStatus(String status){
        this.status = status;
    }
    
    public String getStatus() {
        return this.status;
    }

    public void setValor(Float valor) {
        this.valor = valor;
    }

    public Float getValor() {
        return this.valor;
    }

    public Integer getIdContrato() {
        return this.idContrato;
    }

    public void setIdContrato(Integer idContrato) {
        this.idContrato = idContrato;
    }
}
