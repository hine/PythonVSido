import serial
import threading

import tornado.ioloop
import tornado.web
import tornado.websocket

DEFAULT_PORT = '/dev/tty.usbserial'
DEFAULT_BAUTRATE = 115200

# V-Sido CONNECTのためのclass
class VSidoConnect(object):

    # V-Sidoで利用するコマンドやオペランドのクラス変数定義
    COMMAND_ST = 0xff;
    COMMAND_OP_ANGLE = 0x6f; # 'o'
    COMMAND_OP_IK = 0x6b; # 'k'
    COMMAND_OP_WALK = 0x74; # 't'
    COMMAND_OP_SETVID = 0x73; # 's'
    COMMAND_OP_GPIO = 0x69; # 'i'
    COMMAND_OP_PWM = 0x70; # 'p'

    def __init__(self, port, baudrate):
        # インスタンス生成時にシリアル接続
        self.serial = serial.serial_for_url(port, baudrate, timeout=1)
        self.recieve_buffer = []
        self.message_buffer = []

    def start_reciever(self):
        """ 受信スレッドを立ち上げる """
        self.receiver_alive = True
        self.receiver_thread = threading.Thread(target=self._reciever)
        self.receiver_thread.setDaemon(True)
        self.receiver_thread.start()

    def stop_reciever(self):
        """ 受信スレッドの停止 """
        self.receiver_alive = False
        self.receiver_thread.join()

    def _reciever(self):
        """ 受信データの処理 """
        try:
            while self.receiver_alive:
                data = self.serial.read(1)
                if len(data) > 0:
                    if data == 0xff:
                        self.recieve_buffer = []
                    self.recieve_buffer.append(int.from_bytes(data, byteorder='big'))
                    if len(self.recieve_buffer) > 3:
                        if len(self.recieve_buffer) == self.recieve_buffer[2]:
                            recieve_buffer_str = []
                            for data in self.recieve_buffer:
                                recieve_buffer_str.append('%02x' % data)
                            print('< ' + ' '.join(recieve_buffer_str))
                            self.message_buffer.append('{"type":"received", "data":"' + ' '.join(recieve_buffer_str) + '"}')
                            self.recieve_buffer = []
        except serial.SerialException:
            self.alive = False
            raise

    def send_data(self, command_data):
        ''' コマンド送信 '''
        data_bytes = b''
        data_str = []
        for data in command_data:
            data_bytes += data.to_bytes(1, byteorder='little')
            data_str.append('%02x' % data)
        self.serial.write(data_bytes)
        print('> ' + ' '.join(data_str))
        self.message_buffer.append('{"type":"sent", "data":"' + ' '.join(data_str) + '"}')

    def _make_2byte_data(self, value):
        ''' 2Byteデータを送る場合のff回避ロジック(V-Sido CONNECT RCコマンドリファレンス参照) '''
        value_bytes = value.to_bytes(2, byteorder='big', signed=True)
        return [(value_bytes[1] << 1) & 0x00ff, (value_bytes[0] << 2) & 0x00ff]

    def _adjust_ln_sum(self, command_data):
        ''' コマンドデータのLN(レングス)とSUM(チェックサム)の調整 '''
        #
        ln_pos = 1 if command_data[0] == 0x0c or command_data[0] == 0x0d or command_data[0] == 0x53 or command_data[0] == 0x54 else 2
        if len(command_data) > 3:
            command_data[ln_pos] = len(command_data);
            sum = 0;
            for data in command_data:
                sum ^= data
            command_data[len(command_data) - 1] = sum
            return command_data

    def make_walk_command(self, forward, turn_cw):
        ''' 歩行コマンドのデータ生成 '''
        data = []
        data.append(VSidoConnect.COMMAND_ST) # ST
        data.append(VSidoConnect.COMMAND_OP_WALK) # OP
        data.append(0x00) # LN仮置き
        data.append(0x00) # WAD(Utilityでは0で固定)
        data.append(0x02) # WLN(現在2で固定)
        # 速度ならびに旋回は-100〜100を0〜200に変換する
        data.append(forward + 100)
        data.append(turn_cw + 100)
        data.append(0x00) # SUM仮置き
        return self._adjust_ln_sum(data);


# Tornadoのためのclass
class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


class SocketHandler(tornado.websocket.WebSocketHandler):
    #on_message -> receive data
    #write_message -> send data

    def open(self):
        self.i = 0
        self.callback = tornado.ioloop.PeriodicCallback(self._send_message, 50)
        self.callback.start()
        print("WebSocket opened")

    # origin check disabled
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("got message:",message)
        if message == "walk_forward":
             if vsidoconnect:
                 vsidoconnect.send_data(vsidoconnect.make_walk_command(100, 0))

    def _send_message(self):
        if len(vsidoconnect.message_buffer) > 0:
            self.write_message(vsidoconnect.message_buffer.pop(0))

    def on_close(self):
        self.callback.stop()
        print("WebSocket closed")


# アプリケーション割り当て
web_app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/ws", SocketHandler),
])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':

    import sys
    import time

    print("=== Python V-Sido Server TEST ===")

    # 引数からシリアルポートを決定する
    if len(sys.argv) == 1:
        port = DEFAULT_PORT
    else:
        port = sys.argv[1]
    baudrate = DEFAULT_BAUTRATE

    # V-Sido CONNECT用のインスタンス生成（初期化でシリアルポートをオープンする）
    print("Connecting to robot...", end="")
    try:
        vsidoconnect = VSidoConnect(
            port,
            baudrate
        )
    except serial.SerialException:
        sys.stderr.write("could not open port %r: %s\n" % (port, e))
        print("fail.")
        sys.exit(1)

    # V-Sido CONNECTからの受信スレッド立ち上げ
    vsidoconnect.start_reciever()
    print("done.")

    # テストで歩行コマンド
    #vsidoconnect.send_data(vsidoconnect.make_walk_command(100, 0))
    #while True:
    #    time.sleep(1)

    # Tornadoでlisten開始
    print("Starting Web/WebSocket Server...", end="")
    web_app.listen(8080)
    print("done.")

    print("Open http://localhost:8080/")
    print("")

    # Tornadeのメインループ
    tornado.ioloop.IOLoop.instance().start()
