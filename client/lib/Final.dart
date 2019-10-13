import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';


import 'dart:convert';

import './game.dart';

class Final extends StatefulWidget {
  @override
  _FinalState createState() => new _FinalState();
}

class _FinalState extends State<Final>{
  List<String> litems = ["1","2","Third","4"];
  var _dataFlights = null;

  Future<Null> fetchPost() async {
//    var response = await http.get('http://264ba2f2.ngrok.io');
    while (_dataFlights == null) {
      var response = await http.get('http://52.15.65.153:5000/final');
      if (response.statusCode == 200) {
        // If server returns an OK response, parse the JSON.
        var data = json.decode(response.body);
//      var data = json.decode("{ \"city1\": \"https://instanbul.jpg\", \"city1_name\": \"instanbul\", \"city2\": \"https://instanbul.jpg\", \"city2_name\":     \"barcelona\" }");
        this.setState(() {
          _dataFlights = List.from(data["flights"]);
          print("RAW DATA");
          print(data);
          print("ASSIGNING");
          print(_dataFlights);
        });
      } else {
        // If that response was not OK, throw an error.
        print('Failed to load post');
      }
    }
  }

  @override
  void initState() {
    super.initState();
    fetchPost();
  }

  @override
  Widget build(BuildContext context) {
    if (_dataFlights == null)
      return Scaffold(
        backgroundColor: Colors.blue,
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text("Loading the results...\n", style: TextStyle(color: Colors.white),),
              CircularProgressIndicator(backgroundColor: Colors.green,),
            ],
          ),
        )
      );
    return Scaffold(
      backgroundColor: Colors.blue,
      body: Center(
        child: ListView.builder(
          itemCount: _dataFlights.length,
            itemBuilder: (BuildContext ctxt, int index) {
              print("BUILDING INDEX");
              print(_dataFlights[index]);
              return new Column(
                children: <Widget>[
                  Padding(
                    padding: EdgeInsets.only(left: 30.0, right: 30.0),
                    child:  Image.network(
                      _dataFlights[index]["url"].toString(),
                    ),
                  ),

                  ButtonTheme(
                    minWidth: 300.0,
                    child:RaisedButton(
                      onPressed: null,
                      child: Text(_dataFlights[index]["city"].toString(), style: TextStyle(fontSize: 20)),
                      shape: new RoundedRectangleBorder(
                          borderRadius: new BorderRadius.circular(28.0),
                          side: BorderSide(color: Colors.white)),
                      disabledTextColor: Colors.white,
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 30.0, right: 30.0, bottom: 20.0),
                    child:  Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: <Widget>[
                        ButtonTheme(
                          minWidth: 100.0,
                          child:RaisedButton(
                            onPressed: null,
                            child: Text(_dataFlights[index]["min_price"].toString(), style: TextStyle(fontSize: 15)),
                            shape: new RoundedRectangleBorder(
                                borderRadius: new BorderRadius.circular(28.0),
                                side: BorderSide(color: Colors.white)),
                            disabledTextColor: Colors.white,
                          ),
                        ),
                        ButtonTheme(
                          minWidth: 190.0,
                          child:RaisedButton(
                            onPressed: () async {
                              await _launchURL(_dataFlights[index]["booking_url"]);
                            },
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: <Widget>[
                                Text("Book", style: TextStyle(fontSize: 18)),
                                Padding(
                                  padding: EdgeInsets.only(left: 5.0, right: 5.0),
                                ),
                                Icon(Icons.airplanemode_active, color: Colors.white,)
                              ],
                            ),
                            shape: new RoundedRectangleBorder(
                                borderRadius: new BorderRadius.circular(28.0),
                                side: BorderSide(color: Colors.white)),
                            textColor: Colors.white,
                            color: Colors.green,
                          ),
                        ),

                      ],
                    ),

                  ),
                ],
              );
            }
        ),
      ),
    );
  }

  _launchURL(url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }

}
