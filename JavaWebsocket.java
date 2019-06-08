import com.sun.istack.internal.Nullable;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.drafts.*;
import org.java_websocket.handshake.ServerHandshake;

import org.json.JSONObject;
import java.net.URI;

public class JavaWebsocket {

    WebSocketClient mWs;
    String getMessage = null;
    Boolean isOpen = false;

    public void open() throws Exception {
        mWs = new WebSocketClient(new URI("ws://145.24.222.179:8888"), new Draft_6455()) {

            @Override
            public void onMessage(String message) {
                    if (message.length() > 0 && message != null) {
                        System.out.println("Incoming message = " + message);
                        getMessage = message;
                    }
                    else {
                        System.out.println("EMPTY");
                    }
            }

            @Override
            public void onOpen(ServerHandshake handshake) {
                System.out.println("opened connection");
                isOpen = true;
                sendPing();

            }

            @Override
            public void onClose(int code, String reason, boolean remote) {
                System.out.println("closed connection");
            }

            @Override
            public void onError(Exception ex) {
                System.out.println("ERROR 404");
                ex.printStackTrace();
            }


        };

        mWs.setConnectionLostTimeout(120);
        mWs.connect();
    }

    public String getGetMessage() {
        return getMessage;
    }

    public Boolean getOpen() {
        return isOpen;
    }

    public void sendData(String func, String IBAN, int amount, String PIN, String idSenBank){
        try {
            String idRecBank = IBAN.substring(0,2) + IBAN.substring(4,8);
            System.out.println(idRecBank);
            JSONObject command = new JSONObject("{\"Func\":" + '"' + func + '"'
                    + "," + "\"Amount\":" + '"' + amount + '"'
                    + "," + "\"IBAN\":" + '"' + IBAN + '"'
                    + "," + "\"IDRecBank\":" + '"' + idRecBank + '"'
                    + "," + "\"IDSenBank\":" + '"' + idSenBank + '"'
                    + "," + "\"PIN\":" + '"' + PIN + '"' + "}");
            System.out.println(command);
            mWs.send(command.toString());
        }
        catch (Exception e){
            System.out.println("ERROR CAN'T SEND SHIT TO SERVER");
            e.printStackTrace();
        }
    }
}