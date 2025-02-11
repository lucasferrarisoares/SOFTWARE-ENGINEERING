import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ColaboradorDAO {
    public void inserirColaborador(Colaboradores colaborador) {
        String sql = "INSERT INTO colaboradores (nome, cpf, funcao, salario, vinculoprojeto) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, colaborador.getNome());
            stmt.setString(2, colaborador.getCpf());
            stmt.setString(3, colaborador.getFuncao());
            stmt.setFloat(4, colaborador.getSalario());
            stmt.setString(5, colaborador.getVinculoProjeto());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void atualizarColaborador(Colaboradores colaborador) {
        String sql = "UPDATE colaboradores SET nome = ?, cpf = ?, funcao = ?, salario = ?, vinculoprojeto = ? WHERE id = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, colaborador.getNome());
                stmt.setString(2, colaborador.getCpf());
                stmt.setString(3, colaborador.getFuncao());
                stmt.setFloat(4, colaborador.getSalario());
                stmt.setString(5, colaborador.getVinculoProjeto());
                stmt.setInt(6, colaborador.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void deletarColaborador(int id) {
        String sql = "DELETE FROM colaboradores WHERE id = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public List<Colaboradores> listarTodos() {
        List<Colaboradores> colaboradores = new ArrayList<>();
        String sql = "SELECT * FROM colaboradores";
        try (Connection conn = conexao.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Colaboradores colaborador = new Colaboradores();
                colaborador.setId(rs.getInt("id"));
                colaborador.setNome(rs.getString("nome"));
                colaborador.setCpf(rs.getString("cpf"));
                colaborador.setFuncao(rs.getString("funcao"));
                colaborador.setSalario(rs.getFloat("salario"));
                colaborador.setVinculoProjeto(rs.getString("vinculoprojeto"));
                colaboradores.add(colaborador);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return colaboradores;
    }

    public Colaboradores buscarPorNome(String nome) {
        String sql = "SELECT * FROM colaboradores WHERE nome LIKE ?";
        Colaboradores colaborador = null;
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, "%" + nome + "%");
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    colaborador = new Colaboradores();
                    colaborador.setId(rs.getInt("id"));
                    colaborador.setNome(rs.getString("nome"));
                    colaborador.setCpf(rs.getString("cpf"));
                    colaborador.setFuncao(rs.getString("funcao"));
                    colaborador.setSalario(rs.getFloat("salario"));
                    colaborador.setVinculoProjeto(rs.getString("vinculoprojeto"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return colaborador;
    }
}
