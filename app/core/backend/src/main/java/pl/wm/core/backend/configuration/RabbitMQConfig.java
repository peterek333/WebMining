package pl.wm.core.backend.configuration;

import org.springframework.amqp.core.Queue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class RabbitMQConfig {

    @Value("${queue.name.subscription}")
    private String subscriptionQueueName;

    @Bean
    public Queue notification() {
        return new Queue(subscriptionQueueName);
    }
}
