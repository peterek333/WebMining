package pl.wm.core.backend.domain;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Builder
@Getter
@Setter
//@Document(collection = "subscribedWord")
public class SubscribedWord {

    @Id
    private String id;
    private String keyword;
    private String username;

}
