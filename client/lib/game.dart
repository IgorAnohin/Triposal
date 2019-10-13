import 'package:flutter/material.dart';
import 'package:flutter_seekbar/flutter_seekbar.dart' show SeekBar;
import 'package:auto_size_text/auto_size_text.dart';
import 'package:http/http.dart' as http;

import 'dart:convert';
import 'Final.dart';



class Game extends StatefulWidget {
  @override
  _GameState createState() => new _GameState();
}

class _GameState extends State<Game>{

  var _data = null;
  var _value = 0.0;

  Future<Null> fetchPost() async {
//    var response = await http.get('http://264ba2f2.ngrok.io');
    while (_data == null) {
      var response = await http.get('http://52.15.65.153:5000/');
      if (response.statusCode == 200) {
        // If server returns an OK response, parse the JSON.
        var data = json.decode(response.body);
//      var data = json.decode("{ \"city1\": \"https://instanbul.jpg\", \"city1_name\": \"instanbul\", \"city2\": \"https://instanbul.jpg\", \"city2_name\":     \"barcelona\" }");
        this.setState(() {
          _data = data;
          print("ASSIGNING");
          print(_data);
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
    if (_data == null)
      return Scaffold(
          backgroundColor: Colors.blue,
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text("Fetching content...\n", style: TextStyle(color: Colors.white),),
                CircularProgressIndicator(backgroundColor: Colors.green,),
              ],
            ),
          )
      );
    return Scaffold(
      backgroundColor: Colors.blue,
      body: Stack(
        children: <Widget>[
          Center(
            child:Container(
              decoration: new BoxDecoration(
                shape: BoxShape.rectangle,
                color: Colors.white,
                borderRadius: BorderRadius.all(Radius.circular(8.0)),
              ),
              width: 300,
              height: 500,
              child: createQuestion(_data, context),
            ),
          ),
          Container(
            child: Align(
              alignment: FractionalOffset.bottomCenter,
              child: Padding(
                padding: EdgeInsets.only(left: 10.0, right: 10.0, bottom: 20.0),
                child: ButtonTheme(
                  minWidth: 250.0,
                  child:RaisedButton(
                    onPressed: () {
                      Route route = MaterialPageRoute(builder: (context) => Final());
                      Navigator.pushReplacement(context, route);
                    },
                    child: Text("See the results", style: TextStyle(fontSize: 20)),
                    shape: new RoundedRectangleBorder(
                        borderRadius: new BorderRadius.circular(28.0),
                        side: BorderSide(color: Colors.purple)),
                    color: Colors.purple,
                    textColor: Colors.white,
                  ),
                ),
              ),
            ),
          ),
        ]
      )
    );
  }

  Widget createQuestion(data, BuildContext context) {
    if (data["max"] != null)
      return seekBarQuestion(data, context);
    if (data["city1"] != null)
      return imagesQuestions(data, context);
    if (data["type"] != null)
      return binaryQuestion(data, context);

    print(data);
    Route route = MaterialPageRoute(builder: (context) => Final());
    Navigator.pushReplacement(context, route);
  }

  Widget binaryQuestion(data, BuildContext context) {
    var _question = data["question_text"].toString();
    var _image1 = data["image"].toString();
    return Column (
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0, top: 20.0, bottom: 40.0),
          child: AutoSizeText(
            _question,
            style: TextStyle(fontSize: 20),
            maxLines: 2,
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0),
          child: GestureDetector(
            child: Image.network(
              _image1,
              fit: BoxFit.fitWidth,
              width: MediaQuery.of(context).size.width,
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 30.0, right: 30.0, top: 40),
          child: ButtonTheme(
            minWidth: 250.0,
            child: RaisedButton(
              shape: new RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(28.0),
                  side: BorderSide(color: Colors.green)),
              onPressed: () async {
                await sendPost(_data["question_perk"].toString(), 5);
                Route route = MaterialPageRoute(builder: (context) => Game());
                Navigator.pushReplacement(context, route);
                print("PICK UP TRIP WAS PUSHED");
              },
              color: Colors.green,
              textColor: Colors.white,
              child: Text("+", style: TextStyle(fontSize: 20)),
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 30.0, right: 30.0),
          child: ButtonTheme(
            minWidth: 250.0,
            child: RaisedButton(
              shape: new RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(28.0),
                  side: BorderSide(color: Colors.blue)),
              onPressed: () async {
                await sendPost(_data["question_perk"].toString(), 1);
                Route route = MaterialPageRoute(builder: (context) => Game());
                Navigator.pushReplacement(context, route);
                print("PICK UP TRIP WAS PUSHED");
              },
              color: Colors.blue,
              textColor: Colors.white,
              child: Text("-", style: TextStyle(fontSize: 20)),
            ),
          ),
        ),
      ],
    );

  }


  Widget seekBarQuestion(data, BuildContext context) {
    var _max = double.parse(data["max"].toString());
    var _min = double.parse(data["min"].toString());
    var _question = data["question_text"].toString();
    var _image1 = data["image"].toString();
    return Column (
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0, top: 20.0),
          child: AutoSizeText(
            _question,
            style: TextStyle(fontSize: 20),
            maxLines: 2,
          ),
        ),
        Container(
            margin: EdgeInsets.fromLTRB(10, 0, 10, 4),
            width: 250,
            child: SeekBar(
                progresseight: 10,
                value: _min,
                max: _max,
                min: _min,
                sectionCount: ((_max - _min)).toInt(),
                sectionRadius: 5,
                sectionColor: Colors.red,
                sectionUnSelecteColor: Colors.red[100],
                showSectionText: true,
                sectionTextMarginTop: 2,
                sectionDecimal: 0,
                sectionTextColor: Colors.black,
                sectionSelectTextColor: Colors.red,
                sectionTextSize: 14,
                hideBubble: false,
                bubbleRadius: 14,
                bubbleColor: Colors.green,
                bubbleTextColor: Colors.white,
                bubbleTextSize: 14,
                bubbleMargin: 4,
                afterDragShowSectionText: true,
                onValueChanged: (v) {
                  _value =  v.value;
                }
            )
        ),
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0),
          child: GestureDetector(
            child: Image.network(
              _image1,
              fit: BoxFit.fitWidth,
              width: MediaQuery.of(context).size.width,
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 30.0, right: 30.0, bottom: 20.0),
          child: ButtonTheme(
            minWidth: 250.0,
            child: RaisedButton(
              shape: new RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(28.0),
                  side: BorderSide(color: Colors.green)),
              onPressed: () async {
                await sendPost(_data["question_perk"].toString(), _value);
                Route route = MaterialPageRoute(builder: (context) => Game());
                Navigator.pushReplacement(context, route);
                print("PICK UP TRIP WAS PUSHED");
              },
              color: Colors.green,
              textColor: Colors.white,
              child: Text("Next", style: TextStyle(fontSize: 20)),
            ),
          ),
        ),
      ],
    );
  }

  Widget imagesQuestions(data, BuildContext context) {
    var _image1 = data["city1"].toString();
    var _image2 = data["city2"].toString();
    return Column (
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0, top: 20.0),
          child: AutoSizeText(
            "Which view do you prefer?",
            style: TextStyle(fontSize: 20),
            maxLines: 2,
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0),
          child: GestureDetector(
            onTap: () {
              sendImagePost(data["city1_name"].toString());
              Route route = MaterialPageRoute(builder: (context) => Game());
              Navigator.pushReplacement(context, route);
            },
            child: Image.network(
              _image1,
              fit: BoxFit.fitWidth,
              width: MediaQuery.of(context).size.width,
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0),
          child: GestureDetector(
            onTap: () async {
              await sendImagePost(data["city2_name"].toString());
              Route route = MaterialPageRoute(builder: (context) => Game());
              Navigator.pushReplacement(context, route);
            },
            child: Image.network(
              _image2,
              fit: BoxFit.fitWidth,
              width: MediaQuery.of(context).size.width,
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 10.0, right: 10.0, bottom: 20.0),
        ),
      ],
    );
  }

  Future<Null> sendImagePost(String city) async {
    var map = new Map<String, dynamic>();
    map["city"] = city;
//    http.post('http://264ba2f2.ngrok.io', body: map).then((
    print(map);
    print("HERE");
    await http.post('http://52.15.65.153:5000/', body: json.encode(map)).then((http.Response response) {
      final int statusCode = response.statusCode;

      if (statusCode < 200 || statusCode > 400 || json == null) {
        print("Error while fetching data");
      }
      print("AWESOME");
    });
  }

  Future<Null> sendPost(perk, double value) async {
    var map = new Map<String, dynamic>();
    map["question_perk"] = perk;
    map["value"] = value.toInt().toString();
    print(map);
    print("HERE");
//    http.post('http://264ba2f2.ngrok.io', body: map).then((http.Response response) {
    await http.post('http://52.15.65.153:5000/', body: json.encode(map)).then((http.Response response) {
      final int statusCode = response.statusCode;
      print("statusCode $statusCode");
      if (statusCode < 200 || statusCode > 400 || json == null) {
        print("Error while fetching data");
      }
      print("AWESOME");
    });



  }


}

