from flask import Flask, jsonify, request, render_template
from analytics import log_interaction, get_analytics_counts
from recommendation import recommend

app = Flask(__name__)


@app.route('/log', methods=['POST'])
def log():
    data = request.get_json(force=True)
    log_interaction(data['user_id'], data['interaction'], data['outcome'])
    return jsonify({'status': 'ok'})


@app.route('/recommend/<user_id>')
def recommend_route(user_id):
    recs = recommend(user_id)
    return jsonify({'recommendations': recs})


@app.route('/analytics-data')
def analytics_data():
    data = get_analytics_counts()
    return jsonify({'labels': list(data.keys()), 'values': list(data.values())})


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
