package nyu.cs9053.yahtzeeserver;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
@RestController
public class YahtzeeserverApplication extends SpringBootServletInitializer {
  private final DB db = new DB();

  @RequestMapping(value = "/", method = RequestMethod.POST, produces = "application/json")
  public void saveToDB(@RequestBody String body, HttpServletRequest request) throws JSONException {
    Player p = new Player();
    JSONObject jo = new JSONObject(body);
    System.out.println("Receive Post request to save a game:\n" + jo.toString());
    p.setPlayerName(jo.getString("PlayerName"));
    p.setAces(jo.getInt("Aces"));
    p.setTwos(jo.getInt("Twos"));
    p.setThrees(jo.getInt("Threes"));
    p.setFours(jo.getInt("Fours"));
    p.setFives(jo.getInt("Fives"));
    p.setSixes(jo.getInt("Sixes"));
    p.setUpperSubtotal(jo.getInt("UpperSubtotal"));
    p.setUpperBonus(jo.getInt("UpperBonus"));
    p.setUpperTotal(jo.getInt("UpperTotal"));

    p.setThreeKind(jo.getInt("ThreeKind"));
    p.setFourKind(jo.getInt("FourKind"));
    p.setFullHouse(jo.getInt("FullHouse"));
    p.setSmallSt(jo.getInt("SmallStraight"));
    p.setLargeSt(jo.getInt("LargeStraight"));
    p.setYahtzee(jo.getInt("Yahtzee"));
    p.setChance(jo.getInt("Chance"));
    p.setLowerSubtotal(jo.getInt("LowerSubtotal"));
    p.setLowerBonus(jo.getInt("YahtzeeBonus"));
    p.setTurnNumber(jo.getInt("TurnNumber"));
    p.setRollNumber(jo.getInt("RollNumber"));
    p.setLowerTotal(jo.getInt("TotalPoint"));
    p.setDiceSeq(jo.getString("DiceSeq"));
    System.out.println("There are " + jo.length() + " properties");

    db.savePlayer(p);
  }

  @RequestMapping(
      value = "/{player}",
      method = RequestMethod.GET,
      produces = "application/json")
  public String loadPlayer(@PathVariable String player){
    String[] queryPlayer = player.split(":::::");
    String playerName = queryPlayer[0];
    String timeStored = queryPlayer[1];
    System.out.println("Received a GET request for " + playerName +" at time " + timeStored);
    return db.loadPlayer(playerName, timeStored);
  }

  @RequestMapping(value = "/", method = RequestMethod.GET, produces = "application/json")
  public String loadPlayerList() {
    System.out.println("Received a GET request for all saved games");
    String names = "";

    for (String p : db.getPlayerList()) {
      System.out.println(p);
      names += p + "\n";
    }
    return  names.equals("") ? "" : names;
  }

  public static void main(String[] args) {
    SpringApplication.run(YahtzeeserverApplication.class, args);
  }
}
