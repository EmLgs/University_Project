import random

class Grille:

    def __init__(self, lignes = 8, colonnes = 8):
        self.lignes = lignes
        self.colonnes = colonnes
        self.grille = []
        self.coord = []
        self.arrangements = False
        self.creation_grille()

    def creation_grille(self):
        self.grille = []
        for i in range(self.lignes):
            ligne = []
            for j in range(self.colonnes):
                alea = random.randint(1,4)
                ligne.append(alea)
            self.grille.append(ligne)

    # Afficher proprement la grille
    def affichage(self):
        print("-------------------------------------------------------")
        for ligne in self.grille:
            print('|\t', '\t'.join([str(val) for val in ligne]), '\t|')
        print("-------------------------------------------------------")

    # Convertir coordonnées en numéro
    def coor_to_num(self, pos1, pos2):
        num = ((pos1 * self.lignes) + pos2)
        return(num)

    # Convertir numéro en coordonnées
    def num_to_coor(self, num):
        pos1 = num // self.lignes
        pos2 = num % self.lignes
        return pos1,pos2

    # Vérifier si numéros sont à cotés
    def adjacent(self, x, x2):
        if x+1 == x2:
            return True
        elif x-1 == x2:
            return True
        elif x+self.lignes == x2:
            return True
        elif x-self.lignes == x2:
            return True
        return False

    # Echanger les deux numéros
    def echange(self, x, x2):
        # Vérifier si cases adjacentes
        if(self.adjacent(x,x2)):
            a,b = self.num_to_coor(x)
            a2,b2 = self.num_to_coor(x2)
            # Echanger les cases
            self.grille[a][b],self.grille[a2][b2] = self.grille[a2][b2],self.grille[a][b]
            # Si cela ne créer pas de combinaisons
            if not self.combinaisons():
                print("Echange impossible")
                # Remettre les cases à leurs places
                self.grille[a][b],self.grille[a2][b2] = self.grille[a2][b2],self.grille[a][b]
        # Si les cases ne sont pas adjacentes
        else:
            print("Echange impossible")

    # Vérifier si des combinaisons existent
    def combinaisons(self):
        self.coord = []
        # Vérifier les lignes
        for i in range(self.lignes):
            streak = 1
            for j in range(1,self.colonnes):
                if self.grille[i][j] == self.grille[i][j-1]:
                    streak += 1
                else:
                    streak = 1

                # Si ligne
                if streak == 3:
                    self.coord.append((i,j-2))
                    self.coord.append((i,j-1))
                    self.coord.append((i,j))

                elif streak > 3:
                    self.coord.append((i,j))

        # Vérifier les colonnes
        for j in range(self.colonnes):
            streak = 1
            for i in range(1,self.lignes):
                if self.grille[i][j] == self.grille[i-1][j]:
                    streak += 1
                else:
                    streak = 1

                # Si colonne
                if streak == 3:
                    self.coord.append((i-2,j))
                    self.coord.append((i-1,j))
                    self.coord.append((i,j))

                elif streak > 3:
                    self.coord.append((i,j))

        return(self.coord)


class Level(Grille):

    def __init__(self):
        Grille.__init__(self)

    # Remplacer les cases alignés par des croix (X)
    def destruction(self):
        for a in range(len(self.coord)):
            alea = random.randint(1,4)
            i = self.coord[a][0]
            j = self.coord[a][1]
            self.grille[i][j] = "X"

    # Supprimer les cases alignés, faire tomber celles du dessus et ajouter des nouvelles
    def gravite(self):
        for i in range(self.lignes):
            for j in range(self.colonnes):
                if self.grille[i][j] == "X":
                    # Si c'est la première ligne seulement remplacer par un chiffre aléatoire
                    if i == 0:
                        self.grille[i][j] = random.randint(1,4)
                    # Si ce sont toutes les autres lignes système de descente
                    if i > 0:
                        k = i
                        while k != 0:
                            self.grille[k][j] = self.grille[k-1][j]
                            k -= 1
                        self.grille[0][j] = random.randint(1,4)
                        
    # Avoir une grille sans combinaisons
    def grille_de_debut(self):
        for i in range(5):
            self.combinaisons()
            if self.coord != []:
                for a in range(len(self.coord)):
                    alea = random.randint(1,4)
                    i = self.coord[a][0]
                    j = self.coord[a][1]
                    self.grille[i][j] = alea
            self.coord = []
