#!/usr/bin/env python3
import os, urllib.request, json
from flask import Flask, render_template
app = Flask(__name__)

cn_url = "http://b2b.cnyes.com/prop/realquote/Ajax/Get_GE_Data.aspx?All=&U=1&R=123"
tw_url = "http://rate.bot.com.tw/Pages/Static/UIP003.zh-TW.htm"

@app.route('/')
def hello():
  response = urllib.request.urlopen(cn_url)
  html = response.read().decode('utf-8')
  table1, table2, table3, table4, html = html.split('|')
  t1 = json.loads(table1)
  t2 = json.loads(table2)
  # EUR/USD: t2[2], ID='EUR'
  eur_usd = t2[2]['Buy']
  # USD/RMB: t1[1], ID='CNY'
  usd_rmb = t1[1]['Buy']
  # USD/JPY: t2[1], ID='JPY'
  usd_jpy = t2[1]['Buy']

  response = urllib.request.urlopen(tw_url)
  html = response.read().decode('utf-8')
  usd = html.split('USD')[3]
  usd = usd.split("</td>")[3:5]
  usd = [i.split(">")[1] for i in usd]
  usd = sum(float(i) for i in usd) / 2

  jpy = html.split('JPY')[3]
  jpy = jpy.split("</td>")[3:5]
  jpy = [i.split(">")[1] for i in jpy]
  jpy = sum(float(i) for i in jpy) / 2
  return render_template("index.html",eur_usd=eur_usd,usd_rmb=usd_rmb,
      usd_jpy=usd_jpy, usd=usd, jpy = jpy)

if __name__ == "__main__":
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0',port=port)
