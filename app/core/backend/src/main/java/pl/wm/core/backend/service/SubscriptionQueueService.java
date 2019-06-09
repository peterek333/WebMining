package pl.wm.core.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SubscriptionQueueService {

    private final RabbitTemplate rabbitTemplate;

    public boolean sendToQueue(String topicName, String message) {
        rabbitTemplate.convertAndSend(topicName, message);

        return true;
    }

}
