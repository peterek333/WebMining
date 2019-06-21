package pl.wm.core.backend.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import pl.wm.core.backend.domain.ScrapedPost;

import java.util.List;

public interface ScrapedPostRepository extends MongoRepository<ScrapedPost, String> {

    List<ScrapedPost> findAllBySite(String site);
    List<ScrapedPost> findAllByKeyword(String keyword);
    List<ScrapedPost> findAllByKeywordAndSite(String keyword, String site);
}
