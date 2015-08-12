# PythonVSido

## これは何？
[アスラテック株式会社](http://www.asratec.co.jp/ "アスラテック株式会社")のロボット制御マイコンボード「[V-Sido CONNECT RC](http://www.asratec.co.jp/product/connect/rc/ "V-Sido CONNECT RC")」をコントロールするためのPythonのサンプルコードです。  
[V-Sido Developerサイトの技術資料](https://v-sido-developer.com/learning/connect/connect-rc/ "V-Sido Developerサイトの技術資料")に公開されている情報を元に個人が作成したもので、アスラテック社公式のツールではありません。  
シリアル接続を経由して、V-Sido CONNECTにコマンドを送ることができます。また、その機能をWebSocket経由で利用するサンプルも含みます。

## 誰が作ったの？
アスラテック株式会社に勤務する今井大介(Daisuke IMAI)が個人として作成しました。

## どうして作ったの？
Start Python Clubさん主催のイベント「業務のためのPython勉強会#3」にお呼ばれしたので、PythonでのV-Sido CONNECTの利用とIoTも含むハードウェアをPythonから活用するアイデアの一端になればと思い書きました。
http://startpython.connpass.com/event/17073/

## 動作環境
Python3系で書きました。

動作確認済み環境は、
* OS X 10.10.4(Yosemite) + Python3.4.3


## 使い方
単体の動作は、

$ python vsido_connect.py [シリアルポートデバイス]  
(引数がない場合は、スクリプト中の規定値になります)  

で、ロボットが歩行します。

画面に表示されるレスポンスは以下のとおりです。  
\> は送信したデータです。  
< は受信したデータです。  

WebSocket経由で命令を受け取るサンプルの動作は、

$ python vsido_connect_server.py [シリアルポートデバイス]  
(引数がない場合は、スクリプト中の規定値になります)  

で、サーバーを起動した後、

ブラウザで、 http://localhost:8080/ を開いてください。

## 免責事項
一応。  

このサンプルコードを利用して発生したいかなる損害についても、アスラテック株式会社ならびに今井大介は責任を負いません。自己責任での利用をお願いします。

## ライセンス
このサンプルコードは、GNU劣等GPLで配布します。  

Copyright (C)2015 Daisuke IMAI \<<hine.gdw@gmail.com>\>  

このライブラリはフリーソフトウェアです。あなたはこれを、フリーソフトウェア財団によって発行されたGNU 劣等一般公衆利用許諾契約書(バージョン2.1か、希望によってはそれ以降のバージョンのうちどれか)の定める条件の下で再頒布または改変することができます。  

このライブラリは有用であることを願って頒布されますが、*全くの無保証*です。商業可能性の保証や特定の目的への適合性は、言外に示されたものも含め全く存在しません。詳しくはGNU 劣等一般公衆利用許諾契約書をご覧ください。  

あなたはこのライブラリと共に、GNU 劣等一般公衆利用許諾契約書の複製物を一部受け取ったはずです。もし受け取っていなければ、フリーソフトウェア財団まで請求してください(宛先は the Free Software Foundation, Inc., 59Temple Place, Suite 330, Boston, MA 02111-1307 USA)。  


Copyright (C) 2015 Daisuke IMAI \<<hine.gdw@gmail.com>\>

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.  

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.  

You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA  
