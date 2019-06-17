package pl.wm.core.backend.service;

import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.wm.core.backend.domain.SubscribedWord;

@Service
@RequiredArgsConstructor
public class SubscriptionService {

    @Value("${queue.name.subscription}")
    private String subscriptionQueueName;

    private final SubscriptionQueueService subscriptionQueueService;
    private final UserService userService;
    private final SubscribedWordService subscribedWordService;

    public boolean subscribeKeyword(String keyword) {
        String username = userService.getUsernameFromContext();
        if (username != null) {
            SubscribedWord subscribedWord = SubscribedWord.builder()
                    .keyword(keyword)
                    .username(username)
                    .build();

            subscribedWord = subscribedWordService.addUniqueSubscribedWord(subscribedWord);
            String serializedData = new Gson().toJson(subscribedWord);
            return subscriptionQueueService.sendToQueue(subscriptionQueueName, serializedData);
        }

        return false;
    }

}
