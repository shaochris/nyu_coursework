package nyu.cs9053.yahtzeeserver;

import org.springframework.stereotype.Component;

@Component
public class Player {
  private String playerName;
  private int aces;
  private int twos;
  private int threes;
  private int fours;
  private int fives;
  private int sixes;
  private int upperSubtotal;
  private int upperBonus;
  private int upperTotal;

  private int threeKind;
  private int fourKind;
  private int fullHouse;
  private int smallSt;
  private int largeSt;
  private int yahtzee;
  private int chance;
  private int lowerSubtotal;
  private int lowerBonus;
  private int lowerTotal;

  private int turnNumber;
  private int rollNumber;
  private int id;
  private String timeStored;
  private String diceSeq;

  public void setPlayerIntProps(int[] intProps) {
    aces = intProps[0];
    twos = intProps[1];
    threes = intProps[2];
    fours = intProps[3];
    fives = intProps[4];
    sixes = intProps[5];
    upperSubtotal = intProps[6];
    upperBonus = intProps[7];
    upperTotal = intProps[8];

    threeKind = intProps[9];
    fourKind = intProps[10];
    fullHouse = intProps[11];
    smallSt = intProps[12];
    largeSt = intProps[13];
    yahtzee = intProps[14];
    chance = intProps[15];
    lowerSubtotal = intProps[16];
    lowerBonus = intProps[17];
    lowerTotal = intProps[18];
    turnNumber = intProps[19];
    rollNumber = intProps[20];
  }

  public int[] getIntProps() {
    int[] props = new int[21];
    props[0] = aces;
    props[1] = twos;
    props[2] = threes;
    props[3] = fours;
    props[4] = fives;
    props[5] = sixes;
    props[6] = upperSubtotal;
    props[7] = upperBonus;
    props[8] = upperTotal;
    props[9] = threeKind;
    props[10] = fourKind;
    props[11] = fullHouse;
    props[12] = smallSt;
    props[13] = largeSt;
    props[14] = yahtzee;
    props[15] = chance;
    props[16] = lowerSubtotal;
    props[17] = lowerBonus;
    props[18] = lowerTotal;
    props[19] = turnNumber;
    props[20] = rollNumber;
    return props;
  }

  public Player() {}

  public Player(
      String playerName,
      int aces,
      int twos,
      int threes,
      int fours,
      int fives,
      int sixes,
      int upperSubtotal,
      int upperBonus,
      int upperTotal,
      int threeKind,
      int fourKind,
      int fullHouse,
      int smallSt,
      int largeSt,
      int yahtzee,
      int chance,
      int lowerSubtotal,
      int lowerBonus,
      int lowerTotal,
      int turnNumber,
      int rollNumber,
      int id,
      String timeStored,
      String diceSeq) {
    this.playerName = playerName;
    this.aces = aces;
    this.twos = twos;
    this.threes = threes;
    this.fours = fours;
    this.fives = fives;
    this.sixes = sixes;
    this.upperSubtotal = upperSubtotal;
    this.upperBonus = upperBonus;
    this.upperTotal = upperTotal;
    this.threeKind = threeKind;
    this.fourKind = fourKind;
    this.fullHouse = fullHouse;
    this.smallSt = smallSt;
    this.largeSt = largeSt;
    this.yahtzee = yahtzee;
    this.chance = chance;
    this.lowerSubtotal = lowerSubtotal;
    this.lowerBonus = lowerBonus;
    this.lowerTotal = lowerTotal;
    this.turnNumber = turnNumber;
    this.rollNumber = rollNumber;
    this.id = id;
    this.timeStored = timeStored;
    this.diceSeq = diceSeq;
  }

  public String getPlayerName() {
    return playerName;
  }

  public void setPlayerName(String playerName) {
    this.playerName = playerName;
  }

  public int getAces() {
    return aces;
  }

  public void setAces(int aces) {
    this.aces = aces;
  }

  public int getTwos() {
    return twos;
  }

  public void setTwos(int twos) {
    this.twos = twos;
  }

  public int getThrees() {
    return threes;
  }

  public void setThrees(int threes) {
    this.threes = threes;
  }

  public int getFours() {
    return fours;
  }

  public void setFours(int fours) {
    this.fours = fours;
  }

  public int getFives() {
    return fives;
  }

  public void setFives(int fives) {
    this.fives = fives;
  }

  public int getSixes() {
    return sixes;
  }

  public void setSixes(int sixes) {
    this.sixes = sixes;
  }

  public int getUpperSubtotal() {
    return upperSubtotal;
  }

  public void setUpperSubtotal(int upperSubtotal) {
    this.upperSubtotal = upperSubtotal;
  }

  public int getUpperBonus() {
    return upperBonus;
  }

  public void setUpperBonus(int upperBonus) {
    this.upperBonus = upperBonus;
  }

  public int getUpperTotal() {
    return upperTotal;
  }

  public void setUpperTotal(int upperTotal) {
    this.upperTotal = upperTotal;
  }

  public int getThreeKind() {
    return threeKind;
  }

  public void setThreeKind(int threeKind) {
    this.threeKind = threeKind;
  }

  public int getFourKind() {
    return fourKind;
  }

  public void setFourKind(int fourKind) {
    this.fourKind = fourKind;
  }

  public int getFullHouse() {
    return fullHouse;
  }

  public void setFullHouse(int fullHouse) {
    this.fullHouse = fullHouse;
  }

  public int getSmallSt() {
    return smallSt;
  }

  public void setSmallSt(int smallSt) {
    this.smallSt = smallSt;
  }

  public int getLargeSt() {
    return largeSt;
  }

  public void setLargeSt(int largeSt) {
    this.largeSt = largeSt;
  }

  public int getYahtzee() {
    return yahtzee;
  }

  public void setYahtzee(int yahtzee) {
    this.yahtzee = yahtzee;
  }

  public int getChance() {
    return chance;
  }

  public void setChance(int chance) {
    this.chance = chance;
  }

  public int getLowerSubtotal() {
    return lowerSubtotal;
  }

  public void setLowerSubtotal(int lowerSubtotal) {
    this.lowerSubtotal = lowerSubtotal;
  }

  public int getLowerBonus() {
    return lowerBonus;
  }

  public void setLowerBonus(int lowerBonus) {
    this.lowerBonus = lowerBonus;
  }

  public int getLowerTotal() {
    return lowerTotal;
  }

  public void setLowerTotal(int lowerTotal) {
    this.lowerTotal = lowerTotal;
  }

  public int getTurnNumber() {
    return turnNumber;
  }

  public void setTurnNumber(int turnNumber) {
    this.turnNumber = turnNumber;
  }

  public int getRollNumber() {
    return rollNumber;
  }

  public void setRollNumber(int rollNumber) {
    this.rollNumber = rollNumber;
  }

  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
  }

  public String getTimeStored() {
    return timeStored;
  }

  public void setTimeStored(String timeStored) {
    this.timeStored = timeStored;
  }

  public String getDiceSeq() {
    return diceSeq;
  }

  public void setDiceSeq(String diceSeq) {
    this.diceSeq = diceSeq;
  }
}
