from flask import Flask, render_template, redirect, url_for, flash
import db as dbmod

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-secret"


@app.route('/')
def index():
    # Keep pending and approved as-is
    pending = dbmod.list_topics('pending')
    approved = dbmod.list_topics('approved')

    # Rejected: only pass id + name
    raw_rejected = dbmod.list_topics('rejected')
    rejected = [
        {"topic_id": r.get("topic_id"), "topic_name": r.get("topic_name")}
        for r in raw_rejected
    ]

    # Subscriptions: only user_name + topic_name
    subs = dbmod.list_subscriptions()  # already returns only user_name, topic_name

    return render_template(
        'dashboard.html',
        pending=pending,
        approved=approved,
        rejected=rejected,
        subs=subs
    )


@app.route('/approve/<int:topic_id>', methods=['POST', 'GET'])
def approve(topic_id):
    dbmod.approve_topic(topic_id)
    flash("Topic approved.")
    return redirect(url_for('index'))


@app.route('/reject/<int:topic_id>', methods=['POST', 'GET'])
def reject(topic_id):
    dbmod.reject_topic(topic_id)
    flash("Topic rejected.")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

