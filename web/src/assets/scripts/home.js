import API from "./api.js";

class HomePage {
  constructor() {
    this.table = document.querySelector('.top-mentions');
    this.item = document.querySelector('.table-row');
    this.about = document.querySelector('.container-left');
  }

  init() {
    const resp = API.getTrending(18);
    resp.then((data)=> {
      this.processTableData(data.data);
    });

    var typewriter = new Typewriter(this.about, {
      loop: false,
      delay: 15,
    });

    typewriter
    .typeString('<h3 >About SentixAI</h3><br><br> SentixAI is a social sentiment analyzer which will tell how social media thinks about a company.<br><br> Social media platforms such as reddit, twitter can influence user behaviour, so it is essential to know whats\' happening.<br><br> Sentix AI provides a score on each symbol representing the sentiment on social media.<br><br><br><br><br><br><br><br> <small>** Disclaimer: We dont encourage or discourage these sentiments. We are promoting the knowledge of what\'s happening. :-) **</small>')
    .pauseFor(300)
    .start();
  }

  processTableData(resp) {
    const { data } = resp;
    Object.keys(data).forEach(symbol => {
      const item = this.item.cloneNode(true);
      const sym = item.querySelector('.row-symbol');
      const mentions = item.querySelector('.row-mentions');
      const posScore = item.querySelector('.row-posscore');
      const compScore = item.querySelector('.row-comscore');


      if (symbol) {
        sym.textContent = symbol;
      }

      if (data[symbol]['comments']) {
        mentions.textContent = data[symbol]['comments'].length;
      }

      if (data[symbol]['total_pos_score']) {
        posScore.textContent = Number(data[symbol]['total_pos_score']).toFixed(3);
      }

      if (data[symbol]['total_pos_score']) {
        compScore.textContent = Number(data[symbol]['total_compound_score']).toFixed(3);
      }

      this.item.parentElement.appendChild(item);

      item.addEventListener('click', ()=> {
        window.open(`/${symbol}`, "_blank")
      })

    });
    this.item.parentElement.removeChild(this.item);
  }
}

export default HomePage;
