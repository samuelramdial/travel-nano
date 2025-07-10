// news fetch using news api 

const newsType = document.getElementById("newsType");
const newsdetails = document.getElementById("newsdetails");
var newsDataArr = [];
window.onload = function () {
    fetchHeadlines();
};

const NEWS_API_KEY = '42e02251ecc24a6db0a6e5b69f427da0';


const fetchHeadlines = async () => {
    const response = await fetch(`https://newsapi.org/v2/top-headlines?country=us&apiKey=${NEWS_API_KEY}`);
    newsDataArr = [];
    if (response.status >= 200 && response.status < 300) {
        const myJson = await response.json();
        newsDataArr = myJson.articles;
    } else {
        // handle errors
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }
    display();
}


function display() {
    let sz = newsDataArr.length;
    let index = 0;
    console.log(typeof sz)
    newsdetails.innerHTML = "";
    var col = document.createElement('div');
    col.className = "card";
    // col.style.witdh = 200+'px'

    var card = document.createElement('div');
    card.className = "p-2 item-box";

    var image = document.createElement('img');
    image.setAttribute("height", "matchparent");
    image.setAttribute("width", "100%");
    var cardBody = document.createElement('div');

    var newsHeading = document.createElement('h5');
    newsHeading.className = "card-title";
    var dateHeading = document.createElement('h6');
    dateHeading.className = "text-info";
    var discription = document.createElement('p');
    discription.className = "text-muted";
    var link = document.createElement('a');
    link.className = "btn btn-dark";
    link.setAttribute("target", "_blank");
    link.innerHTML = "Read more";

    function displayNews() {

        // newsdetails.innerHTML = "";
        if (newsDataArr.length == 0) {
            newsdetails.innerHTML = "<h5>No data found.</h5>"
            return;
        }

        let news = newsDataArr[index];


        var date = news.publishedAt.split("T");
        image.src = "";
        image.src = news.urlToImage;
        newsHeading.innerHTML = "";
        newsHeading.innerHTML = news.title;
        dateHeading.innerHTML = "";
        dateHeading.innerHTML = date[0];
        // discription.innerHTML = "";
        // discription.innerHTML = news.description;
        link.href = news.url;
        index++;
        if (sz === index) {
            index = 0;
            fetchHeadlines();
        }

    }
    displayNews()

    cardBody.appendChild(newsHeading);
    cardBody.appendChild(dateHeading);
    cardBody.appendChild(discription);
    cardBody.appendChild(link);
    card.appendChild(image);
    card.appendChild(cardBody);
    col.appendChild(card);
    newsdetails.appendChild(col);

    // update after 50 sec
    setInterval(displayNews, 50000)
}

