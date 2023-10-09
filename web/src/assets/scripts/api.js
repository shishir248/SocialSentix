class API {
  static async getTrending(tops, limit, start, end) {
    const url = 'http://127.0.0.1:8000/api/popular'
    let q = ''
    if (tops) {
      q += `top=${tops}&`
    }
    if (limit) {
      q += `limit=${limit}&`
    }
    if (start) {
      q += `start=${start}&`
    }
    if (end) {
      q += `end=${end}&`
    }

    try{
      const resp = await axios.get(`${url}?${q}`)
      return resp;
    }
    catch(err) {
      return err;
    }
  }

  static async getBard(symbol) {
    const query = `create an article of just 60 words for ${symbol} using source as Nasdaq`;
    const url = 'http://127.0.0.1:8000/bard/getAnswer';
    try{
      const resp = await axios.get(`${url}/${query}`)
      return resp;
    }
    catch(err) {
      return err;
    }
  }

  static async getSymbolInfo(symbol, limit, start, end) {
    const url = 'http://127.0.0.1:8000/api';
    let q = '';
    if (symbol) {
      q += `symbol=${symbol}&`
    }
    if (limit) {
      q += `limit=${limit}&`
    }
    if (start) {
      q += `start=${start}&`
    }
    if (end) {
      q += `end=${end}&`
    }

    try{
      const resp = await axios.get(`${url}?${q}`)
      return resp;
    }
    catch(err) {
      return err;
    }
  }
}

export default API;
