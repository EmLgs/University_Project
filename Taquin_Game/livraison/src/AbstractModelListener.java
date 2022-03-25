package src;

import java.util.ArrayList;

public abstract class AbstractModelListener{

  protected ArrayList<ListenerModel> listeners;

  public AbstractModelListener(){
    this.listeners = new ArrayList<ListenerModel>();
  }

  public void addListener(ListenerModel e){
    this.listeners.add(e);
  }

  public void removeListener(ListenerModel e){
    this.listeners.remove(e);
  }

  protected void fireChangement(){
    for(ListenerModel listeners: this.listeners){
      listeners.modelUpdate(this);
    }
  }
}
