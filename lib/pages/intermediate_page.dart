import 'package:chameleo_app/pages/home_page.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:chameleo_app/pages/login_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class IntermediatePage extends StatefulWidget {
  const IntermediatePage({super.key});

  @override
  _IntermediatePageState createState() => _IntermediatePageState();
}

class _IntermediatePageState extends State<IntermediatePage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _usernameController = TextEditingController();
  String? _errorMessage;

  String? _validateUsername(String? value) {
    if (value == null || value.isEmpty) {
      return 'Username cannot be empty';
    }
    if (!RegExp(r'^[a-z0-9_]+$').hasMatch(value)) {
      return 'Only lowercase letters, numbers, and underscores allowed';
    }
    return null;
  }

  Future<void> _loginUser() async {
    if (_formKey.currentState!.validate()) {
      final username = _usernameController.text;
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username}),
      );

      if (response.statusCode == 200) {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => HomePage(username: username)),
        );
      } else {
        final data = json.decode(response.body);
        setState(() {
          _errorMessage = data['error'] ?? 'Login failed';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 178, 206, 122),
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Expanded(
            flex: 5,
            child: Container(
              color: const Color.fromARGB(255, 178, 206, 122),
              child: SizedBox(
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(70, 1, 70, 1),
                  child: Center(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: RichText(
                        textAlign: TextAlign.justify,
                        text: TextSpan(
                          text: "  Welcome\n",
                          style: GoogleFonts.montserrat(
                            fontSize: 90,
                            color: Colors.black,
                            fontWeight: FontWeight.w600,
                          ),
                          children: [
                            TextSpan(
                                text: "to ",
                                style: GoogleFonts.montserrat(
                                  fontSize: 50,
                                  color: Colors.black,
                                  fontWeight: FontWeight.w600,
                                )),
                            TextSpan(
                              text: "Chameleo",
                              style: GoogleFonts.montserratAlternates(
                                fontSize: 57,
                                color: Colors.white,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            TextSpan(
                                text:
                                    ", your personalized video streaming platform.\n",
                                style: GoogleFonts.montserrat(
                                  fontSize: 50,
                                  color: Colors.black,
                                  fontWeight: FontWeight.w600,
                                )),
                            TextSpan(
                                text:
                                    "    Login  to continue and start exploring.    ",
                                style: GoogleFonts.montserrat(
                                  fontSize: 50,
                                  color: Colors.black,
                                  fontWeight: FontWeight.w600,
                                ))
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            flex: 4,
            child: Container(
              height: 700,
              width: 300,
              margin: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                color: Colors.white,
              ),
              child: Center(
                child: SizedBox(
                  width: 300,
                  height: 600,
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Image.asset(
                            "assets/Logo3.png",
                            scale: 1,
                          ),
                          Text(
                            "Login",
                            style: GoogleFonts.montserrat(
                              fontSize: 40,
                              color: Colors.black,
                            ),
                          ),
                          const SizedBox(height: 20),
                          TextFormField(
                            controller: _usernameController,
                            decoration: InputDecoration(
                              labelText: "Username",
                              labelStyle: GoogleFonts.montserrat(
                                fontSize: 20,
                                color: Colors.black,
                              ),
                            ),
                            validator: _validateUsername,
                          ),
                          const SizedBox(height: 20),
                          if (_errorMessage != null)
                            Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: Text(
                                _errorMessage!,
                                style: const TextStyle(color: Colors.red),
                              ),
                            ),
                          ElevatedButton(
                            onPressed: _loginUser,
                            style: ElevatedButton.styleFrom(
                                backgroundColor:
                                    const Color.fromARGB(255, 178, 206, 122),
                                foregroundColor: Colors.black,
                                textStyle: GoogleFonts.montserrat(
                                  fontSize: 20,
                                  color: Colors.black,
                                ),
                                minimumSize: const Size(300, 50)),
                            child: const Text("Login"),
                          ),
                          const SizedBox(height: 18),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => LoginPage()),
                              );
                            },
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.black,
                                foregroundColor: Colors.white,
                                textStyle: GoogleFonts.montserrat(
                                  fontSize: 20,
                                  color: Colors.white,
                                ),
                                minimumSize: const Size(300, 50)),
                            child: const Text("Sign Up"),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}