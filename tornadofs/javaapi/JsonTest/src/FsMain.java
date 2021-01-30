import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.net.MalformedURLException;
import java.util.*;




public class FsMain {
    static boolean isEmpty(String str) {
        return str == null || str.length() == 0;
    }

    static String builderUrlParams(Map<String, String> params) {
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

    public static String asUrlParams(Map<String, String> source) {
        Iterator<String> it = source.keySet().iterator();
        StringBuilder paramStr = new StringBuilder();
        while (it.hasNext()) {
            String key = it.next();
            String value = source.get(key);
            if (value.isEmpty()) {
                continue;
            }
            try {
                // URL 编码
                value = URLEncoder.encode(value, "utf-8");
            } catch (UnsupportedEncodingException e) {
                // do nothing
            }
            paramStr.append("&").append(key).append("=").append(value);
        }
        // 去掉第一个&
        return paramStr.substring(1);
    }

    static JSONObject api(String sendUrl, String method, Map<String, String> params) {
        System.out.println("url:" + sendUrl);
        System.out.println("method:" + method);
        System.out.println("params:" + params.toString());
        String strparams = builderUrlParams(params);
        try {

            URL url = new URL(sendUrl);
            //打开和url之间的连接
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            PrintWriter out = null;
            //请求方式
            conn.setRequestMethod(method);
            // Post 请求不能使用缓存
            conn.setUseCaches(false);
            conn.setDoOutput(true);
            conn.setDoInput(true);
            // json 格式
            conn.setRequestProperty("Accept", "application/json");
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
                return jsonObj;
                // System.out.println("user:" + jsonObj.get("user"));
            } else {
                return null;
            }
        } catch (IOException e) {
            throw new RuntimeException(String.format("url:%s,param:%s,message:%s", sendUrl, strparams, e.getMessage()), e);
        }
    }

