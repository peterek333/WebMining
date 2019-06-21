import axios from 'axios'

const AXIOS = axios.create({
    baseURL: '/api/scrapedPost'
});

export default {
    getScrapedPosts() {
        return AXIOS.get('');
    },
    getScrapedPostsBySite(site) {
        return AXIOS.get('', {
            params: {
                site: site
            }
        });
    },
    getScrapedPostsByUserKeywords(username) {
        return AXIOS.get('', {
            params: {
                username: username
            }
        });
    },
    getScrapedPostsBySiteAndUserKeywords(site, username) {
        return AXIOS.get('', {
            params: {
                site: site,
                username: username
            }
        });
    }
}


