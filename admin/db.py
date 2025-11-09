import mysql.connector
from config import MYSQL_CONFIG

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

# ============================
#   TOPICS OPERATIONS
# ============================
def list_topics(status=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        if status:
            cur.execute(
                "SELECT topic_id, topic_name, status FROM topics WHERE status=%s ORDER BY topic_id DESC",
                (status,),
            )
        else:
            cur.execute(
                "SELECT topic_id, topic_name, status FROM topics ORDER BY topic_id DESC"
            )
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def get_topic_by_id(topic_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT topic_id, topic_name, status FROM topics WHERE topic_id=%s",
            (topic_id,),
        )
        row = cur.fetchone()
        return row
    finally:
        cur.close()
        conn.close()

def update_topic_status(topic_id, new_status):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE topics SET status=%s WHERE topic_id=%s",
            (new_status, topic_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def approve_topic(topic_id):
    update_topic_status(topic_id, 'approved')

def reject_topic(topic_id):
    update_topic_status(topic_id, 'rejected')

def activate_topic(topic_id):
    update_topic_status(topic_id, 'active')

# ============================
#   SUBSCRIPTIONS
# ============================
def list_subscriptions():
    """
    Return only the subscriber's user_name and the topic_name they've subscribed to,
    as required by the admin dashboard.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT 
                us.user_name,
                t.topic_name
            FROM user_subscriptions AS us
            JOIN topics AS t 
              ON us.topic_name = t.topic_name
            ORDER BY us.id DESC
            """
        )
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

# ============================
#   (No create/insert topic)
# ============================
# Per requirements, topic creation is disabled in the admin app,
# so we remove the insert_topic helper to avoid accidental use.

