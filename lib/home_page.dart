import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:gradient_slide_to_act/gradient_slide_to_act.dart';
import 'package:major_project/negative_page.dart';
import 'package:major_project/neutral_page.dart';
import 'package:major_project/positive_page.dart';

enum CommentCategory { Positive, Negative, Neutral }

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String videoUrl = '';
  Map<String, dynamic> categorizedComments = {};
  CommentCategory selectedCategory = CommentCategory.Positive;

  Future<void> fetchData() async {
    try {
      final response = await http.post(
        Uri.parse(
            'http://192.168.29.188:5000/analyze_video'), // Replace with your server URL.
        body: {'video_url': videoUrl},
      );

      print(response.body);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          categorizedComments = data;
        });
      } else {
        // Handle API request error.
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text('API Error'),
              content:
                  Text('An error occurred while fetching data from the server'),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: Text('OK'),
                )
              ],
            );
          },
        );
      }
    } catch (e) {
      // Handle exception.
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text('API Error'),
            content: Text('An error occurred while making the API request'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text('OK'),
              ),
            ],
          );
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          title: Text(
            'Comment Manager',
            style: TextStyle(fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          backgroundColor: Color.fromARGB(255, 105, 159, 240),
        ),
        body: SingleChildScrollView(
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: TextField(
                  style: TextStyle(color: Colors.black),
                  onChanged: (value) {
                    setState(() {
                      videoUrl = value;
                    });
                  },
                  decoration: InputDecoration(
                    hintText: 'Enter YouTube Video URL',
                    hintStyle: TextStyle(color: Colors.grey),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(25.0),
                      borderSide: BorderSide(
                        color: Colors.blue,
                      ),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(25.0),
                      borderSide: BorderSide(
                        color: Colors.orange,
                      ),
                    ),
                  ),
                ),
              ),
              SizedBox(
                height: 30,
              ),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 15),
                width: MediaQuery.of(context).size.width * 1.4,
                child: GradientSlideToAct(
                  text: 'Analyze Video',
                  textStyle: TextStyle(color: Colors.white, fontSize: 15),
                  backgroundColor: Color(0Xff172663),
                  onSubmit: () {
                    fetchData();
                  },
                  gradient: const LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [Color(0xff0da6c2), Color(0xff0E39C6)],
                  ),
                  // Add your button text here
                ),
              ),
              SizedBox(
                height: 22,
              ),
              Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: <Widget>[
                      GestureDetector(
                        onTap: () {
                          if (categorizedComments != null &&
                              categorizedComments['positive_comments'] !=
                                  null) {
                            final List<String>? positiveComments =
                                (categorizedComments['positive_comments']
                                        as List<dynamic>)
                                    ?.map((comment) => comment.toString())
                                    .toList();

                            if (positiveComments != null &&
                                positiveComments.isNotEmpty) {
                              Navigator.of(context).push(MaterialPageRoute(
                                builder: (context) {
                                  return PositiveCommentsPage(positiveComments);
                                },
                              ));
                            } else {
                              // Handle the case when positive comments are not available.
                              showDialog(
                                context: context,
                                builder: (BuildContext context) {
                                  return AlertDialog(
                                    title: Text('Positive Comments'),
                                    content:
                                        Text('No positive comments available.'),
                                    actions: [
                                      TextButton(
                                        onPressed: () {
                                          Navigator.of(context).pop();
                                        },
                                        child: Text('OK'),
                                      )
                                    ],
                                  );
                                },
                              );
                            }
                          }
                        },
                        child: Container(
                          child: Column(
                            children: [
                              SizedBox(
                                height: 15,
                              ),
                              Icon(
                                Icons.thumb_up_sharp,
                                size: 55,
                              ),
                              Text(
                                'Positive',
                                style: TextStyle(
                                    fontSize: 20, fontWeight: FontWeight.bold),
                              )
                            ],
                          ),
                          height: 110,
                          width: 120,
                          decoration: BoxDecoration(
                              color: const Color.fromARGB(255, 108, 162, 244),
                              borderRadius: BorderRadius.circular(15)),
                        ),
                      ),
                      GestureDetector(
                        onTap: () {
                          if (categorizedComments != null &&
                              categorizedComments['negative_comments'] !=
                                  null) {
                            final List<String>? negativeComments =
                                (categorizedComments['negative_comments']
                                        as List<dynamic>)
                                    ?.map((comment) => comment.toString())
                                    .toList();

                            if (negativeComments != null &&
                                negativeComments.isNotEmpty) {
                              Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (context) {
                                    return NegativeCommentsPage(
                                        negativeComments);
                                  },
                                ),
                              );
                            } else {
                              // Handle the case when negative comments are not available.
                              showDialog(
                                context: context,
                                builder: (BuildContext context) {
                                  return AlertDialog(
                                    title: Text('Negative Comments'),
                                    content:
                                        Text('No negative comments available.'),
                                    actions: [
                                      TextButton(
                                        onPressed: () {
                                          Navigator.of(context).pop();
                                        },
                                        child: Text('OK'),
                                      )
                                    ],
                                  );
                                },
                              );
                            }
                          }
                        },
                        child: Container(
                          child: Column(
                            children: [
                              SizedBox(
                                height: 15,
                              ),
                              Icon(
                                Icons.thumb_down_sharp,
                                size: 55,
                              ),
                              Text(
                                'Negative',
                                style: TextStyle(
                                    fontSize: 20, fontWeight: FontWeight.bold),
                              )
                            ],
                          ),
                          height: 110,
                          width: 120,
                          decoration: BoxDecoration(
                              color: Color.fromARGB(255, 108, 162, 244),
                              borderRadius: BorderRadius.circular(15)),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  GestureDetector(
                    onTap: () {
                      if (categorizedComments != null &&
                          categorizedComments['neutral_comments'] != null) {
                        final List<String>? neutralComments =
                            (categorizedComments['neutral_comments']
                                    as List<dynamic>)
                                ?.map((comment) => comment.toString())
                                .toList();

                        if (neutralComments != null &&
                            neutralComments.isNotEmpty) {
                          Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) {
                              return NeutralCommentsPage(neutralComments);
                            },
                          ));
                        } else {
                          // Handle the case when neutral comments are not available.
                          showDialog(
                            context: context,
                            builder: (BuildContext context) {
                              return AlertDialog(
                                title: Text('Neutral Comments'),
                                content: Text('No neutral comments available.'),
                                actions: [
                                  TextButton(
                                    onPressed: () {
                                      Navigator.of(context).pop();
                                    },
                                    child: Text('OK'),
                                  )
                                ],
                              );
                            },
                          );
                        }
                      }
                    },
                    child: Container(
                      child: Column(
                        children: [
                          SizedBox(height: 18),
                          Icon(
                            Icons.equalizer,
                            size: 55,
                          ),
                          Text(
                            'Neutral',
                            style: TextStyle(
                                fontSize: 20, fontWeight: FontWeight.bold),
                          )
                        ],
                      ),
                      height: 110,
                      width: 285,
                      decoration: BoxDecoration(
                          color: Color.fromARGB(255, 108, 162, 244),
                          borderRadius: BorderRadius.circular(15)),
                    ),
                  ),
                ],
              ),
              // Display categorized comments based on the selected category.
            ],
          ),
        ),
      ),
    );
  }
}
