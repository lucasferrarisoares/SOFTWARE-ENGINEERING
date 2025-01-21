package Pratica1;

import java.sql.*;
import javax.management.RuntimeErrorException;

public class ProdutoDAO {
    
    private Connection con;

    public ProdutoDAO() {
        this.con = new ConnectionFactor
    }

    public void cadastrar(Produto prod) {
        String sql = "insert into produto "
        + "(nome, descricao, codBarras, categoria, quantidade, valor) "
        + "values (?,?,?,?,?,?)";

        try {
            PreparedStatement stmt = con.prepareStatement(sql);
            stmt.setString(1, prod.getNome());
            stmt.setString(2, prod.setDescricao());
            stmt.setInt(3, prod.getCodBarras());
            stmt.setString(4, prod.getCategoria);
            stmt.setInt(5, prod.getQuantidade());
            stmt.setDouble(6, prod.getValor());

            stmt.execute();
            stmt.close();
            
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