    static JSONObject get(String sendUrl, String method, Map<String, String> params) {
        System.out.println("url:" + sendUrl);
        System.out.println("method:" + method);
        System.out.println("params:" + params.toString());
        sendUrl = sendUrl + "?" + asUrlParams(params);
        System.out.println("url parmas:" + sendUrl);
//        String strparams = builderUrlParams(params);
        try {

            URL url = new URL(sendUrl);
            //打开和url之间的连接
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            PrintWriter out = null;
            //请求方式
            conn.setRequestMethod(method);
            // Post 请求不能使用缓存
            conn.setUseCaches(false);
            conn.setDoOutput(true);
            conn.setDoInput(true);
            // json 格式
            conn.setRequestProperty("Accept", "application/json");
            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("HTTP GET Request Failed with Error code : "
                        + conn.getResponseCode());
            }
            StringBuilder sb = new StringBuilder();
            InputStream inStrm = conn.getInputStream();
            byte[] b = new byte[1024];
            int length = -1;
            while ((length = inStrm.read(b)) != -1) {
                sb.append(new String(b, 0, length));
            }
            System.out.println(sb.toString());
            //获取URLConnection对象对应的输出流
            if (sb.toString().equals("")) {
                return null;
            } else {
                JSONObject jsonObj = new JSONObject(sb.toString());
                return jsonObj;
            }

        } catch (IOException e) {
            throw new RuntimeException(String.format("url:%s,param:%s,message:%s", sendUrl, params.toString(), e.getMessage()), e);
        }
    }

    // download file
    public static JSONObject download(String sendUrl, String method, Map<String, String> params) {
        System.out.println("url:" + sendUrl);
        System.out.println("method:" + method);
        System.out.println("params:" + params.toString());
        String strparams = builderUrlParams(params);
        try {
            URL url = new URL(sendUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod(method);
            connection.setRequestProperty("Charset", "UTF-8");

            //
            connection.setUseCaches(false);
            connection.setDoOutput(true);
            connection.setDoInput(true);
            PrintWriter out_p = null;
            out_p = new PrintWriter(connection.getOutputStream());
            out_p.print(strparams);
            out_p.flush();

            int file_leng = connection.getContentLength();
            System.out.println("file length: " + file_leng);
            BufferedInputStream bin = new BufferedInputStream(connection.getInputStream());
            String filename = params.get("filename");
            String path = "./" + filename;
            System.out.println(path);
            File file = new File(path);
            if (!file.getParentFile().exists()) {
                file.getParentFile().mkdirs();
            }
            // connection.getDoInput();
            OutputStream out = new FileOutputStream(file);
            int size = 0;
            int len = 0;
            byte[] buf = new byte[4096];
            while ((size = bin.read(buf)) != -1) {
                len += size;
                out.write(buf, 0, 4096);

                /* android 中为了更新进度条
                Message msg = handler.obtainMessage();
                msg.arg1=len*100/file_leng;
                handler.sendMessage(msg);
                */
                Thread.sleep(100);
                System.out.println("下载了： " + len * 100 / file_leng + "%\n");
            }

            bin.close();
            out.close();

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        JSONObject jsonObj = new JSONObject("{" + "\"" + "msg" + "\"" + ":" + "\"" + "下载成功，文件已保存" +
                "\"" + "}");
        return jsonObj;
    }

    //  ---  upload file  ---
    // download file
    public static JSONObject upload(String urlStr, String method, Map<String, String> params
                                    ,Map<String, String> fileMap) {
        System.out.println("url:" + urlStr);
        System.out.println("method:" + method);
        System.out.println("params:" + params.toString());
        String res = "";
//        String strparams = builderUrlParams(params);
//        String end = "\r\n";
//        String twoHyphens = "--";
        String BOUNDARY = "*****";
//        String newName = "image.jpg";
        HttpURLConnection conn = null;
//        String uploadFile = "storage/sdcard1/bagPictures/102.jpg";
        try {
            URL url = new URL(urlStr);
            conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(30000);
            conn.setDoOutput(true);
            conn.setDoInput(true);
            conn.setUseCaches(false);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Connection", "Keep-Alive");
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.6)");
            conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + BOUNDARY);

            OutputStream out = new DataOutputStream(conn.getOutputStream());
            // text
            if (params != null) {
                StringBuffer strBuf = new StringBuffer();
                Iterator<Map.Entry<String, String>> iter = params.entrySet().iterator();
                while (iter.hasNext()) {
                    Map.Entry<String, String> entry = iter.next();
                    String inputName = (String) entry.getKey();
                    String inputValue = (String) entry.getValue();
                    if (inputValue == null) {
                        continue;
                    }
                    strBuf.append("\r\n").append("--").append(BOUNDARY).append("\r\n");
                    strBuf.append("Content-Disposition: form-data; name=\"" + inputName + "\"\r\n\r\n");
                    strBuf.append(inputValue);
                }
                out.write(strBuf.toString().getBytes());
            }

            // file
            if (fileMap != null) {
                Iterator<Map.Entry<String, String>> iter = fileMap.entrySet().iterator();
                while (iter.hasNext()) {
                    Map.Entry<String, String> entry = iter.next();
                    String inputName = (String) entry.getKey();
                    String inputValue = (String) entry.getValue();
                    if (inputValue == null) {
                        continue;
                    }
                    File file = new File(inputValue);
                    String filename = file.getName();
//                    MagicMatch match = Magic.getMagicMatch(file, false, true);
//                    String contentType = match.getMimeType();
                    String contentType = "multipart/form-data";

                    StringBuffer strBuf = new StringBuffer();
                    strBuf.append("\r\n").append("--").append(BOUNDARY).append("\r\n");
                    strBuf.append("Content-Disposition: form-data; name=\"" + inputName + "\"; filename=\"" + filename + "\"\r\n");
                    strBuf.append("Content-Type:" + contentType + "\r\n\r\n");

                    out.write(strBuf.toString().getBytes());

                    DataInputStream in = new DataInputStream(new FileInputStream(file));
                    int bytes = 0;
                    byte[] bufferOut = new byte[1024];
                    while ((bytes = in.read(bufferOut)) != -1) {
                        out.write(bufferOut, 0, bytes);
                    }
                    in.close();
                }
            }

            byte[] endData = ("\r\n--" + BOUNDARY + "--\r\n").getBytes();
            out.write(endData);
            out.flush();
            out.close();

            // 读取返回数据
            StringBuffer strBuf = new StringBuffer();
            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String line = null;
            while ((line = reader.readLine()) != null) {
                strBuf.append(line).append("\n");
            }
            res = strBuf.toString();
            reader.close();
            reader = null;
        } catch (Exception e) {
            System.out.println("发送POST请求出错。" + urlStr);
            e.printStackTrace();
        } finally {
            if (conn != null) {
                conn.disconnect();
                conn = null;
            }
        }
        System.out.println(res);
        JSONObject jsonObj = new JSONObject(res);
        return jsonObj;
    }


    // get fs main page
    public static void getFsMain() {
        //
        String url = "http://139.224.231.14:9016/app/fsmain";
        Map<String, String> params = new HashMap<String, String>();
        params.put("curpath", "public/File");
        params.put("loginname", "Tornado");
        params.put("token", "2dac3d57d97ee82200b832f0d2c607d1");
        String method = "GET";

        JSONObject result = get(url, method, params);
        if (result == null) {
            System.out.println("fsmain: null");
        } else {
            System.out.println("fsmain:" + result.toString());
        }
    }

    public static void getDownload() {
        String url = "http://139.224.231.14:9016/download";
        Map<String, String> params = new HashMap<String, String>();
        params.put("filename", "public/File/doc/daily/note202006.txt");
        String method = "POST";
        JSONObject result = download(url, method, params);
        if (result == null) {
            System.out.println("fs download: null");
        } else {
            System.out.println("fs download:" + result.toString());
        }
    }

    public static void getUpload(){
        String url = "http://139.224.231.14:9016/app/upload";
        Map<String, String> params = new HashMap<String, String>();
        params.put("curpath", "public/File/doc/test");
        params.put("loginname", "Tornado");
        params.put("token", "27f5cc36db96c26df6b2493fdba80f91");
        Map<String, String> fileparam = new HashMap<String, String>();
        fileparam.put("files", "D:\\project\\PyQt\\FSTornado\\elasticsearch-7.5.1-linux-x86_64.tar.gz");
//        String filename = "D:\\workSpace\\java\\JsonTest\\src\\log.log";
        String method = "POST";
        JSONObject result = upload(url, method, params, fileparam);
        if (result == null) {
            System.out.println("fs upload: null");
        } else {
            System.out.println("fs upload:" + result.toString());
        }
    }
    public static void getRename(){
        String url = "http://139.224.231.14:9016/app/rename";
        Map<String, String> params = new HashMap<String, String>();
        params.put("curpath", "public/File/doc/test");
        params.put("oldname", "wfs.db");
        params.put("newname", "db618.db");
        params.put("loginname", "Tornado");
        params.put("token", "27f5cc36db96c26df6b2493fdba80f91");
//        String filename = "D:\\workSpace\\java\\JsonTest\\src\\log.log";
        String method = "POST";
        JSONObject result = api(url, method, params);
        if (result == null) {
            System.out.println("fs rename: null");
        } else {
            System.out.println("fs rename:" + result.toString());
        }
    }
    public static void getView(){
        String url = "http://139.224.231.14:9016/app/view";
        Map<String, String> params = new HashMap<String, String>();
        params.put("jid", "1717");
        params.put("loginname", "Tornado");
        params.put("token", "e80b81d9cad9ea6bd906c9900c7be67e");
//        String filename = "D:\\workSpace\\java\\JsonTest\\src\\log.log";
        String method = "GET";
        JSONObject result = get(url, method, params);
        if (result == null) {
            System.out.println("fs view: null");
        } else {
//            String jvalue = result.get("jvalue").toString();
            if (result.get("error_code").toString().equals("1")){
                System.out.println(result.toString());
            } else {

                String jdata = result.get("jdata").toString();
                System.out.println("jdate jvalue:");
                System.out.println(jdata);
            }

//            System.out.println(jvalue);
//            System.out.println("fs view:" + result.toString());
        }
    }

    public static void postView(){
        String url = "http://139.224.231.14:9016/app/view";
        Map<String, String> params = new HashMap<String, String>();
        params.put("jid", "1717");
        params.put("jdate", "2020-06-19");
        params.put("jvalue", "3.1900");
        params.put("loginname", "Tornado");
        params.put("token", "1e26c59e58ed3bfe3d122bfd5a62de47");
//        String filename = "D:\\workSpace\\java\\JsonTest\\src\\log.log";
        String method = "POST";
        JSONObject result = api(url, method, params);
        if (result == null) {
            System.out.println("fs view: null");
        } else {
            System.out.println("fs view:" + result.toString());
        }
    }
    public static void getPredict(){
        String url = "http://139.224.231.14:9016/app/predict";
        Map<String, String> params = new HashMap<String, String>();
        params.put("jid", "1717");
        params.put("days", "30");
        params.put("jdate", "2020-06-15");
        params.put("loginname", "Tornado");
        params.put("token", "468ff7bb28836dcea4ea8278566ed911");
//        String filename = "D:\\workSpace\\java\\JsonTest\\src\\log.log";
        String method = "GET";
        JSONObject result = get(url, method, params);
        if (result == null) {
            System.out.println("fs predict: null");
        } else {
//            String jvalue = result.get("jvalue").toString();
//            String jdata = result.get("jdata").toString();
//            System.out.println("jdate jvalue:");
//            System.out.println(jdata);
//            System.out.println(jvalue);
            System.out.println("fs predict:" + result.toString());
        }
    }

    public static void main(String[] args) {
//        getFsMain();
//        getDownload();
//        getUpload();
//        getRename();
//        postView();
        getView();
//        getPredict();
    }
}