package pl.wm.core.backend.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import pl.wm.core.backend.domain.ScrapedPost;
import pl.wm.core.backend.service.ScrapedPostService;

import java.util.Collections;
import java.util.List;

@RestController
@RequestMapping("/api/scrapedPost")
@RequiredArgsConstructor
public class ScrapedPostController {

    private final ScrapedPostService scrapedPostService;

    @GetMapping
    public List<ScrapedPost> getScrapedPosts(@RequestParam(required = false) String site,
                                             @RequestParam(required = false) String username) {
        if (site == null && username == null) {
            return scrapedPostService.getScrapedPosts();
        } else if (site != null && username == null) {
            return scrapedPostService.getScrapedPostsBySite(site);
        } else if (site == null && username != null) {
            return scrapedPostService.getScrapedPostsBySubscribedKeywords(username);
        } else if (site != null && username != null) {
            return scrapedPostService.getScrapedPostsBySiteAndSubscribedKeywords(site, username);
        }
        return Collections.emptyList();
    }

}
