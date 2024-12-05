package aula4;


public class Funcionarios {
    public String nome;
    private String email; 
    private double salario;

    //construtores
    
    public Funcionarios() {}
    
    //Gets//Sets
    public void setEmail(String email) {
        this.email = email;
    }

    public String getEmail() {
        return this.email;
    }

    public void setSalario(Double salario) {
        this.salario = salario;
    }

    public Double getSalario() {
        return this.salario;
    }

    @Override
    public String toString(){
        return "Dados do Funcionário, Nome: " + nome + ", email: " +email+ ", salário: " + salario;
    }
}