package pl.wm.core.backend.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import pl.wm.core.backend.domain.SubscribedWord;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
public class NotificationService {
    private static final Logger LOG = LoggerFactory.getLogger(NotificationService.class);

    private Map<String, List<String>> notifications = new HashMap<>();

    @Transactional
    public List<String> popNotifications(String username) {
        List<String> userNotifications = notifications.get(username);

        if (userNotifications != null) {
//            notifications.remove(username);
            LOG.info("Taked notifications for user = " + username);
        }

        return userNotifications;
    }

    @Transactional
    public List<String> getNotifications(String username) {
        return notifications.get(username);
    }

    @Transactional
    public void putNotifications(SubscribedWord subscribedWord) {
        List<String> userNotifications = notifications.get(subscribedWord.getUsername());
        String keyword = subscribedWord.getKeyword();

        if (userNotifications == null) {
            userNotifications = new ArrayList<>();
            userNotifications.add(keyword);
            notifications.put(subscribedWord.getUsername(), userNotifications);
            LOG.info("New notification: keyword = " + keyword + " for user = " + subscribedWord.getUsername());
        } else {
            if ( !userNotifications.contains(keyword)) {
                userNotifications.add(keyword);
                LOG.info("New notification: keyword = " + keyword + " for user = " + subscribedWord.getUsername());
            }
        }
    }

}
