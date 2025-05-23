import 'package:chameleo_app/pages/intermediate_page.dart';
import 'package:chameleo_app/pages/preferences.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'search_results.dart';
import 'dart:io'; // Import dart:io for process execution
import 'package:path/path.dart' as p;

class HomePage extends StatefulWidget {
  final String username;
  HomePage({Key? key, required this.username}) : super(key: key);
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<VideoItem> videoItems = [];
  List<String> _searchSuggestions = [];
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadVideos();
  }

  Future<void> _loadVideos() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/recommendations/${widget.username}'),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);

        if (data['recommendations'] != null && data['recommendations'] is List &&
    data['recommendations'].isNotEmpty) {
          setState(() {
            videoItems = (data['recommendations'] as List)
                .map((item) => VideoItem(
                      filePath: item['file_path'],
                      title: item['title'],
                      tags: item['tags'].toString(),
                    ))
                .toList();
          });
        } else {
          print('No recommendations found. Loading popular videos...');
          final popularResponse = await http.get(
            Uri.parse('http://127.0.0.1:5000/popular'),
          );

          if (popularResponse.statusCode == 200) {
            final Map<String, dynamic> popularData = json.decode(popularResponse.body);

            setState(() {
              videoItems = (popularData['popular_videos'] as List)
                  .map((item) => VideoItem(
                        filePath: item['file_path'],
                        title: item['title'],
                        tags: item['tags'].toString(),
                      ))
                  .toList();
            });
          }
        }
      } else {
        print('Failed to load videos: ${response.statusCode}');
      }
    } catch (e) {
      print('Error loading videos: $e');
    }
  }



  Future<void> _fetchSearchSuggestions(String query) async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/search/suggestions?q=$query'));
    _searchSuggestions = response.statusCode == 200 ? List<String>.from(json.decode(response.body)['suggestions']) : [];
    setState(() {});
  }

  void _onSearchSubmitted(String query) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => SearchResultsPage(query: query, username: widget.username)));
  }

  Future<void> _playVideoWithCvlc(String filePath) async {
  try {
    String fullVideoPath = p.absolute(filePath);

    Process.start(
      '/usr/bin/cvlc',
      [fullVideoPath, '--no-fullscreen', '--no-one-instance', '--vout=x11'],
    ).then((process) {
      process.stdout.transform(utf8.decoder).listen((data) {
        print('cvlc stdout: $data');
      });
      process.stderr.transform(utf8.decoder).listen((data) {
        print('cvlc stderr: $data');
      });
      process.exitCode.then((exitCode) {
        print('cvlc exitCode: $exitCode');
        if (exitCode != 0) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Could not play video with cvlc.')),
          );
        }
      });
    });
  } catch (e) {
    print('Error playing video with cvlc: $e');
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Error: ${e.toString()}')),
    );
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
            Expanded(
              child: Autocomplete<String>(
                optionsBuilder: (textEditingValue) {
                  if (textEditingValue.text.isEmpty) return const Iterable<String>.empty();
                  _fetchSearchSuggestions(textEditingValue.text);
                  return _searchSuggestions.where((option) => option.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                },
                onSelected: (suggestion) {
                  _searchController.text = suggestion;
                  _onSearchSubmitted(suggestion);
                },
                fieldViewBuilder: (context, controller, focusNode, onSubmitted) => TextField(
                  controller: controller,
                  focusNode: focusNode,
                  decoration: InputDecoration(
                    hintText: "Search...",
                    prefixIcon: const Icon(Icons.search, size: 20),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(25), borderSide: const BorderSide(color: Colors.grey)),
                    filled: true,
                    fillColor: Colors.grey[200],
                    contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                  ),
                  onSubmitted: _onSearchSubmitted,
                ),
              ),
            ),
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
                } else if (value == "Preferences") {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => PreferencesPage(username: widget.username)));
                }
              },
              itemBuilder: (context) => [
                PopupMenuItem(enabled: false, value: "Username", child: Text(widget.username)),
                const PopupMenuItem(value: "Preferences", child: Text("Preferences")),
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
            selectedIndex: 0,
            onDestinationSelected: (index) {
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => index == 0 ? HomePage(username: widget.username) : PreferencesPage(username: widget.username)));
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
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                  mainAxisExtent: 250,
                ),
                itemCount: videoItems.length,
                itemBuilder: (context, index) => InkWell(
                  onTap: () {
                    _playVideoWithCvlc(videoItems[index].filePath);
                  },
                  child: Card(
                    elevation: 4,
                    color: Colors.grey[200],
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            height: 125,
                            width: double.infinity,
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            videoItems[index].title,
                            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            videoItems[index].tags,
                            style: const TextStyle(fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class VideoItem {
  final String filePath;
  final String title;
  final String tags;
  VideoItem({required this.filePath, required this.title, required this.tags});
}