import sqlite3
import igraph as ig
from collections import defaultdict
import heapq

db_path = "chameleo.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def fetch_video_similarity():
    cursor.execute("SELECT video1_id, video2_id, similarity FROM VideoSimilarity")
    return cursor.fetchall()

def fetch_watch_history():
    cursor.execute("SELECT username, video_id, watch_percentage FROM UserVideoInteraction")
    preferences = defaultdict(lambda: {"preferred": set(), "non_preferred": set()})
    
    for username, video_id, watch_percentage in cursor.fetchall():
        if watch_percentage >= 50:
            preferences[username]["preferred"].add(video_id)
        else:
            preferences[username]["non_preferred"].add(video_id)
    
    return preferences

def fetch_clusters():
    cursor.execute("SELECT cluster_id, video_id FROM Clusters")
    cluster_videos = defaultdict(list)
    for cluster_id, video_id in cursor.fetchall():
        cluster_videos[cluster_id].append(video_id)
    return cluster_videos

def compute_centrality(similarity_data):
    g = ig.Graph()
    video_ids = set(v for pair in similarity_data for v in pair[:2])
    video_to_index = {video_id: i for i, video_id in enumerate(video_ids)}
    
    g.add_vertices(len(video_ids))
    edge_list = [(video_to_index[v1], video_to_index[v2]) for v1, v2, _ in similarity_data]
    weights = [sim for _, _, sim in similarity_data]
    g.add_edges(edge_list)
    g.es['weight'] = weights
    
    degree_centrality = g.degree()
    closeness_centrality = g.closeness(weights=g.es['weight'])
    betweenness_centrality = g.betweenness(weights=g.es['weight'])
    
    aggregate_centrality = {v: (degree_centrality[i] + closeness_centrality[i] + betweenness_centrality[i]) for v, i in video_to_index.items()}
    return aggregate_centrality

import heapq
from collections import defaultdict

def compute_shortest_paths(similarity_lookup, num_videos):
    distances = {v: {} for v in range(num_videos)}

    for start in range(num_videos):
        pq = [(0, start)]  # (distance, node)
        visited = set()

        while pq:
            dist, node = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            distances[start][node] = dist  # Store shortest distance

            for neighbor in similarity_lookup[node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (dist + 1, neighbor))  # Edge count as distance

    return distances

def compute_recommendations(preferences, cluster_videos, similarity_data, aggregate_centrality, num_videos):
    user_recommendations = defaultdict(list)
    similarity_lookup = defaultdict(lambda: defaultdict(float))

    # Build similarity lookup
    for video1, video2, similarity in similarity_data:
        similarity_lookup[video1][video2] = similarity
        similarity_lookup[video2][video1] = similarity

    # Compute shortest path distances
    shortest_paths = compute_shortest_paths(similarity_lookup, num_videos)

    # Map videos to clusters
    video_to_cluster = {}
    for cluster_id, videos in cluster_videos.items():
        for video in videos:
            video_to_cluster[video] = cluster_id

    for username, pref_data in preferences.items():
        preferred_videos = pref_data["preferred"]
        non_preferred_videos = pref_data["non_preferred"]
        recommended_videos = []

        # Get clusters of preferred videos
        clusters_to_consider = {video_to_cluster[v] for v in preferred_videos if v in video_to_cluster}

        # Get all videos from these clusters
        candidate_videos = set()
        for cluster_id in clusters_to_consider:
            candidate_videos.update(cluster_videos[cluster_id])

        # Compute RSEF scores for all candidate videos
        for video in candidate_videos:
            if video not in similarity_lookup:
                continue

            rsef_score = 0  # Initialize RSEF score

            # Compute CEF-P contribution (from preferred videos)
            for v in preferred_videos:
                if v in shortest_paths[video] and shortest_paths[video][v] > 0:
                    distance = shortest_paths[video][v]
                    rsef_score += (aggregate_centrality.get(v, 0) / distance)

            # Compute CEF-NP contribution (from non-preferred videos)
            for v in non_preferred_videos:
                if v in shortest_paths[video] and shortest_paths[video][v] > 0:
                    distance = shortest_paths[video][v]
                    rsef_score -= (aggregate_centrality.get(v, 0) / distance)

            recommended_videos.append((video, rsef_score))

        # Sort by score and store top 10 recommendations
        if recommended_videos:
            recommended_videos.sort(key=lambda x: x[1], reverse=True)
            user_recommendations[username] = recommended_videos[:10]  # Keep top 10

    return user_recommendations


def store_recommendations(recommendations):
    cursor.execute("DELETE FROM Recommendations")
    for username, recs in recommendations.items():
        for video_id, rsef_score in recs:
            cursor.execute("INSERT INTO Recommendations (username, video_id, rsef_score) VALUES (?, ?, ?)",
                           (username, video_id, rsef_score))
    conn.commit()

def main():
    similarity_data = fetch_video_similarity()
    preferences = fetch_watch_history()
    cluster_videos = fetch_clusters()
    aggregate_centrality = compute_centrality(similarity_data)
    num_videos = max(max(v1, v2) for v1, v2, _ in similarity_data) + 1
    recommendations = compute_recommendations(preferences, cluster_videos, similarity_data, aggregate_centrality,num_videos)
    print(f"Computed Recommendations: {recommendations}")
    store_recommendations(recommendations)

if __name__ == "__main__":
    main()
    conn.close()
