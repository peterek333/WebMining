package pl.wm.core.backend.domain;

import lombok.Builder;
import lombok.Getter;

@Builder
@Getter
public class SubscriptionData {

    private final String keyword;
    private final String username;

}
