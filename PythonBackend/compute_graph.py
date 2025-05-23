import sqlite3
import igraph as ig
import leidenalg as la
from collections import defaultdict

db_path = "chameleo.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def fetch_interactions():
    """ Fetch user-video interactions from the database. """
    cursor.execute("SELECT username, video_id, watch_percentage FROM UserVideoInteraction")
    return cursor.fetchall()

def compute_similarity(interactions):
    video_users_weights = defaultdict(lambda: defaultdict(float))

    for username, video_id, watch_percentage in interactions:
        video_users_weights[video_id][username] = watch_percentage

    similarity_edges = {}
    video_ids = list(video_users_weights.keys())

    for i in range(len(video_ids)):
        for j in range(i + 1, len(video_ids)):
            v1, v2 = video_ids[i], video_ids[j]
            users_v1, users_v2 = video_users_weights[v1], video_users_weights[v2]

            intersection_sum = 0.0
            union_users = set(users_v1.keys()) | set(users_v2.keys())

            for user in union_users:
                weight_v1 = users_v1.get(user, 0.0)
                weight_v2 = users_v2.get(user, 0.0)
                intersection_sum += min(weight_v1, weight_v2)

            sum_v1 = sum(users_v1.values())
            sum_v2 = sum(users_v2.values())
            union_sum = sum_v1 + sum_v2 - intersection_sum

            if union_sum > 0:
                similarity = intersection_sum / union_sum
                if similarity > 0.2:
                    similarity_edges[(v1, v2)] = similarity
                    similarity_edges[(v2, v1)] = similarity

    return video_ids, similarity_edges

def store_video_similarity(similarity_edges):
    """ Store computed video similarities in the database. """
    cursor.execute("DELETE FROM VideoSimilarity")

    for (video1, video2), similarity in similarity_edges.items():
        cursor.execute("INSERT INTO VideoSimilarity (video1_id, video2_id, similarity) VALUES (?, ?, ?)", 
                       (video1, video2, similarity))
    
    conn.commit()
    print("Video similarity data stored successfully.")

def apply_leiden_clustering(video_ids, similarity_edges):
    g = ig.Graph()

    video_to_index = {video_id: i for i, video_id in enumerate(video_ids)}
    g.add_vertices(len(video_ids))

    edge_list = [(video_to_index[v1], video_to_index[v2]) for v1, v2 in similarity_edges.keys()]
    weights = list(similarity_edges.values())

    g.add_edges(edge_list)
    g.es['weight'] = weights

    partition = la.find_partition(g, la.CPMVertexPartition, resolution_parameter=1)

    cluster_mapping = {video_id: partition.membership[video_to_index[video_id]] for video_id in video_ids}

    print("Cluster Assignments:", cluster_mapping)
    
    for i in range(0,8):
        print("Cluster",i)
        for j in cluster_mapping:
            if cluster_mapping[j] == i:
                print(j)
                
    return cluster_mapping

def store_clusters(cluster_mapping):
    """ Store computed clusters in the database. """
    cursor.execute("DELETE FROM Clusters")

    for video_id, cluster_id in cluster_mapping.items():
        cursor.execute("INSERT INTO Clusters (cluster_id, video_id) VALUES (?, ?)", (cluster_id, video_id))

    conn.commit()
    print("Cluster data stored successfully.")

def main():
    interactions = fetch_interactions()

    video_ids, similarity_edges = compute_similarity(interactions)
    
    if not similarity_edges:
        print("No video similarities found. Skipping storage and clustering.")
        return

    store_video_similarity(similarity_edges)

    cluster_mapping = apply_leiden_clustering(video_ids, similarity_edges)
    store_clusters(cluster_mapping)

    print("Graph computations, similarity storage, and Leiden clustering completed.")

if __name__ == "__main__":
    main()
    conn.close()
