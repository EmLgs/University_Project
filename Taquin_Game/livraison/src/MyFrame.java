package src;

import javax.swing.*;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.*;

public class MyFrame extends JFrame implements ListenerModel{

    Modele modele;
    MyPanel panel;

    public MyFrame(Modele modele){
        super();
        this.modele = modele;
        modele.addListener(this);
        this.panel = new MyPanel(modele);
        
        // Paramètres de la frame
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(panel.getSize().width,panel.getSize().height);
        this.setVisible(true);
        this.setTitle("Taquin");
        
        // Ajout des commandes avec les fleches du clavier
        this.addKeyListener(new KeyListener() {

			@Override
			public void keyTyped(KeyEvent e) {
				// TODO Auto-generated method stub
			}

			@Override
			public void keyPressed(KeyEvent e) {
				int keyCode = e.getKeyCode();
				switch(keyCode) {
					case KeyEvent.VK_UP:
						modele.mouvement("bas");
						break;
					case KeyEvent.VK_DOWN:
						modele.mouvement("haut");
						break;
					case KeyEvent.VK_LEFT:
						modele.mouvement("droite");		
						break;
					case KeyEvent.VK_RIGHT:
						modele.mouvement("gauche");			
						break;
				}		
			}

			@Override
			public void keyReleased(KeyEvent e) {
				// TODO Auto-generated method stub
				
			}
        	
        });
        this.getContentPane().add(panel);
    }
    
    public void modelUpdate(Object source){
    	panel.frameUpdate();
    	panel.updateUI();
  }
}
