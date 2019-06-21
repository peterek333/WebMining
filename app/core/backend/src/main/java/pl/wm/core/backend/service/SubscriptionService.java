package pl.wm.core.backend.service;

import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.wm.core.backend.domain.SubscribedWord;

@Service
@RequiredArgsConstructor
public class SubscriptionService {

    private static final Logger LOG = LoggerFactory.getLogger(SubscriptionService.class);

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

            LOG.info("Subscriberd word: keyword = " + keyword + " for user = " + username);
            return subscriptionQueueService.sendToQueue(subscriptionQueueName, serializedData);
        }

        return false;
    }

}
