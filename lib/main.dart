import 'package:flutter/material.dart';
import 'package:rive/rive.dart';
import 'package:chameleo_app/pages/intermediate_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: RivePlayer(),
    );
  }
}

class RivePlayer extends StatelessWidget {
  const RivePlayer({super.key});

  @override
  Widget build(BuildContext context) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Future.delayed(const Duration(milliseconds: 3080), () {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const IntermediatePage()),
        );
      });
    });

    return const Scaffold(
      body: Center(
        child: RiveAnimation.asset(
          'assets/chameleo.riv',
          fit: BoxFit.cover,
        ),
      ),
    );
  }
}
