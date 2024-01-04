from flask import make_response
import requests
import functions_framework
import json

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    print(type(request_json), request_json)
    if request.method == "POST":
      if request_json['events'][0]['type'] == "message":
        if "จับฉลาก" in request_json['events'][0]['message']["text"]:
          # reply(request_json, json.dumps(request_json))
          reply(request_json, "ลงทะเบียนเสร็จแล้ววววว")
          push(request_json['events'][0]['source']["userId"], "ประกาศผลจับฉลาก 14 ธันวาคม เวลา 18:00:00 น.")
          push(request_json['events'][0]['source']["userId"], "https://www.youtube.com/watch?v=-KF7cYrmAWQ")
          linenotify(request_json)

    response = make_response(request.method, "Done")
    response.status_code = 200
    return response

def push(userId,text):
  LINE_MESSAGING_API = 'https://api.line.me/v2/bot/message/push'
  LINE_HEADER = {'Content-Type': 'application/json', 'Authorization': 'Bearer xBw+kSxKXyTNCmilIz3Fb5iItd05V/LBjEaHs7fh93ySp0Mw7c99c18Kpi2BZ79xELBfY05oboPbugKEyRhbeu9ZZJuCZRh0yaJCo8X2j76QAOg1oPPcocjHFOw4XP/oj2XF/HkNygE8kT8DG6QNjQdB04t89/1O/w1cDnyilFU='}
  data = {
      "to": userId,
      'messages': [
          {
              'type': 'text',
              'text': text
          }
      ]
  }
  response = requests.post(LINE_MESSAGING_API, headers=LINE_HEADER, data=json.dumps(data))
  if response.status_code == 200:
      return response.json()    
  else:
      return {"Execute error:" : response.text}

def reply(body_response, text):
  LINE_MESSAGING_API = 'https://api.line.me/v2/bot/message/reply'
  LINE_HEADER = {'Content-Type': 'application/json', 'Authorization': 'Bearer xBw+kSxKXyTNCmilIz3Fb5iItd05V/LBjEaHs7fh93ySp0Mw7c99c18Kpi2BZ79xELBfY05oboPbugKEyRhbeu9ZZJuCZRh0yaJCo8X2j76QAOg1oPPcocjHFOw4XP/oj2XF/HkNygE8kT8DG6QNjQdB04t89/1O/w1cDnyilFU='}
  response_token = body_response['events'][0]['replyToken']
  data = {
    'replyToken': response_token,
    'messages': [
      {
        'type': 'text',
        'text': text
      }
    ]
  }
  response = requests.post(LINE_MESSAGING_API, headers=LINE_HEADER, data=json.dumps(data))
  if response.status_code == 200:
    return response.json()    
  else:
    return {"Execute error:" : response.text}
  
def linenotify(body_response):
    url = 'https://notify-api.line.me/api/notify'
    token = "XTvmT6K4Ma4nC8Kp88JEaS9RGZuV9gJe7vDaO3iy7Xg" # Line Notify Token
    text = f"{body_response['events'][0]['message']['text']}\n{body_response['events'][0]['source']['userId']}"
    data = {'message': text}
    headers = {'Authorization':'Bearer ' + token}
    session = requests.Session()
    session_post = session.post(url, headers=headers, data =data)
