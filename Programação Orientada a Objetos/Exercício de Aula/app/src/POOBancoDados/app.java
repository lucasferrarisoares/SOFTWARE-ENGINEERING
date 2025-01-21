package POOBancoDados;

import java.net.URL;
import java.sql.*;

public class app {
    public static void main(String[] args) throws SQLException {
        Connection con= DriverManager.getConnection(
            url:"jdbc:mysql://localhost/universitario", user:"root",password:"");
        System.out.println("conectado");
        
    }
}
