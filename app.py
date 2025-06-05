from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/google_trends', methods=['POST'])
def google_trends():
    data = request.get_json()
    keyword = data.get("keyword")

    pytrends = TrendReq(hl='en-ZA', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='ZA', gprop='')

    interest = pytrends.interest_over_time().reset_index()
    related = pytrends.related_queries()[keyword]['top'].to_dict(orient='records')

    return jsonify({
        "keyword": keyword,
        "trendline": interest.to_dict(orient='records'),
        "related_queries": related
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
