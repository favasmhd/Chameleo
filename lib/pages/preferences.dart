import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:chameleo_app/pages/home_page.dart';
import 'package:chameleo_app/pages/intermediate_page.dart';
import 'package:chameleo_app/pages/clusterview.dart';

class PreferencesPage extends StatefulWidget {
  final String username;

  PreferencesPage({Key? key, required this.username}) : super(key: key);

  @override
  _PreferencesPageState createState() => _PreferencesPageState();
}

class _PreferencesPageState extends State<PreferencesPage> {
  List<String> userClusters = [];

  @override
  void initState() {
    super.initState();
    fetchUserClusters();
  }

  Future<void> fetchUserClusters() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/user_clusters/${widget.username}'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          userClusters = List<String>.from(data['clusters']);
        });
      } else {
        print('Failed to load clusters: ${response.statusCode}');
      }
    } catch (e) {
      print('Error loading clusters: $e');
    }
  }

  Future<void> optOutCluster(String clusterId) async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/opt_out'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({'username': widget.username, 'cluster_id': clusterId}),
      );

      if (response.statusCode == 200) {
        setState(() {
          userClusters.remove(clusterId);
        });
      } else {
        print('Failed to opt out: ${response.statusCode}');
      }
    } catch (e) {
      print('Error opting out: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        automaticallyImplyLeading: false,
        toolbarHeight: 80,
        title: Row(
          children: [
            Image.asset("assets/Logo3.png", scale: 1, height: 40),
            const SizedBox(width: 20),
            const Text("Preferences", style: TextStyle(color: Colors.black)), 
          ],
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: PopupMenuButton<String>(
              icon: CircleAvatar(backgroundColor: Colors.grey.shade300, child: const Icon(Icons.person, color: Colors.black)),
              onSelected: (value) {
                if (value == "Logout") {
                  Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => IntermediatePage()));
                }
              },
              itemBuilder: (context) => [
                PopupMenuItem(enabled: false, value: "Username", child: Text(widget.username)),
                const PopupMenuItem(value: "Logout", child: Text("Logout")),
              ],
            ),
          ),
        ],
      ),
      body: Row(
        children: [
          NavigationRail(
            backgroundColor: Colors.white,
            selectedIndex: 1, 
            onDestinationSelected: (index) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (context) => index == 0 ? HomePage(username: widget.username) : PreferencesPage(username: widget.username)),
              );
            },
            labelType: NavigationRailLabelType.all,
            destinations: const [
              NavigationRailDestination(icon: Icon(Icons.home_outlined), label: Text("Home")),
              NavigationRailDestination(icon: Icon(Icons.settings_outlined), label: Text("Preferences")),
            ],
            minWidth: 80,
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: userClusters.isEmpty
                  ? const Center(child: CircularProgressIndicator())
                  : ListView.builder(
                      itemCount: userClusters.length,
                      itemBuilder: (context, index) {
                        String clusterId = userClusters[index];

                        return Card(
                          margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                          child: ListTile(
                            title: Text("Cluster: $clusterId", style: const TextStyle(fontSize: 18)),
                            trailing: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                ElevatedButton(
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => ClusterViewPage(username: widget.username, clusterId: clusterId),
                                      ),
                                    );
                                  },
                                  child: const Text("View"),
                                ),
                                const SizedBox(width: 10),
                                ElevatedButton(
                                  onPressed: () {
                                    optOutCluster(clusterId);
                                  },
                                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                                  child: const Text("Opt-Out", style: TextStyle(color: Colors.white)),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ),
        ],
      ),
    );
  }
}
