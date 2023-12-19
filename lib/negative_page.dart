import 'package:flutter/material.dart';

class NegativeCommentsPage extends StatelessWidget {
  final List<String> comments;

  NegativeCommentsPage(this.comments);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Negative Comments'),
      ),
      body: ListView.builder(
        itemCount: comments.length,
        itemBuilder: (context, index) {
          // Check if this is not the last comment to add a divider.
          if (index < comments.length - 1) {
            return Column(
              children: <Widget>[
                ListTile(
                  title: Text(
                    comments[index],
                    style: TextStyle(color: Color(0xFFEB1555)),
                  ),
                ),
                Divider(
                  color: Colors.blue[900],
                  thickness: 1.2, // Adjust the thickness as needed.
                ),
              ],
            );
          } else {
            // For the last comment, don't add a divider.
            return ListTile(
              title: Text(
                comments[index],
                style: TextStyle(color: Color(0xFFEB1555)),
              ),
            );
          }
        },
      ),
      backgroundColor: Color(0xFF111328),
    );
  }
}
