package src;

public class ConsoleView implements ListenerModel{

  Modele model;

  public ConsoleView(Modele taquin){
    this.model = taquin;
    this.model.addListener(this);
  }

  public void modelUpdate(Object source){
    System.out.println("" + model.toStringGrille());
  }
}
