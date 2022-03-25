package src;

public class Modele extends AbstractModelListener{
  protected int n;
  protected int m;
  protected Tuile [][] grille;

  public Modele(int n, int m){
    this.n = n;
    this.m = m;
    this.grille = new Tuile[this.n][this.m];
    // Grille
    int compteur = 1;
    for(int i = 0; i < this.n; i++){
      for(int j = 0; j < this.m; j++){
        Tuile actual = new Tuile(compteur);
        if(compteur < this.n*this.m){
          grille[i][j] = actual;
        }else{
          grille[i][j] = new Tuile(0);
        }
        compteur++;
      }
    }
  }
  public int getM(){
    return this.m;
  }
  public int getN(){
    return this.n;
  }
  public Tuile[][] getGrille(){
    return this.grille;
  }

  public String toStringGrille(){
    String res = "";
    for(int i = 0; i < this.n; i++){
      for(int j = 0; j < this.m; j++){
        res = res + (" | " + this.grille[i][j].getId());
      }
      res = res + (" | ");
      res = res + ("\n");
      res = res + ("\n");
    }
    res = res + ("--------------\n");
    return res;
  }

  public boolean mouvement(String move){
    Tuile actual = null;
    int x = 0;
    int y = 0;

    for(int i = 0; i < this.n; i++){
      for(int j = 0; j < this.m; j++){
        if(this.grille[i][j].getId() == 0){
          actual = this.grille[i][j];
          x = i;
          y = j;
        }
      }
    }

    Tuile tmp;

    if(move == "haut" && x+1 < m){
      tmp = this.grille[x+1][y];
      this.grille[x+1][y] = actual;
      this.grille[x][y] = tmp;
      fireChangement();
      return true;
    }
    else if(move == "droite" && y-1 >= 0){
      tmp = this.grille[x][y-1];
      this.grille[x][y-1] = actual;
      this.grille[x][y] = tmp;
      fireChangement();
      return true;
    }
    else if(move == "bas" && x-1 >= 0){
      tmp = this.grille[x-1][y];
      this.grille[x-1][y] = actual;
      this.grille[x][y] = tmp;
      fireChangement();
      return true;
    }
    else if(move == "gauche" && y+1 < n){
      tmp = this.grille[x][y+1];
      this.grille[x][y+1] = actual;
      this.grille[x][y] = tmp;
      this.fireChangement();
      return true;
    }
    else{
      return false;
    }
  }

  public void deranger(int chaos){
    String [] tab = {"bas","droite","haut","gauche"};
    int x;

    for(int i = 0; i < chaos; i++){
      x = (int)Math.round(Math.random()*3);

      while(mouvement(tab[x]) != true){
        x = (int)Math.round(Math.random()*3);
      }
    }
  }

  public boolean estrange(){
    Tuile [][] test;
    test = new Tuile[this.n][this.m];
    int compteur = 1;

    // Construction grille de comparaison
    for(int i = 0; i < this.n; i++){
      for(int j = 0; j < this.m; j++){
        Tuile actual = new Tuile(compteur);
        if(compteur < this.n*this.m){
          test[i][j] = actual;
          // Test valeurs egales
          if(test[i][j].getId() != this.grille[i][j].getId()){
            return false;
          }
        }else{
          test[i][j] = new Tuile(0);
          // Test valeurs egales
          if(test[i][j].getId() != this.grille[i][j].getId()){
            return false;
          }
        }
        compteur++;
      }
    }
    return true;
  }
}
