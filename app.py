
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load model
model = joblib.load("model.pkl")

class House(BaseModel):
    area: float


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>House Price Prediction</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Segoe UI',sans-serif;
}

body{
    background:linear-gradient(135deg,#edf2ff,#dbeafe);
    color:#1f2937;
}

nav{
    width:100%;
    height:75px;
    background:white;
    display:flex;
    justify-content:center;
    align-items:center;
    box-shadow:0 2px 15px rgba(0,0,0,.08);
    position:fixed;
    top:0;
    left:0;
    z-index:1000;
}

nav h2{
    color:#2563eb;
    font-size:30px;
    font-weight:700;
}

.hero{
    min-height:100vh;
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:120px 100px 60px;
}

.left{
    width:50%;
}

.left h1{
    font-size:55px;
    line-height:70px;
    margin-bottom:25px;
}

.left p{
    font-size:18px;
    color:#6b7280;
    line-height:32px;
}

.right{
    width:430px;
}

.card{
    background:white;
    padding:40px;
    border-radius:20px;
    box-shadow:0 20px 50px rgba(0,0,0,.12);
}

.card h2{
    text-align:center;
    color:#2563eb;
    margin-bottom:30px;
}

input{
    width:100%;
    padding:15px;
    font-size:16px;
    border:2px solid #d1d5db;
    border-radius:10px;
    margin-bottom:20px;
}

input:focus{
    outline:none;
    border-color:#2563eb;
}

button{
    width:100%;
    padding:15px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    font-size:17px;
    cursor:pointer;
    transition:.3s;
}

button:hover{
    background:#1d4ed8;
}

#result{
    margin-top:20px;
    padding:18px;
    background:#eff6ff;
    border-radius:10px;
    text-align:center;
    color:#2563eb;
    font-size:20px;
    font-weight:600;
}

.features{
    display:flex;
    justify-content:center;
    gap:30px;
    padding:20px 80px 80px;
}

.box{
    background:white;
    width:300px;
    padding:30px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    transition:.3s;
}

.box:hover{
    transform:translateY(-8px);
}

.box h3{
    color:#2563eb;
    margin-bottom:15px;
}

.box p{
    color:#6b7280;
    line-height:26px;
}

footer{
    background:#111827;
    color:white;
    text-align:center;
    padding:20px;
}

@media(max-width:900px){

.hero{
    flex-direction:column;
    text-align:center;
    padding:120px 30px 50px;
}

.left,.right{
    width:100%;
}

.left h1{
    font-size:38px;
    line-height:50px;
}

.features{
    flex-direction:column;
    align-items:center;
    padding:40px 20px;
}

.box{
    width:100%;
}

}

</style>

</head>

<body>

<nav>

<h2>House Price Prediction</h2>

</nav>

<section class="hero">

<div class="left">

<h1>
Predict House Prices Using Machine Learning
</h1>

<p>

This web application uses a Linear Regression Machine Learning model
to estimate house prices based on the area entered by the user.
Simply enter the house area and receive an instant prediction.

</p>

</div>

<div class="right">

<div class="card">

<h2>Price Prediction</h2>

<input
type="number"
id="area"
placeholder="Enter House Area (Square Feet)">

<button onclick="predictPrice()">
Predict Price
</button>

<div id="result">

Prediction will appear here

</div>

</div>

</div>

</section>

<section class="features">

<div class="box">

<h3>Machine Learning</h3>

<p>

Uses Linear Regression trained on house price data for accurate predictions.

</p>

</div>

<div class="box">

<h3>FastAPI</h3>

<p>

Fast and lightweight backend API that processes prediction requests instantly.

</p>

</div>

<div class="box">

<h3>Real-Time Results</h3>

<p>

Enter the area and instantly receive the estimated house price.

</p>

</div>

</section>

<footer>

House Price Prediction API | Developed using Python, Scikit-learn & FastAPI

</footer>

<script>

async function predictPrice(){

let area=document.getElementById("area").value;

if(area==""){

alert("Please enter house area.");

return;

}

let response=await fetch("/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
area:Number(area)
})

});

let data=await response.json();

document.getElementById("result").innerHTML=
"Predicted Price: Rs. " +
Number(data.predicted_price).toLocaleString();

}

</script>

</body>

</html>
"""


# Prediction API
@app.post("/predict")
def predict(house: House):

    prediction=model.predict([[house.area]])

    return {
        "predicted_price": round(prediction[0],2)
    }
