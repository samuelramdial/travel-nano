"use strict";
const url = "https://v6.exchangerate-api.com/v6/45d38949eb39005b6b5c0c15/latest/USD"
let countries = [];
const dropList = Array.from(document.querySelectorAll(".drop-list select"));
const submitBtn = document.querySelector('button[type=submit]');
const exchange = document.querySelector('i');
window.addEventListener('DOMContentLoaded', fetchCountries);

async function fetchCountries()
{
    try{
        const response = await fetch(url)
        if (!response.ok)
            throw Error(`Error ${response.url} ${response.statusText}`);
        countries = await response.json();
        loadCountries(countries['conversion_rates']);
    } catch(error) {
        console.log(error.message);
    }
}

function loadCountries(countries)
{
    let places = Object.keys(countries);
    for (let i = 0; i < dropList.length; i++)
    {
        for (let j = 0; j < places.length; j++)
        {
            let holder;
            if (i == 0){
                holder = places[j] === 'USD' ? "selected" : "";
            }else {
                holder = places[j] === 'CAD' ? "selected" : "";
            }
            let option = `<option value = "${places[j]}" ${holder}>${places[j]}</option>`;
            dropList[i].insertAdjacentHTML("beforeend", option);
        }
    dropList[i].addEventListener('change', e => {loadFlag(e.target)});
    }
}

function loadFlag(e)
{
    let places = Object.keys(countries['conversion_rates']);
    for (let i = 0; i < places.length; i++)
    {
        if (places[i] == e.value)
        {
            let img = e.parentElement.querySelector('img');
            img.src = `https://flagsapi.com/${places[i].substring(0,2)}/flat/64.png`;
        }
    }
}

exchange.addEventListener('click', () => {
    let holder = fromCurrency.value; 
    fromCurrency.value = toCurrency.value; 
    toCurrency.value = holder;
    loadFlag(fromCurrency);
    loadFlag(toCurrency);
})