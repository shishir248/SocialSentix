import API from "./api.js";


class Symbol {
  constructor(el) {
    this.el = el;
    this.symbol = this.el.dataset.symbol;
    this.uniqueThread = new Set();
  }

  init() {
    API.getSymbolInfo(this.symbol, 45).then((resp) => {
      this.processSymbolInfo(resp.data.data[this.symbol]);
      this.limitWords();
    }).catch((err)=> {
      console.error(err);
      return err;
    })

    API.getBard(this.symbol).then((resp) => {
      this.processBard(resp.data);
    }).catch(err=> {
      console.error(err);
      return err;
    })
  }

  limitWords() {
    const threadBody = document.querySelectorAll('.thread-body');
    const maxLimit = 140;
    threadBody.forEach((body)=> {
      if (body.textContent.length > maxLimit) {
        body.textContent = body.textContent.substring(0, maxLimit) + '...';
        const readMore = document.createElement('span');
        readMore.classList.add('thread-readmore');
        readMore.textContent = 'Read More';
        body.parentElement.appendChild(readMore);
      }
    })
  }

  processBard(data) {
    const bardSection = document.querySelector('.bottom-sec');
    bardSection.textContent = data;
  }

  processSymbolInfo(data) {
    const meter = document.querySelector('.result__chart__layer_one.filling');
    const meter2 = document.querySelector('.result__chart__layer_two.filling');
    const positive = Math.ceil(data.total_pos_score * 100);
    const cmpound = Math.ceil(data.total_compound_score * 100);

    if(positive < cmpound) {
      meter.style.zIndex = '316';
    }

    const meterValue = document.querySelectorAll('.card--result__chart__laylay li span');
    meterValue[0].textContent = Math.ceil(data.total_pos_score * 100);
    meterValue[1].textContent = Math.ceil(data.total_compound_score * 100);
    meter.classList.add(`filling${Math.ceil(data.total_pos_score * 100)}`)
    meter2.classList.add(`filling${Math.ceil(data.total_compound_score * 100)}`)

    this.addThreads(data.comments);
  }

  generateUniqueRandomNumber(limit) {
    const randomNum = Math.floor(Math.random() * limit);
    if (this.uniqueThread.has(randomNum)) {
      this.generateUniqueRandomNumber(limit);
    }
    return randomNum;
  }

  sanitizeCommentUrl(url) {
    if(url.indexOf('www.reddit.com') == -1) {
      url = 'https://www.reddit.com/' + url;
    }
    return url;
  }

  addThreads(comments) {
    this.threadWrapper = this.el.querySelector('.thread-wrapper');
    if (comments.length > 15) {
      for (let i = 0; i < 15; i++) {
        const threadWrapper = this.threadWrapper.cloneNode(true);
        const anchor = threadWrapper.querySelector('a');
        const randomNum = this.generateUniqueRandomNumber(comments.length);
        const comment =  comments[randomNum].body;
        anchor.href = this.sanitizeCommentUrl(comments[randomNum].url);
        const threadBody = threadWrapper.querySelector('.thread-body');
        threadBody.textContent = comment;
        this.threadWrapper.parentElement.appendChild(threadWrapper);
      }
    }
    else {
      comments.forEach(comment=> {
        const threadWrapper = this.threadWrapper.cloneNode(true);
        const anchor = threadWrapper.querySelector('a');
        anchor.href = this.sanitizeCommentUrl(comment);
        const threadBody = threadWrapper.querySelector('.thread-body');
        threadBody.textContent = comment.body;
        this.threadWrapper.parentElement.appendChild(threadWrapper);
      });
    }
    this.threadWrapper.parentElement.removeChild(this.threadWrapper);
  }
}

export default Symbol;

const symbolLayout = document.querySelector('.layout-main');
const symbol = new Symbol(symbolLayout);
symbol.init();
