package pl.wm.core.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class NotificationConsumer {

    private static final String NOTIFICATION_TOPIC = "notification";

    private final SubscriptionService subscriptionService;

    //@RabbitListener(queues = NOTIFICATION_TOPIC)
    private void getNotification(String message) {
        System.out.println(message);
    }

}
