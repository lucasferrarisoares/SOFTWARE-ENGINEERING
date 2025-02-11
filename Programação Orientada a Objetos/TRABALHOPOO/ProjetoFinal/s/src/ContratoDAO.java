import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ContratoDAO {
    public void inserirContrato(Contrato contrato) {
        String sql = "INSERT INTO contratos (tiposervico, prazo, valor, statuscontrato, idcliente) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, contrato.getTipoServico());
                stmt.setString(2, contrato.getPrazo());
                stmt.setFloat(3, contrato.getValor());
                stmt.setString(4, contrato.getStatus());
                stmt.setInt(5, contrato.getIdCliente());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void atualizarContrato(Contrato contrato) {
        String sql = "UPDATE contratos SET tiposervico = ?, prazo = ?, valor = ?, statuscontrato = ?, idcliente = ?  WHERE idcontrato = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, contrato.getTipoServico());
                stmt.setString(2, contrato.getPrazo());
                stmt.setFloat(3, contrato.getValor());
                stmt.setString(4, contrato.getStatus());
                stmt.setInt(5, contrato.getIdCliente());
                stmt.setInt(6, contrato.getIdContrato());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void deletarContrato(int id) {
        String sql = "DELETE FROM contratos WHERE id = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public List<Contrato> listarTodos() {
        List<Contrato> contratos = new ArrayList<>();
        String sql = "SELECT * FROM contratos";
        try (Connection conn = conexao.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Contrato contrato = new Contrato();
                contrato.setIdContrato(rs.getInt("idcontrato"));
                contrato.setIdCliente(rs.getInt("idcliente"));
                contrato.setTipoServico(rs.getString("tiposervico"));
                contrato.setStatus(rs.getString("statuscontrato"));
                contrato.setPrazo(rs.getString("prazo"));
                contrato.setValor(rs.getFloat("valor"));
                contrato.setStatus(rs.getString("vinculoprojeto"));
                contratos.add(contrato);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return contratos;
    }

    public Contrato buscarPorNome(String nome) {
        String sql = "SELECT * FROM contratos WHERE nome LIKE ?";
        Contrato contrato = null;
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, "%" + nome + "%");
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    contrato = new Contrato();
                    contrato.setIdContrato(rs.getInt("idcontrato"));
                    contrato.setIdCliente(rs.getInt("idcliente"));
                    contrato.setTipoServico(rs.getString("tiposervico"));
                    contrato.setStatus(rs.getString("statuscontrato"));
                    contrato.setPrazo(rs.getString("prazo"));
                    contrato.setValor(rs.getFloat("valor"));
                    contrato.setStatus(rs.getString("vinculoprojeto"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return contrato;
    }
}
