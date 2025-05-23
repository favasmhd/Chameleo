from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chameleo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({'message': 'User already exists', 'exists': True})
    
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User registered successfully', 'exists': False})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({'message': 'Login successful', 'username': username})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/recommendations/<username>', methods=['GET'])
def get_recommendations(username):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.video_id, v.title, v.file_path, v.tags, r.rsef_score
        FROM Recommendations r
        JOIN Videos v ON r.video_id = v.video_id
        WHERE r.username = ?
        ORDER BY r.rsef_score DESC
        LIMIT 10
    """, (username,))
    
    recommendations = [
        {
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'],
            'tags': row['tags'].split(',') if row['tags'] else [],
            'rsef_score': row['rsef_score']
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()

    return jsonify({'recommendations': recommendations})

@app.route('/popular', methods=['GET'])
def get_popular_videos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.video_id, v.title, v.file_path, v.tags, 
               COUNT(uv.video_id) as watch_count
        FROM videos v
        JOIN UserVideoInteraction uv ON v.video_id = uv.video_id
        GROUP BY v.video_id
        ORDER BY watch_count DESC
        LIMIT 10
    """)
    
    videos = []
    for row in cursor.fetchall():
        videos.append({
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'],
            'tags': row['tags'].split(',') if row['tags'] else [],
            'watch_count': row['watch_count']
        })
    
    conn.close()
    return jsonify({'popular_videos': videos})

