package src;

import javax.swing.*;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.*;
import java.io.File;
import java.io.IOException;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MyPanel extends JPanel implements ActionListener{

    public BufferedImage image;
    public Modele modele;
    public GridBagConstraints gridImages;
    protected JButton[][] buttonGrid;
    public int elem1X, elem1Y, elem2X, elem2Y;
    public boolean click = false;

    public MyPanel(Modele modele){   	
        super();
        this.modele = modele;

        this.setLayout(new GridBagLayout());
        this.setBackground(Color.white);
        this.gridImages = new GridBagConstraints();
        this.buttonGrid = new JButton[modele.getN()][modele.getN()];
        
        try{
            this.image = ImageIO.read(new File("./livraison/doc/img1.jpg"));
          }catch (IOException e1){
            e1.printStackTrace();
        }
        
        this.setBounds(0,0,this.image.getWidth() + 50,this.image.getHeight() + 50);
        
        // Parcourir la grille pour afficher les images
        for(int i = 0; i < modele.getN(); i++){
          for(int j = 0; j < modele.getM(); j++){
        	  
	    	Tuile[][] grille = modele.getGrille();
	        int x, y;
	        
	        // Tansformer les identifiants en coordonnées pour gridImages
	        if(grille[i][j].getId() == 0) {  
                x = (modele.getM() * modele.getN()-1) % modele.getN();
                y = (modele.getM() * modele.getN()-1) / modele.getN();
            }else{
            	x = (grille[i][j].getId()-1) % modele.getN();
      	        y = (grille[i][j].getId()-1) / modele.getN(); 
            }
	        
	        // Recuperer la largeur et longueur d'un carré
            int w = this.image.getWidth() / modele.getM();
            int h = this.image.getHeight() / modele.getN();
            BufferedImage b = this.image.getSubimage(x * w, y * h, w, h);
     
            // Definir la place dans gridImages
            this.gridImages.gridx = j;
            this.gridImages.gridy = i;
            
            // Verifier si la tuile actuelle est la tuile vide ou non
            // Si oui le bouton ne contiendra pas d'images
            if(grille[i][j].getId() != 0) {
            	JButton button = new JButton(new ImageIcon(b));
                button.setPreferredSize(new Dimension(w, h));
                button.addActionListener(this);
            	this.add(button,this.gridImages);
            	this.buttonGrid[i][j] = button;
            }else {
            	JButton button = new JButton();
            	button.setPreferredSize(new Dimension(w, h));
            	button.addActionListener(this);
            	this.add(button, this.gridImages);
            	this.buttonGrid[i][j] = button;
            }
            
          }
        }
    }
        
    public void frameUpdate(){
    	
    	for(int i = 0; i < modele.getN(); i++){
            for(int j = 0; j < modele.getM(); j++){
            	
              remove(this.buttonGrid[i][j]);
              
              Tuile[][] grille = modele.getGrille();
              int x, y;
              
              int w = this.image.getWidth() / modele.getM();
              int h = this.image.getHeight() / modele.getN();
              
              if(grille[i][j].getId() == 0) {  
                x = (modele.getM() * modele.getN()-1) % modele.getN();
                y = (modele.getM() * modele.getN()-1) / modele.getN();
              }else{
              	x = (grille[i][j].getId()-1) % modele.getN();
        	    y = (grille[i][j].getId()-1) / modele.getN(); 
              }

              BufferedImage b = this.image.getSubimage(x * w, y * h, w, h);

              this.gridImages.gridx = j;
              this.gridImages.gridy = i;
              
              if(grille[i][j].getId() != 0) {
            	  JButton button = new JButton(new ImageIcon(b));
            	  button.setPreferredSize(new Dimension(w, h));
            	  button.addActionListener(this);
            	  this.add(button,this.gridImages);
            	  this.buttonGrid[i][j] = button;
              }else{
            	  JButton button = new JButton();
            	  button.setPreferredSize(new Dimension(w, h));
            	  button.addActionListener(this);
            	  this.add(button,this.gridImages);
            	  this.buttonGrid[i][j] = button;
              }
            }
          }
    }
    
    public void changeClick(int elem1X, int elem1Y, int elem2X, int elem2Y){
           
    }

	@Override
	public void actionPerformed(ActionEvent e) {
		/*
		JButton button = (JButton) e.getSource();
		if(click == false) {
			this.elem1X = button;
		}else{
			this.elem2X = button;
		}
		
		if(click == true) {
			click = false;
		}else {
			click = true;
		}
		*/
	}
}
