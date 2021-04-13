var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     console.log(this.responseText)
    }
  };
xhttp.open("GET", "https://us-lti.bbcollab.com/collab/api/csa/recordings?startTime=2020-08-20T00%3A00%3A00-0500&endTime=2020-11-27T23%3A59%3A59-0500&sort=endTime&order=desc&limit=100&offset=0", true);
xhttp.setRequestHeader("Authorization", "Bearer eyJhbGciOiJIUzI1NiJ9....");
xhttp.send();




//no olvidar habilitar popups en chrome
let urls = []
let id
let token = "eyJhbGciOiJIUzI1NiJ9...."
function openLink(urls, index){
    console.log(index)
    if(index < urls.length){
        id = urls[index].id
        fetch("https://us-lti.bbcollab.com/collab/api/csa/recordings/" + id + "/url?validHours=0&validMinutes=5", {
          "headers": {
            "authorization": "Bearer " + token
          },
          "method": "GET",
          "mode": "cors"
        }).then(response => response.json())
        .then(data => {
            let url = data.url
            window.open(url, "_blank", "", false)
            setTimeout( ()=> {
                openLink(urls, index + 1)
            }, 1000)
        });
    }
}
openLink(urls, 0)