@app.route('/search/suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('q', '')

    if not query or len(query) < 2:
        return jsonify({'error': 'Search query too short'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title
        FROM videos
        WHERE title LIKE ?
        LIMIT 10
    """, (f'%{query}%',))

    titles = [row['title'] for row in cursor.fetchall()]

    conn.close()
    return jsonify({'suggestions': titles})

@app.route('/clusters', methods=['GET'])
def get_clusters():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT cluster_id FROM Clusters ORDER BY cluster_id")
    cluster_ids = [row['cluster_id'] for row in cursor.fetchall()]
    
    clusters = []
    for cluster_id in cluster_ids:
        cursor.execute("""
            SELECT v.video_id, v.title, v.file_path, v.tags
            FROM videos v
            JOIN Clusters c ON v.video_id = c.video_id
            WHERE c.cluster_id = ?
            LIMIT 15
        """, (cluster_id,))
        
        videos = []
        for row in cursor.fetchall():
            videos.append({
                'video_id': row['video_id'],
                'title': row['title'],
                'file_path': row['file_path'],
                'tags': row['tags'].split(',') if row['tags'] else []
            })
        
        # Get most common tags in cluster to determine theme
        all_tags = []
        for video in videos:
            all_tags.extend(video['tags'])
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Get top 3 tags
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        theme = ", ".join([tag for tag, _ in top_tags]) if top_tags else f"Cluster {cluster_id}"
        
        clusters.append({
            'cluster_id': cluster_id,
            'theme': theme,
            'videos': videos
        })
    
    conn.close()
    return jsonify({'clusters': clusters})

@app.route('/video/<video_id>', methods=['GET'])
def get_video(video_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM videos WHERE video_id = ?", (video_id,))
    video = cursor.fetchone()
    
    if not video:
        conn.close()
        return jsonify({'error': 'Video not found'}), 404
    
    # Get similar videos
    cursor.execute("""
        SELECT v.video_id, v.title, v.file_path, v.tags, vs.similarity
        FROM VideoSimilarity vs
        JOIN videos v ON vs.video2_id = v.video_id
        WHERE vs.video1_id = ?
        ORDER BY vs.similarity DESC
        LIMIT 5
    """, (video_id,))
    
    similar_videos = []
    for row in cursor.fetchall():
        similar_videos.append({
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'],
            'tags': row['tags'].split(',') if row['tags'] else [],
            'similarity': row['similarity']
        })
    
    result = {
        'video_id': video['video_id'],
        'title': video['title'],
        'file_path': video['file_path'],
        'tags': video['tags'].split(',') if video['tags'] else [],
        'similar_videos': similar_videos
    }
    
    conn.close()
    return jsonify(result)

@app.route('/watch', methods=['POST'])
def record_watch():
    data = request.json
    username = data.get('username')
    video_id = data.get('video_id')
    watch_percentage = data.get('watch_percentage', 100)
    
    if not username or not video_id:
        return jsonify({'error': 'Username and video_id are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if interaction already exists
    cursor.execute("""
        SELECT * FROM UserVideoInteraction 
        WHERE username = ? AND video_id = ?
    """, (username, video_id))
    
    if cursor.fetchone():
        # Update existing interaction
        cursor.execute("""
            UPDATE UserVideoInteraction 
            SET watch_percentage = ?, timestamp = CURRENT_TIMESTAMP
            WHERE username = ? AND video_id = ?
        """, (watch_percentage, username, video_id))
    else:
        # Create new interaction
        cursor.execute("""
            INSERT INTO UserVideoInteraction (username, video_id, watch_percentage)
            VALUES (?, ?, ?)
        """, (username, video_id, watch_percentage))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Watch data recorded successfully'})

@app.route('/history/<username>', methods=['GET'])
def get_watch_history(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.video_id, v.title, v.file_path, v.tags, 
               uv.watch_percentage, uv.timestamp
        FROM UserVideoInteraction uv
        JOIN videos v ON uv.video_id = v.video_id
        WHERE uv.username = ?
        ORDER BY uv.timestamp DESC
    """, (username,))
    
    history = []
    for row in cursor.fetchall():
        history.append({
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'],
            'tags': row['tags'].split(',') if row['tags'] else [],
            'watch_percentage': row['watch_percentage'],
            'timestamp': row['timestamp']
        })
    
    conn.close()
    return jsonify({'history': history})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'Search query is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id, title, file_path, tags
        FROM videos
        WHERE title LIKE ? OR tags LIKE ?
    """, (f'%{query}%', f'%{query}%'))

    results = []
    for row in cursor.fetchall():
        results.append({
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'], # correct key for flutter.
            'tags': row['tags'].split(',') if row['tags'] else []
        })

    conn.close()
    return jsonify({'results': results})

@app.route('/related_videos', methods=['POST'])
def related_videos():
    data = request.get_json()
    tags = data.get('tags', [])

    if not tags:
        return jsonify({'error': 'Tags are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    placeholders = ','.join(['?'] * len(tags))
    query = f"""
        SELECT video_id, title, file_path, tags
        FROM videos
        WHERE tags LIKE '%' || ? || '%'
    """
    for i in range(1, len(tags)):
        query = query + f" OR tags LIKE '%' || ? || '%'"

    cursor.execute(query, tags)

    results = []
    for row in cursor.fetchall():
        results.append({
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'],
            'tags': row['tags'].split(',') if row['tags'] else []
        })

    conn.close()
    return jsonify({'results': results})

@app.route('/videos', methods=['GET'])
def get_videos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id, title, file_path, tags
        FROM videos
    """)

    videos = []
    for row in cursor.fetchall():
        videos.append({
            'video_id': row['video_id'],
            'title': row['title'],
            'file_path': row['file_path'],
            'tags': row['tags']
        })

    conn.close()
    return jsonify(videos)
    
@app.route('/user_clusters/<username>', methods=['GET'])
def get_user_clusters(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch distinct clusters based on videos the user has watched
    cursor.execute("""
        SELECT DISTINCT c.cluster_id
        FROM Clusters c
        JOIN UserVideoInteraction uv ON c.video_id = uv.video_id
        WHERE uv.username = ?
    """, (username,))
    
    clusters = [str(row['cluster_id']) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({'clusters': clusters})

@app.route('/cluster_videos/<int:cluster_id>', methods=['GET'])
def get_videos_by_cluster(cluster_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all videos belonging to the given cluster
    cursor.execute("""
        SELECT v.video_id, v.title, v.file_path, v.tags 
        FROM Videos v
        JOIN Clusters c ON v.video_id = c.video_id
        WHERE c.cluster_id = ?
    """, (cluster_id,))

    videos = [dict(row) for row in cursor.fetchall()]

    conn.close()
    
    return jsonify({"videos": videos})
    
@app.route('/opt_out', methods=['POST'])
def opt_out():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging

        username = data.get('username')
        cluster_id = data.get('cluster_id')

        if not username or not cluster_id:
            return jsonify({"error": "Missing username or cluster_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if cluster_id exists
        cursor.execute("SELECT COUNT(*) FROM Clusters WHERE cluster_id = ?", (cluster_id,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Cluster ID not found"}), 400

        # Delete watched videos from the opted-out cluster
        cursor.execute("""
            DELETE FROM UserVideoInteraction
            WHERE username = ? 
            AND video_id IN (
                SELECT video_id FROM Clusters WHERE cluster_id = ?
            )
        """, (username, cluster_id))

        conn.commit()
        conn.close()

        return jsonify({"message": "Opt-out successful. Rows removed."}), 200

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500



@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
