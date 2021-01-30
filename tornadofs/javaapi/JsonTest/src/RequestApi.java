// package com.yuyuan.yuyuan;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.*;

import org.json.JSONObject;
// javac -encoding UTF-8 RequestApi.java;

public class RequestApi {
    public static void main(String[] args) {
        System.out.println("start request api.");
        requestapi();
    }

    public static void test() {

    }

    public static boolean isEmpty(String str) {
        return str == null || str.length() == 0;
    }

    public static String builderUrlParams(Map<String, String> params) {
        Set<String> keySet = params.keySet();
        List<String> keyList = new ArrayList<String>(keySet);
        Collections.sort(keyList);
        StringBuilder sb = new StringBuilder();
        for (String key : keyList) {
            String value = params.get(key);
            if (isEmpty(value)) {
                continue;
            }
            sb.append(key);
            sb.append("=");
            try {
                sb.append(URLEncoder.encode(params.get(key), "UTF-8"));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
            sb.append("&");
        }
        sb.deleteCharAt(sb.length() - 1);
        return sb.toString();
    }

    public static void requestapi() {
        String sendUrl = "http://139.224.231.14:9016/login";
        //发送请求参数即数据
        Map<String, String> params = new HashMap<String, String>();
        params.put("userAccount", "test");
        params.put("password", "12345a");
        params.put("inputCode", "APP");
        String strparams = builderUrlParams(params);
        try {

            URL url = new URL(sendUrl);
            //打开和url之间的连接
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            PrintWriter out = null;
            //请求方式
            conn.setRequestMethod("POST");
            // Post 请求不能使用缓存
            conn.setUseCaches(false);
            //设置通用的请求属性
            conn.setRequestProperty("User-agent", "Mozilla/5.0 (Linux; U; Android 9; zh-cn; CLT-L29 Build/HUAWEICLT-L29) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/9.8 Mobile Safari/537.36");

//            setHeader("User-Agent","Mozilla/5.0(Windows NT 6.1;Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0");
            //        conn.setRequestProperty("Action",headerType); //header  加入参数
            //设置是否向httpUrlConnection输出，设置是否从httpUrlConnection读入，此外发送post请求必须设置这两个
            //最常用的Http请求无非是get和post，get请求可以获取静态页面，也可以把参数放在URL字串后面，传递给servlet，
            //post与get的 不同之处在于post的参数不是放在URL字串里面，而是放在http请求的正文内。
            conn.setDoOutput(true);
            conn.setDoInput(true);
            //获取URLConnection对象对应的输出流
            out = new PrintWriter(conn.getOutputStream());

            out.print(strparams);
            //缓冲数据
            out.flush();
            //获取URLConnection对象对应的输入流
            InputStream is = conn.getInputStream();
            //构造一个字符流缓存
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String str = "";
            String result = "";
            while ((str = br.readLine()) != null) {
                System.out.println(str);
                result = result + str;
                System.out.println("result:" + result);
            }
            System.out.println("out:" + result);


            //关闭流
            is.close();
            //断开连接，最好写上，disconnect是在底层tcp socket链接空闲时才切断。如果正在被其他线程使用就不切断。
            //固定多线程的话，如果不disconnect，链接会增多，直到收发不出信息。写上disconnect后正常一些。
            conn.disconnect();
            System.out.println("完整结束");

            if (!result.equals("")) {
                JSONObject jsonObj = new JSONObject(result);
                int error_code = (Integer) jsonObj.get("error_code");
                if (error_code == 0) {
                    System.out.println("error_code :" + error_code);
                } else {
                    System.out.println("error:" + jsonObj.get("msg"));
                }

                // System.out.println("user:" + jsonObj.get("user"));
            }
        } catch (IOException e) {
            throw new RuntimeException(String.format("url:%s,param:%s,message:%s", sendUrl, strparams, e.getMessage()), e);
        }
    }
}


