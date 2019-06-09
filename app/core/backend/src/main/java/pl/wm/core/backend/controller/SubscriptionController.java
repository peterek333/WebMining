package pl.wm.core.backend.controller;

import pl.wm.core.backend.service.SubscriptionService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/subscription")
@RequiredArgsConstructor
public class SubscriptionController {

    private final SubscriptionService subscriptionService;

    @PostMapping("/{keyword}")
    public boolean subscribeKeyword(@PathVariable String keyword) {
        return subscriptionService.subscribeKeyword(keyword);
    }

}
