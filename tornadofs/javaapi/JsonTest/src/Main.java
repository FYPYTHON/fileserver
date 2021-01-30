
import org.json.JSONObject;
import org.json.JSONException;


public class Main {
    public static void main (String[] args){
        System.out.println("sting to json.");
        stringToJson();
    }

    public static void stringToJson() {
        String str = "{" + "\"" + "latitude" + "\"" + ":" + 30.23 + "," + "\"" + "longitude"
                + "\"" + ":" + 114.57 + "}";
        System.out.println(str + "\n" + str.getClass());
        try {
//            JSONObject jsonObj = (JSONObject)(new JSONParser().parse(str));
            JSONObject jsonObj = new JSONObject(str);
            System.out.println(jsonObj.toString() + "\n" + jsonObj.getClass());
            /*float longitude = (float)jsonObj.get("longitude");
            System.out.println(longitude);*/
            double latitude = (Double) jsonObj.get("latitude");
            System.out.println(latitude);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}