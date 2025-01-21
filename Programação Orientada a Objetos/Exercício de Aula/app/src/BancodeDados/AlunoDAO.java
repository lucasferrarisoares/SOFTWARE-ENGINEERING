package BancodeDados;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class AlunoDAO {
    public void inserirAluno(Aluno aluno) {
        String sql = "INSERT INTO aluno (nome, matricula, curso, email, telefone, data_nascimento, endereco) VALUES (?, ?, ?, ?, ?, ?, ?)";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, aluno.getNome());
            stmt.setString(2, aluno.getMatricula());
            stmt.setString(3, aluno.getCurso());
            stmt.setString(4, aluno.getEmail());
            stmt.setString(5, aluno.getTelefone());
            stmt.setString(6, aluno.getDataNascimento());
            stmt.setString(7, aluno.getEndereco());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void atualizarAluno(Aluno aluno) {
        String sql = "UPDATE aluno SET nome = ?, matricula = ?, curso = ?, email = ?, telefone = ?, data_nascimento = ?, endereco = ? WHERE id = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, aluno.getNome());
            stmt.setString(2, aluno.getMatricula());
            stmt.setString(3, aluno.getCurso());
            stmt.setString(4, aluno.getEmail());
            stmt.setString(5, aluno.getTelefone());
            stmt.setString(6, aluno.getDataNascimento());
            stmt.setString(7, aluno.getEndereco());
            stmt.setInt(8, aluno.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void deletarAluno(int id) {
        String sql = "DELETE FROM aluno WHERE id = ?";
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public List<Aluno> listarTodos() {
        List<Aluno> alunos = new ArrayList<>();
        String sql = "SELECT * FROM aluno";
        try (Connection conn = conexao.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Aluno aluno = new Aluno();
                aluno.setId(rs.getInt("id"));
                aluno.setNome(rs.getString("nome"));
                aluno.setMatricula(rs.getString("matricula"));
                aluno.setCurso(rs.getString("curso"));
                aluno.setEmail(rs.getString("email"));
                aluno.setTelefone(rs.getString("telefone"));
                aluno.setDataNascimento(rs.getString("data_nascimento"));
                aluno.setEndereco(rs.getString("endereco"));
                alunos.add(aluno);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return alunos;
    }

    public Aluno buscarPorNome(String nome) {
        String sql = "SELECT * FROM aluno WHERE nome LIKE ?";
        Aluno aluno = null;
        try (Connection conn = conexao.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, "%" + nome + "%");
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    aluno = new Aluno();
                    aluno.setId(rs.getInt("id"));
                    aluno.setNome(rs.getString("nome"));
                    aluno.setMatricula(rs.getString("matricula"));
                    aluno.setCurso(rs.getString("curso"));
                    aluno.setEmail(rs.getString("email"));
                    aluno.setTelefone(rs.getString("telefone"));
                    aluno.setDataNascimento(rs.getString("data_nascimento"));
                    aluno.setEndereco(rs.getString("endereco"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return aluno;
    }
}

