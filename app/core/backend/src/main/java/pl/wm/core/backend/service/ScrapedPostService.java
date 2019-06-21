package pl.wm.core.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import pl.wm.core.backend.domain.ScrapedPost;
import pl.wm.core.backend.domain.SubscribedWord;
import pl.wm.core.backend.repository.ScrapedPostRepository;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ScrapedPostService {

    private final ScrapedPostRepository scrapedPostRepository;
    private final SubscribedWordService subscribedWordService;

    public List<ScrapedPost> getScrapedPosts() {
        return scrapedPostRepository.findAll();
    }

    public List<ScrapedPost> getScrapedPostsBySiteAndSubscribedKeywords(String site, String username) {
        List<SubscribedWord> subscribedWords = subscribedWordService.getSubscribedWords(username);

        return subscribedWords.stream()
                .map(subscribedWord ->
                        scrapedPostRepository.findAllByKeywordAndSite(subscribedWord.getKeyword(), site))
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
    }

    public List<ScrapedPost> getScrapedPostsBySite(String site) {
        return scrapedPostRepository.findAllBySite(site);
    }

    public List<ScrapedPost> getScrapedPostsBySubscribedKeywords(String username) {
        List<SubscribedWord> subscribedWords = subscribedWordService.getSubscribedWords(username);

        return subscribedWords.stream()
                .map(subscribedWord ->
                        scrapedPostRepository.findAllByKeyword(subscribedWord.getKeyword()))
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
    }
}
