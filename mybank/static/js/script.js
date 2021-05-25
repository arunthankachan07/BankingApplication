function populate(object){
  if (object.balance==0){
  let html_data=`<h3>No balance</h3>`

  document.querySelector("#result").innerHTML=html_data;
  }
  else{
  let html_data=`<h3>₹${object.balance}</h3>`

  document.querySelector("#result").innerHTML=html_data;
  }
  }
function getBalance(){
  fetch("http://127.0.0.1:8000/bank/balEnq").
  then(res=>res.json()).
  then(data=>populate(data)).catch(err=>console.log(err));

  }


//function exceptHandle(object){
//  let html_data=`<h3>₹${object.message}</h3>`
//  document.querySelector("#result").innerHTML=html_data;
//  }
//function getErrorMessage(){
//  fetch("http://127.0.0.1:8000/bank/transactionshistory").
//  then(res=>res.json()).
//  then(data=>exceptHandle(data)).catch(err=>console.log(err));
//
//  }


