function populate(object){
  let html_data=`<h3>₹${object.balance}</h3>`
  document.querySelector("#result").innerHTML=html_data;
  }
function getBalance(){
  fetch("http://127.0.0.1:8000/bank/balEnq").
  then(res=>res.json()).
  then(data=>populate(data)).catch(err=>console.log(err));

  }
