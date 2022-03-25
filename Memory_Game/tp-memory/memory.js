function startMemoryGame(){

    // obtenir la largeur et la hauteur de la zone disponible

    function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
    }


    function Mélange(array){
      let k;
      for(let i=array.length-1; i>0; i--){
          let j=getRandomInt(i);
          k=array[i];
          array[i]=array[j];
          array[j]=k;
        }
        return array;
      }

    function Grid(){
      let N=6;
      let M=4;
      let Tab=[];
      for(let i=0; i<N*M/2; i++){
        let alea= getRandomInt(32)+1;
        Tab.push(alea);
        Tab.push(alea);
      }

      let newTab =Mélange(Tab);
      console.log(newTab);
      Afficher(newTab)
    }

    Grid()

    function Afficher(array){
      let jeu= document.getElementById("jeu");
      let inverse=document.createElement("img");
      inverse.setAttribute("src","images/js-logo.jpg");

      let height=parseInt(window.getComputedStyle(jeu).getPropertyValue("height"))
      let width=parseInt(window.getComputedStyle(jeu).getPropertyValue("width"))
      let width_card=width/6;
      let height_card=height/4;
      let min=Math.min(width_card,height_card);
      jeu.style.gridTemplateColumns= "repeat("+ 6+","+min+"px)";
      jeu.style.gridTemplateRows= "repeat("+ 4+","+min+"px)";


      for(let i=0; i<array.length; i++){
        let div = document.createElement("div");
        div.dataset.numero=array[i];
        div.appendChild(inverse.cloneNode(true));
        div.addEventListener("click",reverse);
        jeu.appendChild(div);

    nb_score=0;
    coups=0;
    nb_paires=0;
    cmp=1;
    tab1=[];
    tab2=[];
    function reverse(event){
      let j=event.currentTarget;
      let img=j.querySelector("img");
      img.setAttribute("src", "images/" + array[i] + ".jpg");
      div.appendChild(img);
      console.log(array[i]);
      let alldiv=document.querySelectorAll("div");

      tab1.push(j.getAttribute("data-numero"))
      tab2.push(j);
      console.log(tab2);
      if(cmp%2==0){
      setTimeout(retourne, 850);
      function retourne(){
        if(tab1[tab1.length-1]==tab1[tab1.length-2]){
          for(let p=0; p<alldiv.length; p++){
            if(alldiv[p].getAttribute("data-numero")==tab1[tab1.length-1]){
              let img1=tab2[tab2.length-1].querySelector("img");
              let img2=tab2[tab2.length-2].querySelector("img");
              img1.style.display="none";
              img2.style.display="none";
            }else if (alldiv[p].getAttribute("data-numero")==tab1[tab1.length-2]) {
              let img1=tab2[tab2.length-2].querySelector("img");
              let img2=tab2[tab2.length-1].querySelector("img");
              img1.style.display="none";
              img2.style.display="none";
            }
        }
        nb_score=nb_score+3;
        p3.innerHTML="Score: "+nb_score;
        coups++;
        p1.innerHTML="Coups: "+coups;
        nb_paires++;
        p2.innerHTML="Paires trouvées: "+nb_paires;
        }else{
          for(let p=0; p<alldiv.length; p++){
            if(alldiv[p].getAttribute("data-numero")==tab1[tab1.length-1]){
              let img1=alldiv[p].querySelector("img");
              img1.setAttribute("src", "images/js-logo.jpg");
            }else if (alldiv[p].getAttribute("data-numero")==tab1[tab1.length-2]) {
              let img1=alldiv[p].querySelector("img");
              img1.setAttribute("src", "images/js-logo.jpg");
            }
            }
            nb_score--;
            p3.innerHTML="Score: "+nb_score;
            coups++;
            p1.innerHTML="Coups: "+coups;
    cmp++;}
  }}else{cmp++;}
  console.log(tab1);

  }
}




//partie 4
let memory=document.querySelector('h2');
let div1=document.createElement("div");
let div2=document.createElement("div");
let div3=document.createElement("div");

div1.appendChild(memory);

let scoreboard=document.querySelector("section");
scoreboard.appendChild(div1)
let p1=document.createElement("p");
let p4=document.createElement("p");
let p5=document.createElement("p");
let p2=document.createElement("p");
let p3=document.createElement("p");
let txt1=document.createElement("input");
txt1.setAttribute("type","text");
txt1.setAttribute("name","lignes");
txt1.setAttribute("value",6);


let txt2=document.createElement("input");
txt2.setAttribute("type","text");
txt2.setAttribute("name","colonnes");
txt2.setAttribute("value",4);

let coupstxt=document.createTextNode('Coups: '+coups);
let paires=document.createTextNode("Paires trouvées: "+nb_paires);
let score=document.createTextNode('Score: '+nb_score);
let lignes=document.createTextNode('Nombre de lignes: ');
let colonnes=document.createTextNode('Nombre de colonnes: ');

p1.appendChild(coupstxt);
p3.appendChild(score);
p2.appendChild(paires);
p4.appendChild(lignes);
p4.appendChild(txt1);
p5.appendChild(colonnes);
p5.appendChild(txt2);
div2.appendChild(p1);
div2.appendChild(p2);
div2.appendChild(p3);

div3.appendChild(p4);
div3.appendChild(p5);

scoreboard.appendChild(div2);
scoreboard.appendChild(div3);

scoreboard.style.display="grid";
scoreboard.style.gridTemplateColumns="auto auto auto";
console.log(scoreboard);
}
}
