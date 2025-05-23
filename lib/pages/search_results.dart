import 'package:chameleo_app/pages/home_page.dart';
import 'package:chameleo_app/pages/intermediate_page.dart';
import 'package:chameleo_app/pages/preferences.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class SearchResultsPage extends StatefulWidget {
  final String query;
  final String username;

  SearchResultsPage({required this.query, required this.username});

  @override
  _SearchResultsPageState createState() => _SearchResultsPageState();
}

class _SearchResultsPageState extends State<SearchResultsPage> {
  List<dynamic> _searchResults = [];
  List<String> _searchSuggestions = [];
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchSearchResults(widget.query);
    _searchController.text = widget.query;
  }

  Future<void> _fetchSearchResults(String query) async {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:5000/search?q=$query'),
    );

    print('API Response Status Code: ${response.statusCode}');
    print('API Response Body: ${response.body}');
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        _searchResults = data['results'];
      });
    } else {
      setState(() {
        _searchResults = [];
      });
    }
  }

  Future<void> _fetchSearchSuggestions(String query) async {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:5000/search/suggestions?q=$query'),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        _searchSuggestions = List<String>.from(data['suggestions']);
      });
    } else {
      setState(() {
        _searchSuggestions = [];
      });
    }
  }

  void _onSearchSubmitted(String query) {
    setState(() {
      _searchResults = [];
    });
    _fetchSearchResults(query);
  }

  void _playVideo(String videoPath) async {
    try {
      Process.run('cvlc', [videoPath], runInShell: true);
    } catch (e) {
      print('Error playing video: $e');
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
            SizedBox(width: 20),
            Expanded(
              child: Autocomplete<String>(
                optionsBuilder: (TextEditingValue textEditingValue) {
                  if (textEditingValue.text == '') {
                    return const Iterable<String>.empty();
                  }
                  _fetchSearchSuggestions(textEditingValue.text);
                  return _searchSuggestions.where((String option) {
                    return option
                        .toLowerCase()
                        .contains(textEditingValue.text.toLowerCase());
                  });
                },
                onSelected: (String suggestion) {
                  _searchController.text = suggestion;
                  _onSearchSubmitted(suggestion);
                },
                fieldViewBuilder: (BuildContext context,
                    TextEditingController textEditingController,
                    FocusNode focusNode,
                    VoidCallback onFieldSubmitted) {
                  return TextField(
                    controller: textEditingController,
                    focusNode: focusNode,
                    decoration: InputDecoration(
                      hintText: "Search...",
                      hintStyle: GoogleFonts.montserrat(
                          fontSize: 14, color: Colors.grey),
                      prefixIcon: Icon(Icons.search, size: 20),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(25),
                        borderSide: BorderSide(color: Colors.grey),
                      ),
                      filled: true,
                      fillColor: Colors.grey[200],
                      contentPadding:
                          EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                    ),
                    onSubmitted: (String value) {
                      _onSearchSubmitted(value);
                    },
                  );
                },
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
            onDestinationSelected: (int index) {
              if (index == 0) {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (context) => HomePage(username: widget.username),
                  ),
                );
              } else if (index == 1) {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => PreferencesPage(username: widget.username),
                  ),
                );
              }
            },
            labelType: NavigationRailLabelType.all,
            destinations: [
              NavigationRailDestination(
                icon: Icon(Icons.home_outlined),
                label: Text("Home"),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.settings_outlined),
                label: Text("Preferences"),
              ),
            ],
            minWidth: 80,
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: ListView.builder(
                itemCount: _searchResults.length,
                itemBuilder: (context, index) {
                  final video = _searchResults[index];
                  return InkWell(
                    onTap: () => _playVideo(video['file_path']),
                    child: Card(
                      color: Colors.grey[300],
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Container(
                              width: 160,
                              height: 90,
                              color: Colors.grey[400],
                            ),
                            SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    video['title'],
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                    maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    SizedBox(height: 8),
                                    Text(
                                      video['tags'].join(', '),
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.grey[600],
                                      ),
                                      maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
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