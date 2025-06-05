from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/google_trends', methods=['POST'])
def google_trends():
    try:
        data = request.get_json()
        keyword = data.get("keyword")

        pytrends = TrendReq(hl='en-ZA', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='ZA')

        interest = pytrends.interest_over_time().reset_index()
        related_data = pytrends.related_queries()
        
        related = related_data.get(keyword, {}).get('top')

        return jsonify({
            "keyword": keyword,
            "trendline": interest.to_dict(orient='records'),
            "related_queries": related.to_dict(orient='records') if related is not None else []
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
