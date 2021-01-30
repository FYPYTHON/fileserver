import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.IOException;
import java.net.Socket;
import java.net.InetSocketAddress;
import java.net.SocketAddress;

public class JClient { 
    // public static final String IP_ADDR = "127.0.0.1";//服务器地址
    // public static final String IP_ADDR = "192.168.0.87";//服务器地址
    public static final String IP_ADDR = "172.16.83.87";//服务器地址
    public static final int PORT = 5062;//服务器端口号   
    static String text = null;

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
                //if (socket == null){
                //    SocketAddress remoteAddr = new InetSocketAddress(IP_ADDR,PORT);
                //    socket.connect(remoteAddr, 3000); //等待建立连接的超时时间为1分钟
                //}
                // socket = new Socket(IP_ADDR, PORT);
                //创建一个流套接字并将其连接到指定主机上的指定端口号 
				// DataOutputStream out = new DataOutputStream(socket.getOutputStream());
				BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), "utf-8"));
				// String msg = "已发送->" + String.valueOf(count) + ":次 ip:192.168.0.87";
				// out.writeUTF("已发送->" + String.valueOf(count) + ":次 ip:192.168.0.87");
				String msg = "已发送->" + count + ":次 ip:172.16.83.87";
				// String msg = "已发送";
				//System.out.println(msg);
				// System.out.println(msg.getBytes());
				// out.write(msg.getBytes());
				out.write(msg);
				out.flush();
				count++;
				Thread.sleep(500); 

                //读取服务器端数据   
                DataInputStream input = new DataInputStream(socket.getInputStream());

				byte[] buffer;
				buffer = new byte[input.available()];
				if(buffer.length != 0){
                    System.out.println("消息长度："+buffer.length);
                    // 读取缓冲区
                    input.read(buffer);
                    // 转换字符串
                    String three = new String(buffer, "utf-8");
                    System.out.println("消息内容：" + three);

				}



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