import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.IOException;
import java.net.Socket;
import java.net.InetSocketAddress;
import java.net.SocketAddress;

public class JsjClient {
    // public static final String IP_ADDR = "127.0.0.1";//服务器地址
    // public static final String IP_ADDR = "192.168.0.87";//服务器地址
    public static final String IP_ADDR = "172.16.83.87";//服务器地址
    public static final int PORT = 5062;//服务器端口号   
    static String text = null;

    public void sendMsg(Socket socket, String msg){
        BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), "utf-8"));
        out.write(msg);
        out.flush();
    }
    public void handleMsg((Socket socket){
        DataInputStream input = new DataInputStream(socket.getInputStream());
        byte[] buffer;
        buffer = new byte[input.available()];
        if(buffer.length != 0){

            // 读取缓冲区
            input.read(buffer);
            // 转换字符串
            String recvMsg = new String(buffer, "utf-8");
            // System.out.println("消息内容：" + recvMsg);
            switch(recvMsg){
                case "update":
                    sendMsg(socket, "update");
                    break;
                default:
                    System.out.println("消息长度："+buffer.length);
                    System.out.println("消息内容：" + recvMsg);

            }

        }
    }
	public static void main(String[] args) throws IOException {   
        System.out.println("客户端启动...");
        //Socket socket = null;
        //socket = new Socket(IP_ADDR, PORT);
		int count = 0;
		boolean isConnect=false;
		Socket socket = null;
        while (true) {

            try {
                while(!isConnect){
                    try{
                        socket = new Socket(IP_ADDR, PORT);
                        isConnect = true;
                    } catch (Exception e) {
                        System.out.println("客户端连接服务器异常:" + e.getMessage());
                        System.out.println("2秒后重新连接...");
                        Thread.sleep(2000);
                    }
                }
                //System.out.println(socket.getInputStream());
				count++;

                //处理服务器端消息
                handleMsg(socket);

				if(count > 10){
					System.out.println("socket已经断开连接。");
					isConnect = false;
					count = 0;
					socket.close();
					// break;
				}
			} catch (Exception e) { 
				System.out.println("客户端异常:" + e.getMessage());
				isConnect = false;
				socket.close();
				socket = null;
				//Thread.sleep(3000);
			}
		}   
	}
}