import java.sql.*;
import java.util.UUID;

//java -classpath bqjava/*:. Wr...

public class WriteToBigQuery {

    public static void main(String[] args) throws SQLException {
        String projectId = "nimesa-1549405366717";
        String datasetName = "dev";
        String tableName = "test_jdbc";
        String connectionUrl = "jdbc:bigquery://https://www.googleapis.com/bigquery/v2:443;ProjectId=" + projectId + ";OAuthType=3;EnableHighThroughputAPI=1";

        String insertQuery = "INSERT INTO `" + datasetName + "." + tableName + "` (column1, column2) VALUES (?, ?)";

        try (Connection connection = DriverManager.getConnection(connectionUrl);
             PreparedStatement statement = connection.prepareStatement(insertQuery)) {

            // statement.setString(1, "value1");
            // statement.setInt(2, 42);

            // int rowsInserted = statement.executeUpdate();
            // System.out.println(rowsInserted + " row(s) inserted successfully.");

            for(int i = 0; i < 10; i++){
                String uuid = UUID.randomUUID().toString();
                statement.setString(1, uuid);
                statement.setInt(2, i);
    
                statement.addBatch();
            }

            int[] rowsInserted = statement.executeBatch();
            System.out.println(rowsInserted + " row(s) inserted successfully.");
            
        }
    }
}
