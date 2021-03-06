package nyu.cs9053.yahtzeeserver;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.stereotype.Component;

import java.sql.*;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

@Component
public class DB {
  private final List<String> playerList;
  private static Connection conn;

  public DB() {
    playerList = new ArrayList<>();
    conn = null;
    establishConnection();
    PreparedStatement loadPlayerList = null;
    try {

      loadPlayerList = conn.prepareStatement("Select * from Player");

      ResultSet rset = loadPlayerList.executeQuery();

      while (rset.next()) {
        String playerName = rset.getObject(1).toString();
        String timeStamp = rset.getObject(23).toString();
        System.out.println(playerName + "        " + timeStamp);
        this.playerList.add(playerName + "        " + timeStamp);
      }

    } catch (SQLException | NullPointerException e) {
      e.printStackTrace();
    }  finally{
      if (loadPlayerList != null) {
        try {
          loadPlayerList.close();
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }
      }
      if (conn != null) {
        try {
          conn.close();
          System.out.println("Closing DB");
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }
      }
    }
  }

  private void establishConnection() {
    String currentDirectory = System.getProperty("user.dir");
    System.out.println("The current working directory is " + currentDirectory);
    PreparedStatement createTableStmt = null;
    try {

      Class.forName(("org.sqlite.JDBC"));
      conn = DriverManager.getConnection("jdbc:sqlite:yahtzee.db");
      System.out.println("Connected to DB");
      DatabaseMetaData meta = conn.getMetaData();
      ResultSet playerTable = meta.getTables(null, null, "Player", null);
      if (!playerTable.next()) {
        System.out.println("Creating Player table");
        String createTableSQL =
            "CREATE TABLE Player (PlayerName text, Aces int, Twos int, Threes int, Fours\n  int, Fives int, Sixes int, UpperSubtotal int, UpperBonus int, UpperTotal int,\n  ThreeKind int, FourKind int, FullHouse int, SmallStraight int, LargeStraight\n  int, Yahtzee int, Chance int, LowerSubtotal int, YahtzeeBonus int, TotalPoint\n  int, TurnNumber int, RollNumber int, TimeStored text, DiceSeq text, id\n  INTEGER PRIMARY KEY AUTOINCREMENT)";
        createTableStmt = conn.prepareStatement(createTableSQL);
        createTableStmt.execute();
      }

    } catch (SQLException | ClassNotFoundException e) {
      System.err.println("Fail connect to DB yahtzee");
    } finally{

      if (createTableStmt != null) {
        try {
          createTableStmt.close();
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }
      }
    }
  }

  public String loadPlayer(String name, String timeStored){
//    establishConnection();
    JSONObject jo = new JSONObject();

    try (PreparedStatement queryStatement = conn.prepareStatement("SELECT * FROM Player WHERE PlayerName=? AND TimeStored=?")) {
      queryStatement.setString(1, name);
      queryStatement.setString(2, timeStored);
      ResultSet rset = queryStatement.executeQuery();
      if (!rset.isClosed()) {

        jo.put("PlayerName", rset.getObject(1).toString());
        jo.put("Aces", rset.getObject(2).toString());
        jo.put("Twos", rset.getObject(3).toString());
        jo.put("Threes", rset.getObject(4).toString());
        jo.put("Fours", rset.getObject(5).toString());
        jo.put("Fives", rset.getObject(6).toString());
        jo.put("Sixes", rset.getObject(7).toString());
        jo.put("UpperSubtotal", rset.getObject(8).toString());
        jo.put("UpperBonus", rset.getObject(9).toString());
        jo.put("UpperTotal", rset.getObject(10).toString());
        jo.put("ThreeKind", rset.getObject(11).toString());
        jo.put("FourKind", rset.getObject(12).toString());
        jo.put("FullHouse", rset.getObject(13).toString());
        jo.put("SmallStraight", rset.getObject(14).toString());
        jo.put("LargeStraight", rset.getObject(15).toString());
        jo.put("Yahtzee", rset.getObject(16).toString());
        jo.put("Chance", rset.getObject(17).toString());
        jo.put("LowerSubtotal", rset.getObject(18).toString());
        jo.put("YahtzeeBonus", rset.getObject(19).toString());
        jo.put("TotalPoint", rset.getObject(20).toString());
        jo.put("TurnNumber", rset.getObject(21).toString());
        jo.put("RollNumber", rset.getObject(22).toString());
        jo.put("TimeStored", rset.getObject(23).toString());
        jo.put("DiceSeq", rset.getObject(24).toString());
        System.out.println("Respond a \n" + jo.toString());
        return jo.toString();
      } else {
        return "";
      }

    } catch (SQLException | JSONException e) {
      e.printStackTrace();
    } finally {
      if (conn != null) {
        try {
          conn.close();
        System.out.println("Closing DB");
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }

      }
    }
    return "";
  }

  public void savePlayer(Player p) {
    PreparedStatement queryStatement = null;
    try {
      establishConnection();
       queryStatement =
          conn.prepareStatement(
              "INSERT INTO Player(PlayerName, Aces, Twos, Threes, Fours, Fives, Sixes, UpperSubtotal, UpperBonus, UpperTotal, ThreeKind, FourKind, FullHouse, SmallStraight, LargeStraight, Yahtzee, Chance, LowerSubtotal, YahtzeeBonus, TotalPoint, TurnNumber, RollNumber, TimeStored, DiceSeq) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)");
      queryStatement.setString(1, p.getPlayerName());
      int[] playerIntProps = p.getIntProps();
      for (int i = 2; i < 23; i++) {
        queryStatement.setInt(i, playerIntProps[i - 2]);
      }
      String timeStr = Calendar.getInstance().getTime().toString();
      queryStatement.setString(23, timeStr);
      queryStatement.setString(24, p.getDiceSeq());
      queryStatement.executeUpdate();
      System.out.println("Saved " + p.getPlayerName() + " " +  timeStr + " to DB");
    } catch (SQLException e) {

      e.printStackTrace();
    } finally{
      if (queryStatement != null) {
        try {
          queryStatement.close();
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }
      }
      if (conn != null) {
        try {
          conn.close();
          System.out.println("Closing DB");
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }
      }
    }
  }

  public List<String> getPlayerList() {
    establishConnection();
    playerList.clear();
    PreparedStatement loadPlayerList = null;
    try {

      loadPlayerList = conn.prepareStatement("Select * from Player");

      ResultSet rset = loadPlayerList.executeQuery();

      while (rset.next()) {
        String playerName = rset.getObject(1).toString();
        String timeStamp = rset.getObject(23).toString();
        System.out.println(playerName + "        " + timeStamp);
        this.playerList.add(playerName + "        " + timeStamp);
      }

    } catch (SQLException | NullPointerException e) {
      e.printStackTrace();
    } finally{
      if (loadPlayerList != null) {
        try {
          loadPlayerList.close();
        } catch (SQLException throwables) {
          throwables.printStackTrace();
        }
      }
    }
    return this.playerList;
  }
}
