const express = require("express");
const cors = require('cors')
const app = express();
const port = 8000;
app.use(express.json());

var mysql = require('mysql');

app.use(cors())
var con = mysql.createConnection({
        host:'xxx.xx.xx.x',
        user:'xxxxxxxxx', 
        password: "xxxxxxxx",
        database:'xxxxxxxxxx',
});

con.connect(function(err) {
    if (err) throw err;
    console.log("Connected!");
    //console.log(con)
});


app.get("/", (req, res) => {
    res.json({ message: "ok" });
  });

//Server-Funktionen für die Parameter
app.get('/getParamData', async(req, res) => {
    

    con.query("SELECT * FROM Paramter_Tabelle", function (err, result, fields) {
      if (err) throw err;
      console.log(result);
      res.send(result);
    });

})

app.put('/sendParamData', async(req, res) => {
    
  console.log("send param")
  console.log(req.body.params)
  var Parameter = req.body.params
  for(let param in Parameter){
    console.log(Parameter[param])
    var sql = `UPDATE Paramter_Tabelle SET Value = ${Parameter[param].Value} WHERE Indizes = ${Parameter[param].Indizes}`;
    con.query(sql, function (err, result) {
      if (err) throw err;
      console.log(result.affectedRows + " record(s) updated");
    });
  }
  return res.json({status: 'inserted'})

});

//Server-Funktionen für das Dashboard
app.get('/getProduktionData', async(req, res) => {
    
  console.log("gimmi param")
  const date = new Date()
  var sql = "SELECT * FROM " + "peter_wafer_colorcheck_" + ('0' + date.getDate()).slice(-2) + ('0' + (date.getMonth()+1)).slice(-2) + date.getFullYear()
  con.query(sql, function (err, result) {
    if (err) throw err;
    console.log(result)
    res.send(result)
  });
  
  

  

})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});

