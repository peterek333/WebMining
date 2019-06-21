package pl.wm.core.backend.domain;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;

@Getter
@Setter
public class ScrapedPost {

    @Id
    private String id;
    private String keyword;
    private String title;
    private String url;
    private String site;
    private String createdDatetime;
    private String description;

}
