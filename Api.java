

import com.sun.istack.internal.Nullable;
import org.json.JSONObject;

import java.sql.Time;
import java.util.concurrent.TimeUnit;

public class Api {

    public void getData(String func, String IBAN, int amount, String PIN, String idSenBank) {
        try {
            JSONObject dataFromMessage;

            if (func == null) {
                func = "";
            }
            if (PIN == null) {
                PIN = "";
            }
            if (idSenBank == null) {
                idSenBank = "";
            }
            Boolean checkCOnn = false;
            String messageget;
            JavaWebsocket serverconnection = new JavaWebsocket();
            serverconnection.open();
            checkCOnn = serverconnection.getOpen();
            while (!checkCOnn) {
                TimeUnit.MILLISECONDS.sleep(90);
                checkCOnn = serverconnection.getOpen();
            }
            serverconnection.sendData(func, IBAN, amount, PIN, idSenBank);
            TimeUnit.MILLISECONDS.sleep(200);
            messageget = serverconnection.getGetMessage();
            if (messageget != null) {
                System.out.print(messageget);

            } else {
                System.out.println("Message is empty");
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }


    }


}
