cross123=document.getElementById("cross121");
popup=document.getElementById("pooopup");

main=document.getElementById("main2")

main.style.opacity=0.04;
// main.style.display='none';

cross123.addEventListener("click",function(){
    console.log('i am in class');
    
    main.style.opacity=100;
    popup.style.display='none';


});

