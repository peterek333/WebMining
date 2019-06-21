package pl.wm.core.backend.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import pl.wm.core.backend.domain.SubscribedWord;

import java.util.List;
import java.util.Optional;

public interface SubscribedWordRepository extends MongoRepository<SubscribedWord, String> {

    Optional<SubscribedWord> findFirstByKeywordAndUsername(String keyword, String username);
    List<SubscribedWord> findAllByUsername(String username);
}
