function populate(object){
  if (object.balance==0){
  let html_data=`<h3 style="font-family: Arial, Helvetica, sans-serif;">No balance</h3>`

  document.querySelector("#result").innerHTML=html_data;
  }
  else{
  let html_data=`<h3 style="font-family: Arial, Helvetica, sans-serif;">₹ ${object.balance}</h3>`

  document.querySelector("#result").innerHTML=html_data;
  }
  }
function getBalance(){
  fetch("http://127.0.0.1:8000/balEnq").
  then(res=>res.json()).
  then(data=>populate(data)).catch(err=>console.log(err));

  }


//script for debit transaction detail view - modal window
function debitdetail(object){
    console.log(object.date)
 let html_data=`<h3 style="text-align:center;color:red;font-family: Arial, Helvetica, sans-serif;">- ₹${object.amount}.00</h3>
 <h4 style="text-align:center;font-family: Arial, Helvetica, sans-serif;">SBK-OUT/TID/sbk000${object.id}</h4>
  <table class="table">
  <tr><td>Transaction Id</td><td>sbk000${object.id}</td></tr>
  <tr><td>To</td><td>${object.to_accno}</td></tr>
  <tr><td>On</td><td>${object.date}</td></tr>
  <tr><td>Remarks</td><td>${object.remarks}</td></tr>
   <tr><td>Transaction Type</td><td>Debit</td></tr>
  </table>
 `
 document.querySelector("#debit").innerHTML=html_data;
  }
function getDebit(tid){
   let id = tid
  fetch(`http://127.0.0.1:8000/t_debit/${id}`).
  then(res=>res.json()).
  then(data=>debitdetail(data)).catch(err=>console.log(err));

  }



//script for credit transaction detail view - modal window
function creditdetail(object){
    console.log(object.date)
 let html_data=`<h3 style="text-align:center;color:green;font-family: Arial, Helvetica, sans-serif;">+ ₹${object.amount}.00</h3>

 <h4 style="text-align:center;font-family: Arial, Helvetica, sans-serif;">SBK-IN/TID/sbk000${object.id}</h4>
  <table class="table">
  <tr><td>Transaction Id</td><td>sbk000${object.id}</td></tr>
  <tr><td>From</td><td>${object.from_accno}</td></tr>
  <tr><td>On</td><td>${object.date}</td></tr>
  <tr><td>Remarks</td><td>${object.remarks}</td></tr>
   <tr><td>Transaction Type</td><td>Credit</td></tr>

  </table>
 `

document.querySelector("#credit").innerHTML=html_data;


  }
function getCredit(tid){
   let id = tid
  fetch(`http://127.0.0.1:8000/t_credit/${id}`).
  then(res=>res.json()).
  then(data=>creditdetail(data)).catch(err=>console.log(err));

  }





