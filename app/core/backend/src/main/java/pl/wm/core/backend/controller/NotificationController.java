package pl.wm.core.backend.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pl.wm.core.backend.service.NotificationService;

import java.util.List;

@RestController
@RequestMapping("/api/notification")
@RequiredArgsConstructor
public class NotificationController {

    private final NotificationService notificationService;

    @GetMapping("/{username}")
    public List<String> getNotifications(@PathVariable String username) {
        return notificationService.getNotifications(username);
    }

    @GetMapping("/pop/{username}")
    public List<String> getNotificationsAndRemove(@PathVariable String username) {
        return notificationService.popNotifications(username);
    }
}
