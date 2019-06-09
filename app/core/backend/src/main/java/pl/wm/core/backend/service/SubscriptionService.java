package pl.wm.core.backend.service;

import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;
import pl.wm.core.backend.domain.SubscriptionData;

@Service
@RequiredArgsConstructor
public class SubscriptionService {

    @Value("${queue.name.subscription}")
    private String subscriptionQueueName;

    private final SubscriptionQueueService subscriptionQueueService;
    private final UserService userService;

    public boolean subscribeKeyword(String keyword) {
        String username = userService.getUsernameFromContext();
        if (username != null) {
            SubscriptionData subscriptionData = SubscriptionData.builder()
                    .keyword(keyword)
                    .username(username)
                    .build();

            String serializedData = new Gson().toJson(subscriptionData);
            return subscriptionQueueService.sendToQueue(subscriptionQueueName, serializedData);
        }

        return false;
    }

}
