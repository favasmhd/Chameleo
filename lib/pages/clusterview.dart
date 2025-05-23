import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ClusterViewPage extends StatefulWidget {
  final String username;
  final String clusterId;

  ClusterViewPage({Key? key, required this.username, required this.clusterId}) : super(key: key);

  @override
  _ClusterViewPageState createState() => _ClusterViewPageState();
}

class _ClusterViewPageState extends State<ClusterViewPage> {
  List<Map<String, dynamic>> clusterVideos = [];

  @override
  void initState() {
    super.initState();
    _loadClusterVideos();
  }

  Future<void> _loadClusterVideos() async {
    try {
      print("Fetching videos for Cluster ID: ${widget.clusterId}");
      
      final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/cluster_videos/${widget.clusterId}'),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        print("API Response: $data");  // Debugging

        if (data['videos'] != null && data['videos'] is List) {
          setState(() {
            clusterVideos = List<Map<String, dynamic>>.from(data['videos']);
          });
        }
      } else {
        print('Failed to load cluster videos: ${response.statusCode}');
      }
    } catch (e) {
      print('Error loading cluster videos: $e');
    }
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Cluster ${widget.clusterId} Videos'),
      ),
      body: clusterVideos.isEmpty
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: clusterVideos.length,
              itemBuilder: (context, index) {
                final video = clusterVideos[index];
                return ListTile(
                  leading: Icon(Icons.video_library),
                  title: Text(video['title']),
                  subtitle: Text(
  (video['tags'] is List) ? video['tags'].join(', ') : video['tags'].toString(),
),

                  onTap: () {
                    // Handle video playback or details page
                  },
                );
              },
            ),
    );
  }
}
