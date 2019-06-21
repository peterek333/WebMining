package pl.wm.core.backend.controller;

import org.springframework.web.bind.annotation.*;
import pl.wm.core.backend.service.SubscriptionService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/subscription")
@RequiredArgsConstructor
public class SubscriptionController {

    private final SubscriptionService subscriptionService;

    @PostMapping("/{keyword}")
    public boolean subscribeKeyword(@PathVariable String keyword, @RequestParam String username) {
        return subscriptionService.subscribeKeyword(keyword, username);
    }

}
