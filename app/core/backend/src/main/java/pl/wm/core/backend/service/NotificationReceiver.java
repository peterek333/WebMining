package pl.wm.core.backend.service;

import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.annotation.RabbitHandler;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
import pl.wm.core.backend.domain.SubscribedWord;
import java.nio.charset.StandardCharsets;

@Component
@RequiredArgsConstructor
@RabbitListener(queues = "notification")
public class NotificationReceiver {

    private final NotificationService notificationService;

    @RabbitHandler
    public void receive(String subscribedWordJson) {
        putNotifications(subscribedWordJson);
    }


    @RabbitHandler
    public void receive(byte[] subscribedWordBytes) {
        String subscribedWordJson = new String(subscribedWordBytes, StandardCharsets.UTF_8);

        putNotifications(subscribedWordJson);
    }

    private void putNotifications(String subscribedWordJson) {
        SubscribedWord subscribedWord = new Gson().fromJson(subscribedWordJson, SubscribedWord.class);

        notificationService.putNotifications(subscribedWord);
    }

}
