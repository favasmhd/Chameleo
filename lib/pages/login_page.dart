import 'package:chameleo_app/pages/intermediate_page.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Scaffold(
        backgroundColor: Color.fromARGB(255, 178, 206 ,122),
        body: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Expanded(
              flex: 5,
              child: Container(
                color: Color.fromARGB(255, 178, 206 ,122),
                child: SizedBox(
                  child: Padding(
                    padding: EdgeInsets.fromLTRB(70, 1, 70, 1),
                    child:Center(
                      child: Padding(
                        padding: const EdgeInsets.all(20),
                        child: RichText(
                          textAlign: TextAlign.justify,
                          text:
                              TextSpan(
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
                                      fontSize:50,
                                      color: Colors.black,
                                      fontWeight: FontWeight.w600,
                                    )
                                  ),
                                  TextSpan(
                                    text: "Chameleo",
                                    style: GoogleFonts.montserratAlternates(
                                      fontSize: 57,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  TextSpan(
                                    text: ", your personalized video streaming platform.\n",
                                    style: GoogleFonts.montserrat(
                                      fontSize: 50,
                                      color: Colors.black,
                                      fontWeight: FontWeight.w600,
                                    )
                                  ),
                                  TextSpan(
                                    text: "    Login  to continue and start exploring.    ",
                                    style: GoogleFonts.montserrat(
                                      fontSize: 50,
                                      color: Colors.black,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  )
                                ]
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
                margin: EdgeInsets.all(20),
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
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Image.asset(
                            "assets/Logo3.png",
                            scale: 1,
                          ),
                          Text(
                            "Login",
                            style:GoogleFonts.montserrat(
                              fontSize: 40,
                              color: Colors.black,
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          
                          SizedBox(
                            height: 20,                          
                          ),
                          
                          TextField(
                            decoration: InputDecoration(
                              labelText: "Userame",
                              labelStyle: GoogleFonts.montserrat(
                                fontSize: 20,
                                color: Colors.black,
                              )
                            ),
                          ),
                          
                          SizedBox(
                            height: 20,
                          ),

                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => IntermediatePage()),
                              );
                            },
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Color.fromARGB(255, 0, 0, 0),
                                foregroundColor: const Color.fromARGB(255, 255, 255, 255),
                                textStyle: GoogleFonts.montserrat(
                                fontSize: 20,
                                color: Colors.black,
                              ),
                              minimumSize: Size(300, 50)
                            ),
                            child: Text("Register"),
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          SizedBox(
                            height: 20,
                            child: Text("Already a user?"),
                          ),
                          
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => IntermediatePage()),
                              );
                            },
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Color.fromARGB(255, 178, 206 ,122),
                                foregroundColor: Colors.black,
                                textStyle: GoogleFonts.montserrat(
                                fontSize: 20,
                                color: Colors.black,
                              ),
                              minimumSize: Size(300, 50)
                            ),
                            child: Text("Login"),
                          ),
                          SizedBox(
                            height: 18,
                          ),
                          
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            )
          ]
        )
      ),
      ],
    );
  }
}
