import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ProjetoDAO {
    public void inserirProjeto(Projeto projeto) {
        String sql = "INSERT INTO projeto (nome, descricaocliente, equipe, responsavel, prazo, orcamento) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, projeto.getNome());
                stmt.setString(2, projeto.getDescricaoCliente());
                stmt.setString(3, projeto.getEquipe());
                stmt.setString(4, projeto.getResponsavel());
                stmt.setString(5, projeto.getPrazo());
                stmt.setFloat(6, projeto.getOrcamento());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void atualizarProjeto(Projeto projeto) {
        String sql = "UPDATE projeto SET nome = ?, descricaocliente = ?, equipe = ?, responsavel = ?, prazo = ?, orcamento = ?  WHERE idprojeto = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, projeto.getNome());
                stmt.setString(2, projeto.getDescricaoCliente());
                stmt.setString(3, projeto.getEquipe());
                stmt.setString(4, projeto.getResponsavel());
                stmt.setString(5, projeto.getPrazo());
                stmt.setFloat(6, projeto.getOrcamento());
                stmt.setInt(7, projeto.getIdProjeto());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void deletarProjeto(int id) {
        String sql = "DELETE FROM projeto WHERE id = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public List<Projeto> listarTodos() {
        List<Projeto> projetos = new ArrayList<>();
        String sql = "SELECT * FROM projeto";
        try (Connection conn = conexao.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Projeto projeto = new Projeto();
                projeto.setIdProjeto(rs.getInt("idprojeto"));
                projeto.setNome(rs.getString("nome"));
                projeto.setEquipe(rs.getString("equipe"));
                projeto.setResponsavel(rs.getString("responsavel"));
                projeto.setPrazo(rs.getString("prazo"));
                projeto.setStatus(rs.getString("status"));
                projeto.setOrcamento(rs.getFloat("orcamento"));
                projetos.add(projeto);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return projetos;
    }

    public Projeto buscarPorNome(String nome) {
        String sql = "SELECT * FROM projeto WHERE nome LIKE ?";
        Projeto projeto = null;
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, "%" + nome + "%");
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    projeto = new Projeto();
                    projeto.setIdProjeto(rs.getInt("idprojeto"));
                    projeto.setNome(rs.getString("nome"));
                    projeto.setEquipe(rs.getString("equipe"));
                    projeto.setResponsavel(rs.getString("responsavel"));
                    projeto.setPrazo(rs.getString("prazo"));
                    projeto.setStatus(rs.getString("status"));
                    projeto.setOrcamento(rs.getFloat("orcamento"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return projeto;
    }
}