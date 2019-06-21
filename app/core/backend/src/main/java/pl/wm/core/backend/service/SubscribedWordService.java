package pl.wm.core.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import pl.wm.core.backend.domain.SubscribedWord;
import pl.wm.core.backend.repository.SubscribedWordRepository;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class SubscribedWordService {

    private final SubscribedWordRepository subscribedWordRepository;

    public SubscribedWord addUniqueSubscribedWord(SubscribedWord subscribedWord) {
        Optional<SubscribedWord> subscribedWordOptional = subscribedWordRepository
                .findFirstByKeywordAndUsername(subscribedWord.getKeyword(), subscribedWord.getUsername());

        return subscribedWordOptional.orElseGet(() -> subscribedWordRepository.save(subscribedWord));
    }

    public List<SubscribedWord> getSubscribedWords(String username) {
        return subscribedWordRepository.findAllByUsername(username);
    }

}
