package src;

import java.io.IOException;

public class Demo{

  public static void main (String[] args) throws IOException{
  	
    Modele taquin = new Modele(3,3);
    
    MyFrame frame = new MyFrame(taquin);
    ConsoleView vue = new ConsoleView(taquin);
  }
}
